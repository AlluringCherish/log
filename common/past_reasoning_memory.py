from pathlib import Path
from typing import Optional


PAST_REASONING_MEMORY_PLACEHOLDER = "{{PAST_REASONING_MEMORY_EXAMPLES}}"


def load_past_reasoning_memory(path: Optional[str]) -> str:
    if not path:
        return ""

    memory_path = Path(path)
    text = memory_path.read_text(encoding="utf-8").strip()
    return _examples_only(text)


def render_prompt_with_past_reasoning_memory(prompt: str, memory_path: Optional[str]) -> str:
    examples = load_past_reasoning_memory(memory_path)
    return prompt.replace(PAST_REASONING_MEMORY_PLACEHOLDER, examples)


def _examples_only(text: str) -> str:
    example_start = text.find("### Example")
    if example_start >= 0:
        return text[example_start:].strip()
    return text
