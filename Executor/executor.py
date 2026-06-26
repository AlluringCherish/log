import re
import traceback
from typing import Any, Dict, List, Tuple

from IPython.terminal.embed import InteractiveShellEmbed

from Benchmarks.re2_ob import Case
from common.llm import LLMClient
from common.prompts import EXECUTOR_SYSTEM_PROMPT, OPENRCA_EXECUTOR_CODE_RULES


CODE_BLOCK_RE = re.compile(r"```python\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)


class Executor:
    system_prompt = EXECUTOR_SYSTEM_PROMPT

    def __init__(self, case: Case, llm: LLMClient, max_retries: int = 2) -> None:
        self.case = case
        self.llm = llm
        self.max_retries = max_retries
        self.history: List[Dict[str, str]] = self._initial_history()
        self.kernel = InteractiveShellEmbed()
        self._initialize_kernel()

    def reset(self) -> None:
        self.kernel.reset()
        self.history = self._initial_history()
        self._initialize_kernel()

    def execute(self, instruction: str) -> Tuple[str, str, bool]:
        self.history.append({"role": "user", "content": instruction})
        prompt = list(self.history)
        code = ""
        result = ""

        for _ in range(self.max_retries):
            response = self.llm.chat(prompt + [self._continuation_note()])
            code = self._extract_code(response)

            if self._has_forbidden_code(code):
                prompt.extend(
                    [
                        {"role": "assistant", "content": response},
                        {
                            "role": "user",
                            "content": (
                                "You are not permitted to generate visualizations, shell commands, or file writes. "
                                "Revise the answer and provide text-only Python analysis code."
                            ),
                        },
                    ]
                )
                continue

            execution = self.kernel.run_cell(code)
            if execution.success:
                result = str(execution.result).strip()
                if not result:
                    result = "<empty execution result>"
                result = self._truncate_result(result)
                self.history.append({"role": "assistant", "content": f"```python\n{code}\n```"})
                return code, result, True

            err = self._format_error(execution)
            result = err
            prompt.extend(
                [
                    {"role": "assistant", "content": f"```python\n{code}\n```"},
                    {"role": "user", "content": f"Execution failed:\n{err}\nPlease revise your code and retry."},
                ]
            )

        failure = "The Executor failed to complete the instruction, please re-write a new instruction for Executor."
        self.history.append({"role": "assistant", "content": failure})
        return code or failure, result or failure, False

    def _initialize_kernel(self) -> None:
        graph = self.case.agent_context().get("service_dependency_graph", {})
        init_code = f"""
import json
import os
import pandas as pd
import numpy as np
pd.set_option('display.width', 427)
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 20)

case_name = {self.case.name!r}
case_dir = {self.case.case_dir!r}
metric_path = {self.case.metric_path!r}
logs_path = {self.case.logs_path!r}
traces_path = {self.case.traces_path!r}
tracets_err_path = {self.case.tracets_err_path!r}
tracets_lat_path = {self.case.tracets_lat_path!r}
inject_time = {self.case.inject_time!r}
possible_root_cause_services = ['checkoutservice', 'currencyservice', 'emailservice', 'productcatalogservice', 'recommendationservice']
possible_root_cause_metrics = ['cpu', 'mem', 'diskio', 'latency', 'socket']
service_dependency_graph = {graph!r}
"""
        self.kernel.run_cell(init_code)

    def _initial_history(self) -> List[Dict[str, str]]:
        return [
            {
                "role": "system",
                "content": f"{EXECUTOR_SYSTEM_PROMPT}\n\n## CURRENT CASE CONTEXT\n\n{self._case_context_prompt()}",
            },
        ]

    def _case_context_prompt(self) -> str:
        files = {
            "metrics": ("metric_path", self.case.metric_path),
            "logs": ("logs_path", self.case.logs_path),
            "traces": ("traces_path", self.case.traces_path),
        }
        lines = [
            "Current case context loaded in the IPython kernel:",
            f"- case_name = {self.case.name!r}",
            f"- case_dir = {self.case.case_dir!r}",
            f"- inject_time = {self.case.inject_time!r}  # Unix seconds",
            "- available telemetry file variables:",
        ]
        for label, (variable, path) in files.items():
            if path:
                lines.append(f"  - {label}: use `{variable}` = {path!r}")
        lines.extend(
            [
                "- service_dependency_graph is already loaded as a Python variable.",
                "- possible_root_cause_services and possible_root_cause_metrics are already loaded as Python variables.",
                "- Use only the listed telemetry paths and in-memory variables for analysis.",
            ]
        )
        return "\n".join(lines)

    @staticmethod
    def _extract_code(response: str) -> str:
        match = CODE_BLOCK_RE.search(response)
        if match:
            return match.group(1).strip()
        stripped = response.strip()
        open_fence = re.match(r"```(?:python)?\s*(.*)", stripped, flags=re.DOTALL | re.IGNORECASE)
        if open_fence:
            code = open_fence.group(1)
            code = re.sub(r"\s*```\s*$", "", code)
            return code.strip()
        return stripped

    @staticmethod
    def _has_forbidden_code(code: str) -> bool:
        forbidden = [
            "matplotlib",
            "seaborn",
            "plt.",
            "subprocess",
            "os.system",
            "shutil.",
            ".to_csv",
            ".to_json",
            ".to_excel",
            "problem.json",
            "%%bash",
        ]
        lowered = code.lower()
        return any(item.lower() in lowered for item in forbidden) or bool(re.search(r"(?m)^\s*!", code))

    @staticmethod
    def _format_error(execution: Any) -> str:
        error = execution.error_in_exec or execution.error_before_exec
        if error is None:
            return "Unknown execution error."
        return "".join(
            traceback.format_exception(
                type(error),
                error,
                error.__traceback__,
            )
        )

    @staticmethod
    def _truncate_result(result: str, max_chars: int = 12000) -> str:
        if len(result) <= max_chars:
            return result
        return result[:max_chars] + "\n\n**Note**: execution output was truncated."

    @staticmethod
    def _continuation_note() -> Dict[str, str]:
        return {
            "role": "user",
            "content": (
                "Continue your code writing process following the rules:\n\n"
                f"{OPENRCA_EXECUTOR_CODE_RULES}\n\n"
                "Response format:\n\n```python\n(YOUR CODE HERE)\n```"
            ),
        }
