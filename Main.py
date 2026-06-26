import argparse
import copy
import json
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Dict, List

from nbformat import v4 as nbf

from Benchmarks.re2_ob import Case, discover_cases, normalize_ranking, write_outputs
from Controller.controller import Controller
from Reasoner.reasoner import DEFAULT_REASONER_STATE, Reasoner
from Tools.offline_aiopslab_tools import OfflineAIOpsLabAPIRuntime, OfflineEvidenceRuntime
from Tools.kg_tools import InjectTimeServiceGraphToolRuntime, RangeWindowServiceGraphToolRuntime
from common.llm import DEFAULT_LOCAL_MODEL, LLMClient, LLMConfigError, require_llm_env
from common.past_reasoning_memory import render_prompt_with_past_reasoning_memory
from common.prompts import (
    API_CONTROLLER_SYSTEM_PROMPT,
    API_REASONER_SYSTEM_PROMPT,
    EVIDENCE_CONTROLLER_SYSTEM_PROMPT,
    EVIDENCE_REASONER_SYSTEM_PROMPT,
    INJECT_CONTROLLER_SYSTEM_PROMPT,
    INJECT_REASONER_SYSTEM_PROMPT,
    RANGE_CONTROLLER_SYSTEM_PROMPT,
    RANGE_REASONER_SYSTEM_PROMPT,
)


MAX_TOOL_RETRIES = 2
FINAL_REASONER_OBSERVATION = (
    "No new tool observation. Produce the final answer from the accumulated previous_reasoner_state only."
)
FINAL_RANKING_SCHEMA_INSTRUCTIONS = (
    "Produce the final top-3 root-cause ranking now from the accumulated Reasoner analysis and structured state. "
    "Return exactly one compact JSON object with exactly two keys: "
    "`analysis` and `final_ranking`. Keep `analysis` under 40 words in plain prose. "
    "`final_ranking` must be a ranked array of up to 3 root-cause candidate objects ordered from most likely to least likely. "
    "Each object must have exactly these fields: "
    "`time` as Unix seconds, `component` as one candidate component listed in the system prompt, "
    "and `reason` as one candidate reason listed in the system prompt. Derive `time` from the first data point of the selected "
    "consecutive anomalous component-KPI sub-series. Choose `reason` from the abnormal component-local metrics KPI key. "
    "Use logs and traces as validation evidence for the metrics-led component/reason hypothesis. "
    "Do not request tools or mention future investigation. "
    "Return only the allowed keys and fields named above."
)

