from __future__ import annotations

from pathlib import Path


class RunLogger:
    """同时写控制台和文本文件的运行日志。"""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.handle = path.open("a", encoding="utf-8", buffering=1)

    def log(self, message: str) -> None:
        print(message, flush=True)
        self.handle.write(message + "\n")

    def close(self) -> None:
        self.handle.close()

    def __enter__(self) -> "RunLogger":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

