import json
from typing import Any, Dict, List

from common.llm import LLMClient
from common.prompts import INJECT_REASONER_SYSTEM_PROMPT


BASE_FORBIDDEN_REASONER_KEYS = (
    "action_type",
    "params",
    "instruction",
    "next_action",
    "analysis_goal",
    "ready_to_answer",
    "completed",
    "terminate",
    "done",
    "summary",
    "tool_call",
    "tool_calls",
)

NORMAL_FORBIDDEN_REASONER_KEYS = BASE_FORBIDDEN_REASONER_KEYS + (
    "final_ranking",
)
FINAL_FORBIDDEN_REASONER_KEYS = BASE_FORBIDDEN_REASONER_KEYS + (
    "state",
)


DEFAULT_REASONER_STATE: Dict[str, Any] = {
    "metrics": [],
    "traces": [],
    "logs": [],
    "rankings": [],
}


class Reasoner:
    def __init__(self, llm: LLMClient, system_prompt: str = INJECT_REASONER_SYSTEM_PROMPT) -> None:
        self.llm = llm
        self.system_prompt = system_prompt

    def analyze(
        self,
        case_context: Dict[str, Any],
        previous_state: Dict[str, Any],
        latest_observation: str,
        final_prompt: str = "",
    ) -> Dict[str, Any]:
        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "case_context": self._llm_case_context(case_context),
                        "previous_reasoner_state": previous_state,
                        "latest_tool_observation": latest_observation,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
            },
        ]
        if final_prompt:
            messages.append({"role": "user", "content": final_prompt})

        is_final = bool(final_prompt)
        data = self.llm.json_chat(
            messages,
            required_keys=("analysis", "final_ranking") if is_final else ("analysis", "state"),
            forbidden_keys=FINAL_FORBIDDEN_REASONER_KEYS if is_final else NORMAL_FORBIDDEN_REASONER_KEYS,
        )
        if is_final:
            data = {
                "analysis": str(data.get("analysis", "")),
                "final_ranking": self._normalize_final_ranking(data.get("final_ranking")),
            }
        else:
            next_state = self._normalize_state(data.get("state"))
            data = {
                "analysis": str(data.get("analysis", "")),
                "state": self._merge_state(previous_state, next_state),
            }
        return data

    @staticmethod
    def _llm_case_context(case_context: Dict[str, Any]) -> Dict[str, Any]:
        if case_context.get("time_context") == "api":
            time_range = case_context.get("telemetry_time_range") or {}
            return {
                "case_name": case_context.get("case_name"),
                "telemetry_time_range": {
                    "start_time": time_range.get("start_time"),
                    "end_time": time_range.get("end_time"),
                },
            }
        return case_context

    @staticmethod
    def _as_list(value: Any) -> List[Any]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    @staticmethod
    def _normalize_final_ranking(value: Any) -> List[Dict[str, Any]]:
        ranking: List[Dict[str, Any]] = []
        for item in Reasoner._as_list(value):
            if not isinstance(item, dict):
                continue
            ranking.append(
                {
                    "time": item.get("time"),
                    "component": item.get("component"),
                    "reason": Reasoner._canonical_reason(item.get("reason")),
                }
            )
            if len(ranking) >= 3:
                break
        return ranking

    @staticmethod
    def _canonical_reason(value: Any) -> Any:
        if value is None:
            return None
        text = str(value)
        normalized = text.strip().lower()
        for reason in ("cpu", "mem", "diskio", "latency", "socket"):
            if normalized == reason or normalized.startswith(f"{reason}-") or normalized.startswith(f"{reason}_"):
                return reason
        return text

    @staticmethod
    def _normalize_state(value: Any) -> Dict[str, Any]:
        state = dict(DEFAULT_REASONER_STATE)
        if not isinstance(value, dict):
            return state
        for key in state:
            raw = value.get(key, [])
            state[key] = raw if isinstance(raw, list) else []
        for key in ("metrics", "traces", "logs"):
            state[key] = [str(item) for item in state[key] if item is not None]
        state["rankings"] = Reasoner._normalize_rankings(state["rankings"])
        return state

    @staticmethod
    def _normalize_rankings(value: Any) -> List[Any]:
        if not isinstance(value, list):
            return []
        rankings: List[Any] = []
        for item in value:
            if not isinstance(item, dict):
                continue
            rankings.append(
                {
                    "rank": item.get("rank"),
                    "component": item.get("component"),
                    "reason": item.get("reason"),
                }
            )
        return rankings

    @staticmethod
    def _merge_state(previous_state: Any, next_state: Dict[str, Any]) -> Dict[str, Any]:
        previous_payload = previous_state.get("state") if isinstance(previous_state, dict) else None
        previous = Reasoner._normalize_state(previous_payload)
        merged = dict(DEFAULT_REASONER_STATE)
        for key in ("metrics", "traces", "logs"):
            merged[key] = Reasoner._dedupe_items(previous.get(key, []) + next_state.get(key, []))
        merged["rankings"] = next_state.get("rankings") or previous.get("rankings", [])
        return merged

    @staticmethod
    def _dedupe_items(items: List[Any]) -> List[Any]:
        deduped: List[Any] = []
        seen = set()
        for item in items:
            try:
                marker = json.dumps(item, sort_keys=True, ensure_ascii=False)
            except TypeError:
                marker = repr(item)
            if marker in seen:
                continue
            seen.add(marker)
            deduped.append(item)
        return deduped