EVIDENCE_FINAL_RANKING_SCHEMA_INSTRUCTIONS = (
    "Produce the final top-3 root-cause ranking now from the accumulated Reasoner analysis and structured state. "
    "Return exactly one compact JSON object with exactly two keys: "
    "`analysis` and `final_ranking`. Keep `analysis` under 40 words in plain prose. "
    "`final_ranking` must be a ranked array of up to 3 root-cause candidate objects ordered from most likely to least likely. "
    "Each object must have exactly these fields: "
    "`time` as relative seconds from the beginning of the case, `component` as one candidate component listed in the system prompt, "
    "and `reason` as one candidate reason listed in the system prompt. Derive `time` from the first data point of the selected "
    "consecutive anomalous component-KPI sub-series. Choose `reason` only from the abnormal component-local metrics KPI key. "
    "Do not change the reason to latency solely because trace latency is high. "
    "Use traces second and logs third as validation evidence for the metrics-led component/reason hypothesis. "
    "Do not request tools or mention future investigation. "
    "Return only the allowed keys and fields named above."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reasoner-Controller RCA agent with KG tools.")
    parser.add_argument("--data-root", required=True, help="Path to local data directory.")
    parser.add_argument("--case-limit", type=int, default=None, help="Limit number of cases for smoke tests.")
    parser.add_argument(
        "--case-indices",
        default=None,
        help="Comma-separated 1-based case indices to run, e.g. 1,30,60.",
    )
    parser.add_argument("--output-dir", default="output", help="Directory for predictions and traces.")
    parser.add_argument("--max-steps", type=int, default=10, help="Maximum Controller tool-call steps per case.")
    parser.add_argument(
        "--time-context",
        choices=["inject", "range", "api", "evidence"],
        default="inject",
        help="Telemetry mode. `inject` uses pre-attached KG summaries; `range` uses windowed KG calls; `api` exposes offline AIOpsLab-style read APIs; `evidence` exposes precomputed get_evidence.",
    )
    parser.add_argument("--llm-backend", choices=["local", "openai"], default="local", help="LLM backend to use.")
    parser.add_argument("--local-model", default=DEFAULT_LOCAL_MODEL, help="Local Qwen model directory.")
    parser.add_argument("--model", default=None, help="OpenAI-compatible model override. Defaults to OPENAI_MODEL.")
    parser.add_argument("--max-new-tokens", type=int, default=1024, help="Maximum generated tokens per LLM call.")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument(
        "--parallelism",
        type=int,
        default=1,
        help="Number of cases to run concurrently. Use only with OpenAI-compatible API backends.",
    )
    parser.add_argument("--cpu", action="store_true", help="Force local model to run on CPU. Very slow for Qwen3-8B.")
    parser.add_argument(
        "--past-reasoning-memory",
        default=None,
        help=(
            "Optional path to past observation -> analysis -> ranking examples. "
            "Applied to the evidence Reasoner prompt placeholder only."
        ),
    )
    return parser.parse_args()


def parse_case_indices(value: str) -> List[int]:
    indices: List[int] = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        index = int(item)
        if index <= 0:
            raise ValueError(f"Case indices are 1-based positive integers: {index}")
        indices.append(index)
    if not indices:
        raise ValueError("--case-indices must include at least one index")
    return indices


def write_notebook(case: Case, prediction: List[str], steps: List[Dict[str, Any]], notebook_path: str) -> None:
    nb = nbf.new_notebook()
    nb.cells.append(
        nbf.new_markdown_cell(
            "# RCA Trajectory\n\n"
            f"- Case: `{case.name}`\n"
            f"- Prediction: `{prediction}`"
        )
    )

    for step in steps:
        step_id = step.get("step")
        reasoner = step.get("reasoner", {})
        controller = step.get("controller")
        tool_calls = step.get("tool_calls") or (controller or {}).get("tool_calls")
        observation = step.get("observation", "")

        nb.cells.append(
            nbf.new_markdown_cell(
                f"## Step {step_id}\n\n"
                f"### Controller\n```json\n{json.dumps(controller, ensure_ascii=False, indent=2)}\n```\n\n"
                + (
                    f"### Tool Calls\n```json\n{json.dumps(tool_calls, ensure_ascii=False, indent=2)}\n```\n"
                    if tool_calls
                    else ""
                )
            )
        )

        if "code" in step:
            nb.cells.append(nbf.new_code_cell(step.get("code", "")))

        nb.cells.append(
            nbf.new_markdown_cell(
                "### Observation\n\n"
                f"```\n{observation}\n```"
            )
        )

        if reasoner:
            nb.cells.append(
                nbf.new_markdown_cell(
                    "### Reasoner\n"
                    f"```json\n{json.dumps(reasoner, ensure_ascii=False, indent=2)}\n```"
                )
            )

    os.makedirs(os.path.dirname(notebook_path), exist_ok=True)
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)


