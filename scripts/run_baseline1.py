from __future__ import annotations

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baseline1 experiment entry."""

from pathlib import Path
import sys

EXPERIMENT_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(EXPERIMENT_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_ROOT_FOR_IMPORTS))

import argparse
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from spec_abduction.acsl import GeneratedCodeError, add_probe_markers, validate_generated_code
from spec_abduction.autobench import discover_cases
from spec_abduction.config import DEFAULT_AUTOBENCH_DIR, DEFAULT_CONFIG, EXPERIMENT_ROOT, load_model_config
from spec_abduction.llm import LLMClient, extract_code_response
from spec_abduction.logging import RunLogger
from spec_abduction.outputs import (
    case_record,
    resumed_record,
    save_failed_file,
    save_failure_wp_output,
    successful_file_path,
)
from spec_abduction.prompts.baseline1 import build_direct_generation_prompt, build_prompt
from spec_abduction.types import AttemptRecord, Case
from spec_abduction.wp import attempt_status, result_score, run_wp


DEFAULT_OUT_ROOT = EXPERIMENT_ROOT / "results" / "baseline1_llm_direct"

"""解析命令行参数。

    这个实验脚本默认即可在 `spec_generation_abduction` 目录内运行。
    常用参数：
    - `--datasets` 控制跑哪些 AutoBench 子数据集；
    - `--attempts` 控制每题最多生成几次；
    - `--resume` 支持断点续跑；
    - `--overwrite` 用于完全清空旧结果重新跑。
    """
def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Baseline1 direct LLM ACSL generation over AutoBench.")
    parser.add_argument("--autobench-dir", default=str(DEFAULT_AUTOBENCH_DIR), help="Local AutoBench root.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="models_config.yaml.")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT), help="Output root.")
    parser.add_argument(
        "--datasets",
        default="SyGuS,frama-c-problem,svcomp,46_fib",
        help="Comma-separated dataset names, or all.",
    )
    parser.add_argument("--model", "--override-model", dest="model", default="gpt-4o", help="Model name in config.")
    parser.add_argument("--override-base-url", help="Runtime base_url override.")
    parser.add_argument("--attempts", type=int, default=5, help="Independent LLM generations per case.")
    parser.add_argument("--limit", type=int, default=0, help="Global case limit; 0 means no limit.")
    parser.add_argument("--dataset-limit", type=int, default=0, help="Per-dataset case limit; 0 means no limit.")
    parser.add_argument("--temperature", type=float, default=0.4, help="LLM temperature.")
    parser.add_argument("--max-tokens", type=int, default=8192, help="LLM max completion tokens.")
    parser.add_argument("--frama-c", default="frama-c", help="frama-c executable.")
    parser.add_argument("--wp-timeout", type=int, default=8, help="WP prover timeout.")
    parser.add_argument("--provers", default="Alt-Ergo,Z3", help="WP prover list.")
    parser.add_argument("--resume", action="store_true", help="Skip cases with existing final output.")
    parser.add_argument("--overwrite", action="store_true", help="Remove out-root before running.")
    parser.add_argument("--dry-run", action="store_true", help="Print selected cases without LLM/WP.")
    parser.add_argument("--add-probe-markers", action="store_true", help="Add plain PROBE_HERE comments for later probing.")
    return parser.parse_args(argv)

"""对单个题目的某个 attempt 调用 LLM 生成完整 C+ACSL。"""
def generate_code(client: LLMClient, case: Case, attempt: int, temperature: float, max_tokens: int) -> str:

    source_code = case.source_path.read_text(encoding="utf-8", errors="replace")
    raw = client.chat(build_direct_generation_prompt(case, source_code, attempt), temperature, max_tokens, f"{case.dataset}_{case.filename}_attempt{attempt}")
    code = extract_code_response(raw)
    if not code:
        raise ValueError("LLM returned empty code")
    validate_generated_code(source_code, code)
    return code if code.endswith("\n") else code + "\n"

"""
运行单个题目。
流程：
    1. 如果 `--resume` 且已有精简输出，则直接读取旧结果；
    2. 在临时目录中创建每次 attempt 的 C 文件和 WP 日志；
    3. 最多尝试 `--attempts` 次 LLM 生成；
    4. 每次生成后立即运行 WP;
    5. 如果某次 Pass,提前停止该题;
    6. Pass 时保存通过文件；否则保存分数最高的失败 attempt 的 WP 输出。
