import json
from typing import Any, Dict, List

from common.llm import LLMClient
from common.prompts import INJECT_CONTROLLER_SYSTEM_PROMPT


class Controller:
    def __init__(self, llm: LLMClient, system_prompt: str = INJECT_CONTROLLER_SYSTEM_PROMPT) -> None:
        self.llm = llm
        self.system_prompt = system_prompt

    def decide(
        self,
        case_context: Dict[str, Any],
        reasoner_state: Dict[str, Any],
        action_history: List[Dict[str, Any]],
        max_steps: int,
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
                        "reasoner_state": reasoner_state,
                        "action_history": action_history,
                        "max_steps": max_steps,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
            },
        ]
        data = self.llm.json_chat(messages, required_keys=("completed",))
        completed = self._to_bool(data.get("completed"))
        if completed:
            return {"completed": True}
        tool_calls = self._normalize_tool_calls(data)
        return {"completed": False, "tool_calls": tool_calls}

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
    def _normalize_tool_calls(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        raw_calls = data.get("tool_calls")
        if raw_calls is None and isinstance(data.get("tool_call"), dict):
            raw_calls = [data["tool_call"]]
        if isinstance(raw_calls, dict):
            raw_calls = [raw_calls]
        if not isinstance(raw_calls, list):
            return []

        tool_calls: List[Dict[str, Any]] = []
        for raw_call in raw_calls:
            if not isinstance(raw_call, dict):
                continue
            name = raw_call.get("name") or raw_call.get("tool_name") or raw_call.get("tool")
            args = raw_call.get("args", raw_call.get("parameters", {}))
            if not name:
                nested_calls = [
                    (key, value)
                    for key, value in raw_call.items()
                    if key not in {"args", "parameters", "reasoning"} and isinstance(value, dict)
                ]
                if len(nested_calls) == 1:
                    name, args = nested_calls[0]
            if not name or not isinstance(args, dict):
                continue
            reasoning = raw_call.get("reasoning") or args.pop("reasoning", "")
            tool_calls.append(
                {
                    "name": str(name),
                    "args": args,
                    "reasoning": str(reasoning),
                }
            )
        return tool_calls

    @staticmethod
    def _to_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"true", "yes", "1"}
        return bool(value)