def execute_tool_calls_with_retry(
    controller: Controller,
    tool_runtime: Any,
    case_context: Dict[str, Any],
    reasoner_state: Dict[str, Any],
    action_history: List[Dict[str, Any]],
    decision: Dict[str, Any],
    max_steps: int,
    max_retries: int = MAX_TOOL_RETRIES,
) -> Dict[str, Any]:
    attempts: List[Dict[str, Any]] = []
    current_decision = decision
    tool_calls = current_decision.get("tool_calls", [])
    tool_elapsed_s = 0.0
    controller_retry_elapsed_s = 0.0

    def timing() -> Dict[str, float]:
        return {
            "tool": tool_elapsed_s,
            "controller_retry": controller_retry_elapsed_s,
        }

    for attempt_no in range(1, max_retries + 2):
        tool_start = time.perf_counter()
        tool_observations = tool_runtime.execute_tool_calls(tool_calls)
        tool_elapsed_s += time.perf_counter() - tool_start
        status = all(bool(item.get("status")) for item in tool_observations)
        attempts.append(
            {
                "attempt": attempt_no,
                "tool_calls": tool_calls,
                "tool_observations": tool_observations,
                "status": status,
            }
        )
        if (
            status
            or attempt_no > max_retries
            or (
                case_context.get("time_context") != "evidence"
                and all_non_overlapping_window_failures(tool_observations)
            )
        ):
            return {
                "decision": current_decision,
                "tool_calls": tool_calls,
                "tool_observations": tool_observations,
                "attempts": attempts,
                "status": status,
                "timing_s": timing(),
            }

        retry_feedback = {
            "tool_calls": tool_calls,
            "tool_observations": tool_observations,
            "status": False,
            "feedback": (
                "One or more tool calls failed. Return corrected `tool_calls` that fix the tool name or arguments. "
                "Set `completed` to false in this retry response."
            ),
        }
        controller_retry_start = time.perf_counter()
        retry_decision = controller.decide(
            case_context,
            reasoner_state,
            action_history + [retry_feedback],
            max_steps=max_steps,
        )
        controller_retry_elapsed_s += time.perf_counter() - controller_retry_start
        retry_decision = suppress_repeated_tool_calls(retry_decision, action_history + [retry_feedback])
        if retry_decision.get("completed"):
            return {
                "decision": retry_decision,
                "tool_calls": tool_calls,
                "tool_observations": tool_observations,
                "attempts": attempts,
                "status": status,
                "timing_s": timing(),
            }
        current_decision = retry_decision
        tool_calls = current_decision.get("tool_calls", [])

    return {
        "decision": current_decision,
        "tool_calls": tool_calls,
        "tool_observations": [],
        "attempts": attempts,
        "status": False,
        "timing_s": timing(),
    }


def rounded_timing_s(**values: float) -> Dict[str, float]:
    return {key: round(float(value), 3) for key, value in values.items()}


def all_non_overlapping_window_failures(tool_observations: List[Dict[str, Any]]) -> bool:
    if not tool_observations:
        return False
    for item in tool_observations:
        if item.get("status"):
            return False
        observation = str(item.get("observation", ""))
        if "Requested window does not overlap the available telemetry range" not in observation:
            return False
    return True


