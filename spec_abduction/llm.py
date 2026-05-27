from __future__ import annotations

import datetime as dt
import json
import re
from typing import Any, Callable, Dict, List

from .config import ModelConfig


class LLMClient:
    """OpenAI-compatible LLM client。

    这里没有复用 AutoSpec 的 BaseChatClass，而是直接使用 openai SDK。
    这样新实验目录可以独立运行，只要安装 `openai` 和配置好 base_url/api_key 即可。
    """

    def __init__(self, config: ModelConfig, log: Callable[[str], None] = print) -> None:
        self.config = config
        self.call_index = 0
        self.log = log
        try:
            import openai
        except Exception as exc:
            raise RuntimeError(f"openai package is not available: {exc}") from exc
        self.openai = openai
        self.client = openai.OpenAI(api_key=config.api_key, base_url=config.base_url) if hasattr(openai, "OpenAI") else None
        if self.client is None:
            # 兼容 openai==0.x 的旧接口；新版本优先走 OpenAI() client。
            openai.api_key = config.api_key
            if config.base_url:
                openai.api_base = config.base_url

    def chat(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int, purpose: str) -> str:
        """调用 LLM 并返回文本内容。

        baseline1 的最终输出保持精简，不持久化 prompt/response 日志。
        失败时继续抛异常，由上层把该 attempt 记为 Error。
        """

        self.call_index += 1
        self.log(f"[{dt.datetime.now().strftime('%H:%M:%S')}] LLM start {purpose}")
        try:
            if self.client is not None:
                # openai>=1.x 调用路径。
                response = self.client.chat.completions.create(
                    model=self.config.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=self.config.params.get("timeout", 300),
                )
                content = response.choices[0].message.content or ""
            else:
                # openai==0.x 调用路径。
                response = self.openai.ChatCompletion.create(
                    model=self.config.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    request_timeout=self.config.params.get("timeout", 300),
                )
                content = response["choices"][0]["message"]["content"]
            self.log(f"[{dt.datetime.now().strftime('%H:%M:%S')}] LLM done {purpose}, chars={len(content)}")
            return content
        except Exception as exc:
            self.log(f"[{dt.datetime.now().strftime('%H:%M:%S')}] LLM error {purpose}: {type(exc).__name__}: {exc}")
            raise


def parse_json_object(text: str) -> Dict[str, Any]:
    """尽量从 LLM 输出中解析 JSON object。

    LLM 偶尔会包一层 ```json fence```，或在 JSON 前后添加少量文字。
    baseline1 prompt 要求 JSON-only，但这里仍做容错，减少格式噪声导致的失败。
    """

    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[A-Za-z0-9_-]*\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        parsed = json.loads(cleaned)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        pass
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start >= 0 and end > start:
        parsed = json.loads(cleaned[start : end + 1])
        return parsed if isinstance(parsed, dict) else {}
    return {}


def strip_markdown_fence(text: str) -> str:
    """移除 LLM 可能返回的 Markdown 代码块外壳。"""

    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```[A-Za-z0-9_-]*\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def extract_code_response(raw: str) -> str:
    """从 LLM 响应中提取完整 C 代码。

    优先读取 JSON 字段 `code` / `annotated_code`；
    如果解析失败，则把整段响应当作代码处理。这是为了兼容偶发的非 JSON 输出。
    """

    obj = parse_json_object(raw)
    code = str(obj.get("code") or obj.get("annotated_code") or "").strip()
    return strip_markdown_fence(code if code else raw)

