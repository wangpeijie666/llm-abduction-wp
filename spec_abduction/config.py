from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTOBENCH_DIR = EXPERIMENT_ROOT / "data" / "AutoBench"
DEFAULT_CONFIG = EXPERIMENT_ROOT / "configs" / "models_config.yaml"


@dataclass
class ModelConfig:
    """一次 LLM 调用所需的模型配置。

    `models_config.yaml` 中通常包含模板和模型映射，这里会解析成这个更直接的结构。
    `params` 保留 timeout 等额外配置项，便于不改代码地调整 provider 行为。
    """

    model_name: str
    platform: str
    api_key: str
    base_url: str
    params: Dict[str, Any]


def load_model_config(config_path: Path, model_name: str, override_base_url: Optional[str]) -> ModelConfig:
    """从本地 YAML 配置中解析模型信息。

    配置格式沿用 AutoSpec 的 `models_config.yaml`：
    - `ConfigTemplates` 定义 provider/base_url/api_key/api_key_env 等模板；
    - `ModelMap` 把模型名映射到模板；
    - API key 可以直接写在 `api_key`，也可以从 `api_key_env` 指定的环境变量读取。
    """

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    model_map = data.get("ModelMap", {})
    templates = data.get("ConfigTemplates", {})
    if model_name not in model_map:
        raise ValueError(f"Model `{model_name}` not found in {config_path}. Available: {list(model_map)}")
    model_entry = dict(model_map[model_name] or {})
    template_id = model_entry.pop("template_id")
    template = dict(templates[template_id] or {})
    merged = {**template, **model_entry}
    api_key_env = merged.get("api_key_env", "OPENAI_API_KEY")
    api_key = merged.get("api_key") or os.getenv(api_key_env)
    if not api_key:
        # 明确报出缺失的认证配置，避免 LLM 调用时才得到不清楚的鉴权错误。
        raise EnvironmentError(
            f"Set `api_key` in {config_path} or environment variable `{api_key_env}` for model `{model_name}`"
        )
    base_url = override_base_url or merged.get("base_url", "")
    params = {key: value for key, value in merged.items() if key not in {"platform", "api_key", "api_key_env", "base_url"}}
    return ModelConfig(
        model_name=model_name,
        platform=str(merged.get("platform", "")),
        api_key=api_key,
        base_url=str(base_url),
        params=params,
    )
