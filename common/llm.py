import json
import os
import re
import sys
import time
from typing import Any, Dict, Iterable, List, Optional, Protocol


DEFAULT_LOCAL_MODEL = "/data/models/Qwen3-8B"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class LLMConfigError(RuntimeError):
    pass


class LLMResponseError(RuntimeError):
    pass


class ChatBackend(Protocol):
    def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> str:
        ...


def require_llm_env(
    model_override: Optional[str] = None,
    backend: str = "openai",
    local_model: str = DEFAULT_LOCAL_MODEL,
) -> None:
    if backend == "local":
        if not os.path.isdir(local_model):
            raise LLMConfigError(f"Local model directory does not exist: {local_model}")
        return

    missing = []
    if not (os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENROUTER_API_KEY")):
        missing.append("OPENAI_API_KEY or OPENROUTER_API_KEY")
    if not (
        model_override
        or os.environ.get("OPENAI_MODEL")
        or os.environ.get("OPENROUTER_MODEL")
    ):
        missing.append("OPENAI_MODEL or OPENROUTER_MODEL or --model")
    if missing:
        raise LLMConfigError(
            "Missing LLM configuration: "
            + ", ".join(missing)
            + ". Optional: OPENAI_BASE_URL for OpenAI-compatible endpoints."
        )


def _strip_thinking(text: str) -> str:
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"<\|im_start\|>.*?<\|im_end\|>", "", cleaned, flags=re.DOTALL)
    return cleaned.strip()


def extract_json_object(text: str) -> Dict[str, Any]:
    cleaned = _strip_thinking(text)
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL | re.IGNORECASE)
    if fence:
        cleaned = fence.group(1).strip()

    if not cleaned.startswith("{"):
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            cleaned = cleaned[start : end + 1]

    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        repaired = _repair_truncated_json(cleaned)
        if repaired != cleaned:
            try:
                value = json.loads(repaired)
            except json.JSONDecodeError:
                raise LLMResponseError(f"LLM did not return valid JSON: {exc}\nRaw response:\n{text}") from exc
        else:
            raise LLMResponseError(f"LLM did not return valid JSON: {exc}\nRaw response:\n{text}") from exc

    if not isinstance(value, dict):
        raise LLMResponseError(f"Expected a JSON object, got {type(value).__name__}")
    return value


def _repair_truncated_json(text: str) -> str:
    if '"args"' in text:
        text = text.replace('},{"name"', '}},{"name"')
        text = text.replace('},{"tool_name"', '}},{"tool_name"')
        text = text.replace('},{"tool"', '}},{"tool"')
    # Qwen occasionally emits `"metrics":["a"],["b"]` instead of
    # `"metrics":["a","b"]` when copying evidence strings.
    text = re.sub(r'\]\s*,\s*\[\s*"((?:traces|logs|rankings)"\s*:)', r'],"\1', text)
    text = re.sub(r'"\]\s*,\s*\["', '","', text)
    stack = []
    in_string = False
    escape = False
    output = []
    closers = {"{": "}", "[": "]"}
    expected_openers = {"}": "{", "]": "["}
    for char in text:
        output.append(char)
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char in "{[":
            stack.append(char)
        elif char in expected_openers:
            expected = expected_openers[char]
            if expected in stack:
                inserted = []
                while stack and stack[-1] != expected:
                    inserted.append(closers[stack.pop()])
                if inserted:
                    output[-1:-1] = inserted
                if stack and stack[-1] == expected:
                    stack.pop()
    if in_string:
        output.append('"')
    while stack:
        output.append(closers[stack.pop()])
    return "".join(output)


class OpenAIChatBackend:
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        top_p: float = 0.9,
    ) -> None:
        require_llm_env(model, backend="openai")
        openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        if model:
            self.model = model
        elif openrouter_key and os.environ.get("OPENROUTER_MODEL"):
            self.model = os.environ["OPENROUTER_MODEL"]
        else:
            self.model = os.environ.get("OPENAI_MODEL") or os.environ["OPENROUTER_MODEL"]
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> str:
        from openai import OpenAI

        openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        client_args: Dict[str, Any] = {"api_key": openrouter_key or os.environ["OPENAI_API_KEY"]}
        if openrouter_key:
            client_args["base_url"] = (
                os.environ.get("OPENROUTER_BASE_URL")
                or os.environ.get("OPENAI_BASE_URL")
                or DEFAULT_OPENROUTER_BASE_URL
            )
        elif os.environ.get("OPENAI_BASE_URL"):
            client_args["base_url"] = os.environ["OPENAI_BASE_URL"]
        client = OpenAI(**client_args)

        request = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
        }

        last_error: Optional[Exception] = None
        for attempt in range(3):
            try:
                response = client.chat.completions.create(**request)
                return response.choices[0].message.content or ""
            except Exception as exc:  # pragma: no cover - endpoint-specific failures
                last_error = exc
                if "429" in str(exc) or "rate" in str(exc).lower():
                    time.sleep(2**attempt)
                    continue
                raise
        raise RuntimeError(f"LLM request failed after retries: {last_error}")