"""
def run_case(args: argparse.Namespace, client: LLMClient, case: Case, out_root: Path) -> Dict[str, Any]:

    if args.resume:
        record = resumed_record(case, out_root)
        if record is not None:
            # 断点续跑：已有精简输出不重复消耗 LLM 调用和 WP 时间。
            return record

    best: Optional[AttemptRecord] = None
    successful_file = ""
    with tempfile.TemporaryDirectory(prefix="baseline1_") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        generated_dir = temp_dir / "generated_specs"
        wp_dir = temp_dir / "wp_logs"
        generated_dir.mkdir(parents=True, exist_ok=True)
        wp_dir.mkdir(parents=True, exist_ok=True)
        for attempt in range(1, args.attempts + 1):
            generated_file = generated_dir / f"attempt_{attempt:02d}.c"
            try:
                code = generate_code(client, case, attempt, args.temperature, args.max_tokens)
                if args.add_probe_markers:
                    # 默认 baseline1 不插 probe marker；只有为后续实验准备输入时才开启。
                    code = add_probe_markers(code)
                generated_file.write_text(code, encoding="utf-8")
                wp = run_wp(args.frama_c, generated_file, wp_dir, f"attempt_{attempt:02d}", args.wp_timeout, args.provers)
                record = AttemptRecord(
                    case.dataset,
                    case.filename,
                    attempt,
                    str(generated_file),
                    wp.result_type,
                    wp.stdout_path,
                    wp.stderr_path,
                    attempt_status(wp.result_type),
                    result_score(wp.result_type),
                    wp.stdout,
                    wp.stderr,
                    wp.command,
                    code,
                )
            except Exception as exc:
                # 单个 attempt 出错不终止整个题目；继续尝试下一次生成。
                generated_code = exc.code if isinstance(exc, GeneratedCodeError) else generated_file.read_text(encoding="utf-8", errors="replace") if generated_file.exists() else ""
                record = AttemptRecord(
                    case.dataset,
                    case.filename,
                    attempt,
                    str(generated_file),
                    "Error",
                    "",
                    "",
                    "Error",
                    -1.0,
                    "",
                    "",
                    [],
                    generated_code,
                    f"{type(exc).__name__}: {exc}",
                )
            if best is None or record.score > best.score:
                best = record
            if record.status == "Pass":
                # baseline1 的成功定义：N 次独立生成中任意一次通过即可。
                target = successful_file_path(out_root, case)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(generated_file, target)
                successful_file = str(target)
                break
    failure_wp_output = ""
    failed_file = ""
    if best and best.status != "Pass":
        failed_file = save_failed_file(out_root, case, best)
        failure_wp_output = save_failure_wp_output(out_root, case, best)
    return case_record(case, best, False, successful_file, failed_file, failure_wp_output)

"""
写 baseline1 的最终统计报告。
最终只写 Markdown summary,通过文件和失败 WP 输出由 `run_case` 按需保存。
"""
def write_reports(out_root: Path, records: List[Dict[str, Any]]) -> None:

    status_counts = Counter(record["final_status"] for record in records)
    dataset_counts: Dict[str, Counter] = {}
    for record in records:
        dataset_counts.setdefault(record["dataset"], Counter())[record["final_status"]] += 1
    lines = ["# Baseline1 Direct LLM Spec Generation", "", "## Overall", "", "| Status | Count |", "| --- | ---: |"]
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count} |")
    lines.extend(["", "## By Dataset", "", "| Dataset | Pass | Fail | Invalid | Error | Total |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for dataset, counter in sorted(dataset_counts.items()):
        total = sum(counter.values())
        lines.append(f"| {dataset} | {counter.get('Pass', 0)} | {counter.get('Fail', 0)} | {counter.get('Invalid', 0)} | {counter.get('Error', 0)} | {total} |")
    lines.extend(["", "## Per Case", "", "| Dataset | File | Status | Best Attempt | Best Result | C File | WP Output |", "| --- | --- | --- | ---: | --- | --- | --- |"])
    for record in records:
        c_file = record.get("successful_saved_file") or record.get("failed_saved_file", "")
        wp_output = record.get("failure_wp_output", "")
        lines.append(f"| {record['dataset']} | {record['filename']} | {record['final_status']} | {record.get('best_attempt', '')} | {record.get('best_result_type', '')} | {c_file} | {wp_output} |")
    (out_root / "baseline1_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def clean_output(out_root: Path) -> None:
    for directory_name in ("successful_files", "failed_cases", "failed_files", "wp_outputs", "generated_specs", "wp_logs", "cases", "llm_logs", "best_files"):
        directory = out_root / directory_name
        if directory.exists():
            shutil.rmtree(directory)
    for file_name in ("baseline1_summary.json", "baseline1_results.jsonl", "baseline1_summary.csv", "baseline1_console.txt"):
        file_path = out_root / file_name
        if file_path.exists():
            file_path.unlink()


def main(argv: Optional[Sequence[str]] = None) -> int:
    """脚本入口。"""

    args = parse_args(argv)
    autobench_dir = Path(args.autobench_dir).resolve()
    out_root = Path(args.out_root).resolve()
    cases = discover_cases(autobench_dir, args.datasets, args.dataset_limit, args.limit)
    if args.dry_run:
        # dry-run 只做数据集枚举，不调用 LLM，也不跑 WP。
        print(f"Selected {len(cases)} case(s)")
        for dataset, count in sorted(Counter(case.dataset for case in cases).items()):
            print(f"{dataset}: {count}")
        return 0
    if args.overwrite and out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    if not args.resume:
        clean_output(out_root)
    with RunLogger(out_root / "baseline1_console.txt") as logger:
        client = LLMClient(load_model_config(Path(args.config).resolve(), args.model, args.override_base_url), logger.log)
        records: List[Dict[str, Any]] = []
        for index, case in enumerate(cases, 1):
            logger.log(f"[{index}/{len(cases)}] baseline1 {case.dataset}/{case.filename}")
            records.append(run_case(args, client, case, out_root))
        write_reports(out_root, records)
        logger.log(f"Summary: {out_root / 'baseline1_summary.md'}")
        logger.log(f"Successful files: {out_root / 'successful_files'}")
        logger.log(f"Failed cases: {out_root / 'failed_cases'}")
        logger.log(f"Console log: {out_root / 'baseline1_console.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
