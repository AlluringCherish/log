import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def split_rank(rank: Any) -> Tuple[str, str]:
    if not isinstance(rank, str) or "_" not in rank:
        return str(rank), ""
    component, reason = rank.split("_", 1)
    if reason in {"delay", "loss"}:
        reason = "latency"
    if reason == "disk":
        reason = "diskio"
    return component.replace("-db", ""), reason


def normalize_prediction(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    normalized = []
    for item in value:
        component, reason = split_rank(item)
        if component and reason:
            normalized.append(f"{component}_{reason}")
    return normalized


def topk_flags(answer: str, prediction: Iterable[str], k: int) -> Dict[str, bool]:
    answer_component, answer_reason = split_rank(answer)
    pred = normalize_prediction(list(prediction))[:k]
    components = []
    reasons = []
    fine = []
    for rank in pred:
        component, reason = split_rank(rank)
        if component not in components:
            components.append(component)
        if reason not in reasons:
            reasons.append(reason)
        fine.append((component, reason))
    return {
        "component": answer_component in components,
        "reason": answer_reason in reasons,
        "both": (answer_component, answer_reason) in fine,
    }


def accuracy(rows: List[Dict[str, Any]], model_key: str) -> Dict[str, float]:
    total = len(rows)
    result: Dict[str, float] = {}
    for k in (1, 2, 3):
        for target in ("component", "reason", "both"):
            result[f"top_{k}_{target}"] = (
                sum(bool(row[f"{model_key}_top_{k}_{target}"]) for row in rows) / total
                if total
                else 0.0
            )
    return result


def summarize_step(step: Dict[str, Any]) -> Dict[str, Any]:
    controller = step.get("controller") or {}
    tool_calls = controller.get("tool_calls") if isinstance(controller, dict) else None
    if not tool_calls:
        tool_calls = step.get("tool_calls")
    reasoner = step.get("reasoner") or {}
    summary: Dict[str, Any] = {
        "step": step.get("step"),
        "completed": bool(controller.get("completed")) if isinstance(controller, dict) else None,
        "tool_calls": tool_calls or [],
        "timing_s": step.get("timing_s"),
    }
    if isinstance(reasoner, dict):
        summary["analysis"] = reasoner.get("analysis")
        if "final_ranking" in reasoner:
            summary["final_ranking"] = reasoner.get("final_ranking")
        state = reasoner.get("state")
        if isinstance(state, dict):
            summary["state_counts"] = {
                key: len(state.get(key, []))
                for key in ("metrics", "traces", "logs", "rankings")
            }
            rankings = state.get("rankings")
            if rankings:
                summary["rankings"] = rankings
    return summary


def summarize_trajectory(record: Dict[str, Any], max_steps: int = 20) -> List[Dict[str, Any]]:
    return [summarize_step(step) for step in record.get("steps", [])[:max_steps]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare Qwen3 8B and Qwen3.5 9B RCA runs.")
    parser.add_argument("--qwen3", required=True, type=Path, help="Qwen3 predictions.json")
    parser.add_argument("--qwen35", required=True, type=Path, help="Qwen3.5 predictions.json")
    parser.add_argument("--problem", required=True, type=Path, help="Benchmark problem.json")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    qwen3_records = {row["case"]: row for row in load_json(args.qwen3)}
    qwen35_records = {row["case"]: row for row in load_json(args.qwen35)}
    problem = load_json(args.problem)
    cases = problem.get("cases", [])
    meta_by_case = {case["case_id"]: case for case in cases}

    common_cases = sorted(set(qwen3_records) & set(qwen35_records))
    rows: List[Dict[str, Any]] = []
    for case_id in common_cases:
        q3 = qwen3_records[case_id]
        q35 = qwen35_records[case_id]
        answer = q3.get("answer") or q35.get("answer") or meta_by_case.get(case_id, {}).get("answer_rank")
        row: Dict[str, Any] = {
            "case": case_id,
            "source_group": meta_by_case.get(case_id, {}).get("source_group"),
            "service": meta_by_case.get(case_id, {}).get("service"),
            "fault": meta_by_case.get(case_id, {}).get("fault"),
            "answer": answer,
            "qwen3_prediction": normalize_prediction(q3.get("prediction")),
            "qwen35_prediction": normalize_prediction(q35.get("prediction")),
            "qwen3_steps": len(q3.get("steps", [])),
            "qwen35_steps": len(q35.get("steps", [])),
            "qwen3_time_s": (q3.get("timing_s") or {}).get("all"),
            "qwen35_time_s": (q35.get("timing_s") or {}).get("all"),
            "qwen3_error": q3.get("error"),
            "qwen35_error": q35.get("error"),
        }
        for model_key, record_key in (("qwen3", "qwen3_prediction"), ("qwen35", "qwen35_prediction")):
            for k in (1, 2, 3):
                flags = topk_flags(str(answer), row[record_key], k)
                for target, value in flags.items():
                    row[f"{model_key}_top_{k}_{target}"] = value
        rows.append(row)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "case_count": len(rows),
        "qwen3": accuracy(rows, "qwen3"),
        "qwen35": accuracy(rows, "qwen35"),
    }
    summary["delta_qwen3_minus_qwen35"] = {
        key: summary["qwen3"][key] - summary["qwen35"][key]
        for key in summary["qwen3"]
    }

    qwen3_only_top1 = [
        row
        for row in rows
        if row["qwen3_top_1_both"] and not row["qwen35_top_1_both"]
    ]
    qwen35_only_top1 = [
        row
        for row in rows
        if row["qwen35_top_1_both"] and not row["qwen3_top_1_both"]
    ]
    qwen3_only_top3 = [
        row
        for row in rows
        if row["qwen3_top_3_both"] and not row["qwen35_top_3_both"]
    ]
    qwen35_only_top3 = [
        row
        for row in rows
        if row["qwen35_top_3_both"] and not row["qwen3_top_3_both"]
    ]
    summary["difference_counts"] = {
        "qwen3_only_top1_both": len(qwen3_only_top1),
        "qwen35_only_top1_both": len(qwen35_only_top1),
        "qwen3_only_top3_both": len(qwen3_only_top3),
        "qwen35_only_top3_both": len(qwen35_only_top3),
    }

    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    fieldnames = [
        "case",
        "source_group",
        "service",
        "fault",
        "answer",
        "qwen3_prediction",
        "qwen35_prediction",
        "qwen3_steps",
        "qwen35_steps",
        "qwen3_time_s",
        "qwen35_time_s",
        "qwen3_error",
        "qwen35_error",
    ]
    for model_key in ("qwen3", "qwen35"):
        for k in (1, 2, 3):
            for target in ("component", "reason", "both"):
                fieldnames.append(f"{model_key}_top_{k}_{target}")

    with (args.output_dir / "case_comparison.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            csv_row = dict(row)
            csv_row["qwen3_prediction"] = json.dumps(row["qwen3_prediction"], ensure_ascii=False)
            csv_row["qwen35_prediction"] = json.dumps(row["qwen35_prediction"], ensure_ascii=False)
            writer.writerow({key: csv_row.get(key) for key in fieldnames})

    diff_payload = {
        "qwen3_only_top1_both": qwen3_only_top1,
        "qwen35_only_top1_both": qwen35_only_top1,
        "qwen3_only_top3_both": qwen3_only_top3,
        "qwen35_only_top3_both": qwen35_only_top3,
    }
    (args.output_dir / "differences.json").write_text(
        json.dumps(diff_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    trajectory_payload = {}
    for group_name, group_rows in diff_payload.items():
        trajectory_payload[group_name] = []
        for row in group_rows:
            case_id = row["case"]
            trajectory_payload[group_name].append(
                {
                    "case": case_id,
                    "meta": meta_by_case.get(case_id, {}),
                    "answer": row["answer"],
                    "qwen3_prediction": row["qwen3_prediction"],
                    "qwen35_prediction": row["qwen35_prediction"],
                    "qwen3_trajectory": summarize_trajectory(qwen3_records[case_id]),
                    "qwen35_trajectory": summarize_trajectory(qwen35_records[case_id]),
                }
            )
    (args.output_dir / "difference_trajectories.json").write_text(
        json.dumps(trajectory_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Qwen Run Comparison",
        "",
        f"- Compared cases: {len(rows)}",
        "",
        "## Accuracy",
        "",
        "| metric | qwen3_8b | qwen35_9b | delta |",
        "|---|---:|---:|---:|",
    ]
    for key in sorted(summary["qwen3"]):
        lines.append(
            f"| {key} | {summary['qwen3'][key]:.4f} | {summary['qwen35'][key]:.4f} | {summary['delta_qwen3_minus_qwen35'][key]:+.4f} |"
        )
    lines.extend(
        [
            "",
            "## Difference Counts",
            "",
            f"- qwen3 only top1 both: {len(qwen3_only_top1)}",
            f"- qwen35 only top1 both: {len(qwen35_only_top1)}",
            f"- qwen3 only top3 both: {len(qwen3_only_top3)}",
            f"- qwen35 only top3 both: {len(qwen35_only_top3)}",
            "",
            "## Top1 Both Differences",
            "",
        ]
    )
    for title, group_rows in (
        ("Qwen3 correct, Qwen3.5 wrong", qwen3_only_top1),
        ("Qwen3 wrong, Qwen3.5 correct", qwen35_only_top1),
    ):
        lines.extend([f"### {title}", ""])
        if not group_rows:
            lines.append("- none")
            lines.append("")
            continue
        for row in group_rows:
            lines.append(
                f"- {row['case']} answer={row['answer']} qwen3={row['qwen3_prediction']} qwen35={row['qwen35_prediction']}"
            )
        lines.append("")
    (args.output_dir / "comparison_summary.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
