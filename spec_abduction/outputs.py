from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Optional

from .types import AttemptRecord, Case


def successful_file_path(out_root: Path, case: Case) -> Path:
    """最终保存通过文件的位置。"""

    return out_root / "successful_files" / case.dataset / case.filename


def failed_case_dir(out_root: Path, case: Case) -> Path:
    """最终保存未通过题输出的 case 目录。"""

    return out_root / "failed_cases" / case.dataset / Path(case.filename).stem


def failure_wp_output_path(out_root: Path, case: Case) -> Path:
    """最终保存失败题 WP 输出的位置。"""

    return failed_case_dir(out_root, case) / "wp.txt"


def failed_file_path(out_root: Path, case: Case) -> Path:
    """最终保存未通过题最佳失败 C 文件的位置。"""

    return failed_case_dir(out_root, case) / case.filename


def parse_metadata_line(text: str, name: str) -> str:
    """从已保存的 WP 输出文件头部读取 resume 所需的简单元数据。"""

    match = re.search(rf"^{re.escape(name)}: (.*)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def resumed_record(case: Case, out_root: Path) -> Optional[Dict[str, Any]]:
    """根据精简输出目录判断一个 case 是否可 resume。"""

    success_file = successful_file_path(out_root, case)
    if success_file.exists():
        return {
            "dataset": case.dataset,
            "filename": case.filename,
            "source_path": str(case.source_path),
            "final_status": "Pass",
            "overall_success": True,
            "best_attempt": "",
            "best_result_type": "Pass",
            "successful_saved_file": str(success_file),
            "failed_saved_file": "",
            "failure_wp_output": "",
            "skipped_existing": True,
        }
    failure_output = failure_wp_output_path(out_root, case)
    failed_file = failed_file_path(out_root, case)
    if failure_output.exists() and failed_file.exists():
        text = failure_output.read_text(encoding="utf-8", errors="replace")
        status = parse_metadata_line(text, "Final status") or "Fail"
        result_type = parse_metadata_line(text, "Best result") or status
        attempt = parse_metadata_line(text, "Best attempt")
        return {
            "dataset": case.dataset,
            "filename": case.filename,
            "source_path": str(case.source_path),
            "final_status": status,
            "overall_success": False,
            "best_attempt": attempt,
            "best_result_type": result_type,
            "successful_saved_file": "",
            "failed_saved_file": str(failed_file),
            "failure_wp_output": str(failure_output),
            "skipped_existing": True,
        }
    return None


def case_record(
    case: Case,
    best: Optional[AttemptRecord],
    skipped: bool,
    successful_file: str = "",
    failed_file: str = "",
    failure_wp_output: str = "",
) -> Dict[str, Any]:
    """生成最终逐题汇总记录。

    这条记录只写入最终 Markdown summary。
    """

    return {
        "dataset": case.dataset,
        "filename": case.filename,
        "source_path": str(case.source_path),
        "final_status": best.status if best else "Error",
        "overall_success": bool(best and best.status == "Pass"),
        "best_attempt": best.attempt if best else None,
        "best_result_type": best.wp_result_type if best else None,
        "successful_saved_file": successful_file,
        "failed_saved_file": failed_file,
        "failure_wp_output": failure_wp_output,
        "skipped_existing": skipped,
    }


def save_failed_file(out_root: Path, case: Case, best: AttemptRecord) -> str:
    """把未通过题目的最佳失败 C 文件写入最终目录。"""

    path = failed_file_path(out_root, case)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(best.code if best.code.endswith("\n") else best.code + "\n", encoding="utf-8")
    return str(path)


def save_failure_wp_output(out_root: Path, case: Case, best: AttemptRecord) -> str:
    """把未通过题目的最佳失败 WP 输出写成一个文本文件。"""

    path = failure_wp_output_path(out_root, case)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"Dataset: {case.dataset}",
        f"File: {case.filename}",
        f"Source: {case.source_path}",
        f"Final status: {best.status}",
        f"Best attempt: {best.attempt}",
        f"Best result: {best.wp_result_type}",
        "",
        "Command:",
        " ".join(best.wp_command or []),
    ]
    if best.error:
        lines.extend(["", "Attempt error:", best.error])
    lines.extend(["", "WP stdout:", best.wp_stdout or ""])
    lines.extend(["", "WP stderr:", best.wp_stderr or ""])
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return str(path)