def tool_call_signature(call: Dict[str, Any]) -> str:
    return json.dumps(
        {
            "name": call.get("name"),
            "args": call.get("args", {}),
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def suppress_repeated_tool_calls(decision: Dict[str, Any], action_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    if decision.get("completed"):
        return decision

    tool_calls = decision.get("tool_calls", [])
    if not isinstance(tool_calls, list) or not tool_calls:
        return decision

    executed_signatures = set()
    for entry in action_history:
        for call in entry.get("tool_calls", []) or []:
            if isinstance(call, dict):
                executed_signatures.add(tool_call_signature(call))

    filtered_calls = [
        call
        for call in tool_calls
        if isinstance(call, dict) and tool_call_signature(call) not in executed_signatures
    ]
    if len(filtered_calls) == len(tool_calls):
        return decision

    filtered_decision = dict(decision)
    if filtered_calls:
        filtered_decision["completed"] = False
        filtered_decision["tool_calls"] = filtered_calls
    else:
        filtered_decision["completed"] = True
        filtered_decision.pop("tool_calls", None)
    return filtered_decision


def compact_tool_observations(tool_observations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    compact: List[Dict[str, Any]] = []
    for item in tool_observations:
        call = item.get("tool_call", {})
        summary: Dict[str, Any] = {
            "tool_call": {
                "name": call.get("name"),
                "args": call.get("args", {}),
            },
            "status": item.get("status"),
        }
        observation = item.get("observation")
        if isinstance(observation, str):
            try:
                payload = json.loads(observation)
            except json.JSONDecodeError:
                payload = None
            if isinstance(payload, dict):
                summary["observation_summary"] = summarize_api_observation(payload)
            else:
                summary["observation_summary"] = observation[:500]
        else:
            summary["observation_summary"] = observation
        compact.append(summary)
    return compact


def summarize_api_observation(payload: Dict[str, Any]) -> Dict[str, Any]:
    telemetry = payload.get("telemetry")
    summary: Dict[str, Any] = {
        "telemetry": telemetry,
        "component": payload.get("component"),
        "window": payload.get("window"),
    }
    if telemetry == "metrics":
        summary["matched_rows"] = payload.get("matched_rows")
        summary["metrics"] = [
            {
                "metric": item.get("metric"),
                "count": item.get("count"),
                "mean": item.get("mean"),
                "std": item.get("std"),
                "min": item.get("min"),
                "max": item.get("max"),
                "p95": item.get("p95"),
                "p99": item.get("p99"),
            }
            for item in payload.get("items", [])
            if isinstance(item, dict)
        ]
    elif telemetry == "logs":
        summary["total_count"] = payload.get("total_count")
        summary["count_by_level"] = payload.get("count_by_level")
        summary["top_templates"] = payload.get("top_templates", [])[:3]
    elif telemetry == "traces":
        summary["expansion"] = payload.get("expansion")
        summary["downstream_components"] = payload.get("downstream_components")
        summary["edge_count"] = payload.get("edge_count")
        summary["summary_row_count"] = payload.get("summary_row_count")
        summary["matched_spans"] = payload.get("matched_spans")
        summary["operation_summaries"] = payload.get("operation_summaries", [])[:3]
    elif telemetry == "evidence":
        summary["query"] = payload.get("query")
        summary["returned_count"] = payload.get("returned_count")
        summary["matched_count"] = payload.get("matched_count")
        summary["truncated"] = payload.get("truncated")
        summary["next_start_time"] = payload.get("next_start_time")
        summary["returned_windows"] = payload.get("returned_windows")
        summary["lines"] = payload.get("lines", [])[:30]
    else:
        for key in ("matched_rows", "total_count", "matched_spans"):
            if key in payload:
                summary[key] = payload[key]
    return summary


def final_ranking_instructions(time_context: str) -> str:
    if time_context == "evidence":
        return EVIDENCE_FINAL_RANKING_SCHEMA_INSTRUCTIONS
    return FINAL_RANKING_SCHEMA_INSTRUCTIONS


def run_case(
    case: Case,
    reasoner: Reasoner,
    controller: Controller,
    max_steps: int,
    trace_dir: str,
    time_context: str,
) -> Dict[str, Any]:
    case_start = time.perf_counter()
    if time_context == "evidence":
        tool_runtime = OfflineEvidenceRuntime(case)
    elif time_context == "api":
        tool_runtime = OfflineAIOpsLabAPIRuntime(case)
    elif time_context == "range":
        tool_runtime = RangeWindowServiceGraphToolRuntime(case)
    else:
        tool_runtime = InjectTimeServiceGraphToolRuntime(case)
    case_context = case.agent_context(time_context=time_context)
    reasoner_state: Dict[str, Any] = {
        "analysis": "No analysis has been performed yet.",
        "state": copy.deepcopy(DEFAULT_REASONER_STATE),
    }
    if time_context == "evidence":
        latest_observation = (
            "Initial case metadata and precomputed evidence relative time range are available. "
            "No get_evidence API has been called yet."
        )
    elif time_context == "api":
        latest_observation = (
            "Initial case metadata and offline telemetry timestamp ranges are available. "
            "No read API has been called yet."
        )
    elif time_context == "range":
        latest_observation = (
            "Initial case metadata and global telemetry timestamp ranges are available. No tool has been called yet."
        )
    else:
        latest_observation = (
            "Initial case metadata and KG telemetry summaries are available. No tool has been called yet."
        )
    action_history: List[Dict[str, Any]] = []
    steps: List[Dict[str, Any]] = []
    prediction: List[str] = []
    final_ranking: List[Any] = []

    for step_no in range(1, max_steps + 1):
        step_start = time.perf_counter()
        controller_start = time.perf_counter()
        decision = controller.decide(case_context, reasoner_state, action_history, max_steps=max_steps)
        controller_elapsed_s = time.perf_counter() - controller_start
        decision = suppress_repeated_tool_calls(decision, action_history)

        step_record: Dict[str, Any] = {
            "step": step_no,
            "controller": decision,
        }

        if decision["completed"]:
            final_prompt = (
                "The Controller has terminated the diagnosis. "
                f"{final_ranking_instructions(time_context)}"
            )
            reasoner_start = time.perf_counter()
            reasoner_state = reasoner.analyze(
                case_context,
                reasoner_state,
                FINAL_REASONER_OBSERVATION,
                final_prompt=final_prompt,
            )
            reasoner_elapsed_s = time.perf_counter() - reasoner_start
            final_ranking = reasoner_state.get("final_ranking", [])
            prediction = normalize_ranking(final_ranking)
            step_record["observation"] = "Controller marked analysis complete."
            step_record["reasoner"] = reasoner_state
            step_record["timing_s"] = rounded_timing_s(
                controller=controller_elapsed_s,
                reasoner=reasoner_elapsed_s,
                tool=0.0,
                all=time.perf_counter() - step_start,
            )
            steps.append(step_record)
            break

        execution = execute_tool_calls_with_retry(
            controller,
            tool_runtime,
            case_context,
            reasoner_state,
            action_history,
            decision,
            max_steps=max_steps,
        )
        execution_timing = execution.get("timing_s", {})
        controller_elapsed_s += float(execution_timing.get("controller_retry", 0.0))
        decision = execution["decision"]
        tool_calls = execution["tool_calls"]
        tool_observations = execution["tool_observations"]
        status = execution["status"]
        observation = json.dumps(
            {
                "tool_observations": tool_observations,
                **(
                    {"tool_retry_attempts": execution["attempts"]}
                    if len(execution["attempts"]) > 1 or not status
                    else {}
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
        action_history.append(
            {
                "tool_calls": tool_calls,
                "status": status,
            }
        )
        latest_observation = observation
        step_record["controller"] = decision
        step_record["tool_observations"] = tool_observations
        if len(execution["attempts"]) > 1 or not status:
            step_record["tool_retry_attempts"] = execution["attempts"]
        step_record["status"] = status
        step_record["observation"] = observation
        reasoner_start = time.perf_counter()
        reasoner_state = reasoner.analyze(case_context, reasoner_state, latest_observation)
        reasoner_elapsed_s = time.perf_counter() - reasoner_start
        step_record["reasoner"] = reasoner_state
        step_record["timing_s"] = rounded_timing_s(
            controller=controller_elapsed_s,
            reasoner=reasoner_elapsed_s,
            tool=float(execution_timing.get("tool", 0.0)),
            all=time.perf_counter() - step_start,
        )
        steps.append(step_record)

    if not prediction:
        step_start = time.perf_counter()
        final_prompt = (
            "Maximum steps reached. "
            f"{final_ranking_instructions(time_context)}"
        )
        reasoner_start = time.perf_counter()
        reasoner_state = reasoner.analyze(
            case_context,
            reasoner_state,
            FINAL_REASONER_OBSERVATION,
            final_prompt=final_prompt,
        )
        reasoner_elapsed_s = time.perf_counter() - reasoner_start
        final_ranking = reasoner_state.get("final_ranking", [])
        prediction = normalize_ranking(final_ranking)
        steps.append(
            {
                "step": "max_steps_reasoner_final",
                "controller": None,
                "reasoner": reasoner_state,
                "observation": final_prompt,
                "timing_s": rounded_timing_s(
                    controller=0.0,
                    reasoner=reasoner_elapsed_s,
                    tool=0.0,
                    all=time.perf_counter() - step_start,
                ),
            }
        )

    case_timing_s = rounded_timing_s(all=time.perf_counter() - case_start)
    os.makedirs(trace_dir, exist_ok=True)
    with open(os.path.join(trace_dir, f"{case.name}.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "case": case_context,
                "prediction": prediction,
                "final_ranking": final_ranking,
                "steps": steps,
                "timing_s": case_timing_s,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    write_notebook(case, prediction, steps, os.path.join(trace_dir, f"{case.name}.ipynb"))

    return {
        "case": case,
        "prediction": prediction,
        "final_ranking": final_ranking,
        "steps": steps,
        "timing_s": case_timing_s,
        "time_context": time_context,
    }


def main() -> None:
    args = parse_args()
    if args.parallelism <= 0:
        raise ValueError("--parallelism must be a positive integer")
    if args.parallelism > 1 and args.llm_backend == "local":
        raise ValueError("--parallelism > 1 is supported only with OpenAI-compatible API backends")
    require_llm_env(args.model, backend=args.llm_backend, local_model=args.local_model)

    all_cases = discover_cases(args.data_root)
    if args.case_indices:
        indices = parse_case_indices(args.case_indices)
        cases = []
        for index in indices:
            if index > len(all_cases):
                raise ValueError(f"Case index {index} is out of range; only {len(all_cases)} cases found")
            cases.append(all_cases[index - 1])
    else:
        cases = all_cases[: args.case_limit] if args.case_limit is not None else all_cases
    llm = LLMClient(
        model=args.model,
        temperature=args.temperature,
        backend=args.llm_backend,
        local_model=args.local_model,
        max_new_tokens=args.max_new_tokens,
        top_p=args.top_p,
        cpu=args.cpu,
    )
    if args.time_context == "evidence":
        reasoner_prompt = render_prompt_with_past_reasoning_memory(
            EVIDENCE_REASONER_SYSTEM_PROMPT,
            args.past_reasoning_memory,
        )
        controller_prompt = EVIDENCE_CONTROLLER_SYSTEM_PROMPT
    elif args.time_context == "api":
        reasoner_prompt = API_REASONER_SYSTEM_PROMPT
        controller_prompt = API_CONTROLLER_SYSTEM_PROMPT
    elif args.time_context == "range":
        reasoner_prompt = RANGE_REASONER_SYSTEM_PROMPT
        controller_prompt = RANGE_CONTROLLER_SYSTEM_PROMPT
    else:
        reasoner_prompt = INJECT_REASONER_SYSTEM_PROMPT
        controller_prompt = INJECT_CONTROLLER_SYSTEM_PROMPT
    reasoner = Reasoner(llm, system_prompt=reasoner_prompt)
    controller = Controller(llm, system_prompt=controller_prompt)

    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.abspath(args.output_dir)
    trace_dir = os.path.join(output_dir, "traces", run_id)
    records: List[Dict[str, Any]] = []

    print(f"Loaded {len(cases)} cases from {args.data_root}")
    print(f"Writing outputs to {output_dir}")
    if args.parallelism > 1:
        print(f"Running with parallelism={args.parallelism}")

    def run_one(index: int, case: Case) -> Dict[str, Any]:
        try:
            return run_case(case, reasoner, controller, args.max_steps, trace_dir, args.time_context)
        except Exception as exc:
            print(f"  failed: {case.name}: {exc}")
            return {
                "case": case,
                "prediction": [],
                "error": str(exc),
                "steps": [{"traceback": traceback.format_exc()}],
                "time_context": args.time_context,
            }

    if args.parallelism == 1:
        for index, case in enumerate(cases, start=1):
            print(f"[{index}/{len(cases)}] {case.name}")
            records.append(run_one(index, case))
            write_outputs(output_dir, records)
    else:
        records_by_index: List[Any] = [None] * len(cases)
        with ThreadPoolExecutor(max_workers=args.parallelism) as executor:
            futures = {
                executor.submit(run_one, index, case): (index, case)
                for index, case in enumerate(cases, start=1)
            }
            for completed_count, future in enumerate(as_completed(futures), start=1):
                index, case = futures[future]
                print(f"[{completed_count}/{len(cases)} done] {case.name}")
                records_by_index[index - 1] = future.result()
                records = [record for record in records_by_index if record is not None]
                write_outputs(output_dir, records)

    print("Done.")
    print(f"Predictions: {os.path.join(output_dir, 'predictions.json')}")
    print(f"Evaluation: {os.path.join(output_dir, 'evaluation.json')}")


if __name__ == "__main__":
    try:
        main()
    except LLMConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(2)