class LocalQwenChatBackend:
    def __init__(
        self,
        model_path: str = DEFAULT_LOCAL_MODEL,
        temperature: float = 0.0,
        max_new_tokens: int = 1024,
        top_p: float = 0.9,
        cpu: bool = False,
    ) -> None:
        require_llm_env(backend="local", local_model=model_path)
        self.model_path = model_path
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
        self.top_p = top_p
        self.cpu = cpu
        self._tokenizer = None
        self._model = None

    def _load(self) -> None:
        if self._model is not None and self._tokenizer is not None:
            return

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        device_map = None if self.cpu else "auto"
        dtype = torch.float32 if self.cpu or not torch.cuda.is_available() else torch.bfloat16

        print(f"Loading local model from {self.model_path}", file=sys.stderr)
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            dtype=dtype,
            device_map=device_map,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )
        self._model.eval()

    def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> str:
        self._load()

        import torch

        assert self._tokenizer is not None
        assert self._model is not None

        prompt = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        inputs = self._tokenizer(prompt, return_tensors="pt")
        if not self.cpu:
            inputs = inputs.to(self._model.device)

        temp = self.temperature if temperature is None else temperature
        generation_kwargs = {
            "max_new_tokens": self.max_new_tokens,
            "do_sample": temp > 0,
            "pad_token_id": self._tokenizer.eos_token_id,
        }
        if temp > 0:
            generation_kwargs["temperature"] = temp
            generation_kwargs["top_p"] = self.top_p

        input_tokens = int(inputs["input_ids"].shape[-1])
        free_before_mib = None
        total_mib = None
        if not self.cpu and torch.cuda.is_available():
            torch.cuda.empty_cache()
            free_before, total = torch.cuda.mem_get_info()
            free_before_mib = free_before // (1024 * 1024)
            total_mib = total // (1024 * 1024)

        try:
            with torch.inference_mode():
                output_ids = self._model.generate(**inputs, **generation_kwargs)
        except torch.cuda.OutOfMemoryError as exc:
            if not self.cpu and torch.cuda.is_available():
                torch.cuda.empty_cache()
                free_after, _ = torch.cuda.mem_get_info()
                raise torch.cuda.OutOfMemoryError(
                    f"{exc} prompt_tokens={input_tokens}, max_new_tokens={self.max_new_tokens}, "
                    f"cuda_free_before_mib={free_before_mib}, cuda_free_after_empty_cache_mib={free_after // (1024 * 1024)}, "
                    f"cuda_total_mib={total_mib}"
                ) from exc
            raise

        generated_ids = output_ids[0][inputs["input_ids"].shape[-1] :]
        return self._tokenizer.decode(generated_ids, skip_special_tokens=True).strip()


class LLMClient:
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.0,
        backend: str = "local",
        local_model: str = DEFAULT_LOCAL_MODEL,
        max_new_tokens: int = 1024,
        top_p: float = 0.9,
        cpu: bool = False,
    ) -> None:
        self.backend_name = backend
        if backend == "local":
            self.backend: ChatBackend = LocalQwenChatBackend(
                model_path=local_model,
                temperature=temperature,
                max_new_tokens=max_new_tokens,
                top_p=top_p,
                cpu=cpu,
            )
        elif backend == "openai":
            self.backend = OpenAIChatBackend(
                model=model,
                temperature=temperature,
                max_tokens=max_new_tokens,
                top_p=top_p,
            )
        else:
            raise LLMConfigError(f"Unsupported LLM backend: {backend}. Choose local or openai.")

    def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> str:
        return self.backend.chat(messages, temperature=temperature)

    def json_chat(
        self,
        messages: List[Dict[str, str]],
        required_keys: Iterable[str],
        forbidden_keys: Iterable[str] = (),
    ) -> Dict[str, Any]:
        correction_messages = list(messages)
        last_error = ""
        for _ in range(3):
            raw = self.chat(correction_messages)
            try:
                data = extract_json_object(raw)
            except LLMResponseError as exc:
                last_error = str(exc)
                correction_messages.extend(
                    [
                        {"role": "assistant", "content": raw},
                        {
                            "role": "user",
                            "content": "Return exactly one valid JSON object only.",
                        },
                    ]
                )
                continue

            missing = [key for key in required_keys if key not in data]
            forbidden = [key for key in forbidden_keys if key in data]
            if not missing and not forbidden:
                return data
            last_error = f"Missing keys: {missing}. Forbidden keys present: {forbidden}."
            correction_messages.extend(
                [
                    {"role": "assistant", "content": raw},
                    {
                        "role": "user",
                        "content": (
                            "Return one valid JSON object only. "
                            f"Missing keys: {missing}. Forbidden keys present: {forbidden}."
                        ),
                    },
                ]
            )
        raise LLMResponseError(f"LLM response did not satisfy the required JSON schema. {last_error}")
