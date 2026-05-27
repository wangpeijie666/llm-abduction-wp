from __future__ import annotations

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baseline2 experiment entry."""

from pathlib import Path
import sys

EXPERIMENT_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(EXPERIMENT_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_ROOT_FOR_IMPORTS))

import argparse
import json
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
from spec_abduction.prompts.baseline2 import build_feedback_prompt, feedback_entry
from spec_abduction.types import AttemptRecord, Case, WPResult
from spec_abduction.wp import attempt_status, result_score, run_wp


DEFAULT_OUT_ROOT = EXPERIMENT_ROOT / "results" / "baseline2_feedback"
FEEDBACK_CHAR_LIMIT = 12000


def prompt_log_path(out_root: Path, case: Case, attempt: int) -> Path:
    return out_root / "prompt_logs" / case.dataset / Path(case.filename).stem / f"round_{attempt:02d}_prompt.json"


def save_prompt_log(path: Path, case: Case, attempt: int, messages: List[Dict[str, str]]) -> None:
    user_payload: Dict[str, Any] = {}
    for message in messages:
        if message.get("role") != "user":
            continue
        try:
            parsed = json.loads(message.get("content", ""))
        except json.JSONDecodeError:
            parsed = {}
        if isinstance(parsed, dict):
            user_payload = parsed
        break
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "dataset": case.dataset,
                "filename": case.filename,
                "attempt": attempt,
                "messages": messages,
                "user_payload": user_payload,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


"""解析 baseline2 命令行参数。"""
def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Baseline2 feedback-guided LLM ACSL generation over AutoBench.")
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
    parser.add_argument("--attempts", type=int, default=5, help="Feedback repair rounds per case.")
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

"""调用 LLM 生成或修复完整 C+ACSL。"""
def generate_code(
    client: LLMClient,
    case: Case,
    attempt: int,
    temperature: float,
    max_tokens: int,
    previous_code: str,
    verifier_feedback: Optional[Dict[str, Any]],
    prompt_log_file: Optional[Path],
) -> str:

    source_code = case.source_path.read_text(encoding="utf-8", errors="replace")
    messages = build_feedback_prompt(case, source_code, attempt, previous_code, verifier_feedback)
    if prompt_log_file is not None:
        save_prompt_log(prompt_log_file, case, attempt, messages)
    raw = client.chat(messages, temperature, max_tokens, f"{case.dataset}_{case.filename}_round{attempt}")
    code = extract_code_response(raw)
    if not code:
        raise ValueError("LLM returned empty code")
    validate_generated_code(source_code, code)
    return code if code.endswith("\n") else code + "\n"

"""把 WP 结果整理成 attempt record。"""
def make_attempt_record(case: Case, attempt: int, generated_file: Path, code: str, wp: WPResult) -> AttemptRecord:

    return AttemptRecord(
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

"""运行单个 baseline2 case。"""
def run_case(args: argparse.Namespace, client: LLMClient, case: Case, out_root: Path) -> Dict[str, Any]:

    if args.resume:
        record = resumed_record(case, out_root)
        if record is not None:
            return record

    best: Optional[AttemptRecord] = None
    successful_file = ""
    previous_code = ""
    previous_feedback: Optional[Dict[str, Any]] = None
    with tempfile.TemporaryDirectory(prefix="baseline2_") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        generated_dir = temp_dir / "generated_specs"
        wp_dir = temp_dir / "wp_logs"
        generated_dir.mkdir(parents=True, exist_ok=True)
        wp_dir.mkdir(parents=True, exist_ok=True)
        for attempt in range(1, args.attempts + 1):
            generated_file = generated_dir / f"round_{attempt:02d}.c"
            try:
                code = generate_code(
                    client,
                    case,
                    attempt,
                    args.temperature,
                    args.max_tokens,
                    previous_code,
                    previous_feedback,
                    prompt_log_path(out_root, case, attempt),
                )
                if args.add_probe_markers:
                    code = add_probe_markers(code)
                generated_file.write_text(code, encoding="utf-8")
                wp = run_wp(args.frama_c, generated_file, wp_dir, f"round_{attempt:02d}", args.wp_timeout, args.provers)
                record = make_attempt_record(case, attempt, generated_file, code, wp)
            except Exception as exc:
                code = exc.code if isinstance(exc, GeneratedCodeError) else generated_file.read_text(encoding="utf-8", errors="replace") if generated_file.exists() else previous_code
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
                    code,
                    f"{type(exc).__name__}: {exc}",
                )
            if best is None or record.score > best.score:
                best = record
            if record.status == "Pass":
                target = successful_file_path(out_root, case)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(generated_file, target)
                successful_file = str(target)
                break
            previous_code = record.code
            previous_feedback = feedback_entry(record)
    failure_wp_output = ""
    failed_file = ""
    if best and best.status != "Pass":
        failed_file = save_failed_file(out_root, case, best)
        failure_wp_output = save_failure_wp_output(out_root, case, best)
    return case_record(case, best, False, successful_file, failed_file, failure_wp_output)

"""写 baseline2 的最终 Markdown summary。"""
def write_reports(out_root: Path, records: List[Dict[str, Any]]) -> None:

    status_counts = Counter(record["final_status"] for record in records)
    dataset_counts: Dict[str, Counter] = {}
    for record in records:
        dataset_counts.setdefault(record["dataset"], Counter())[record["final_status"]] += 1
    lines = ["# Baseline2 Feedback-Guided LLM Spec Generation", "", "## Overall", "", "| Status | Count |", "| --- | ---: |"]
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count} |")
    lines.extend(["", "## By Dataset", "", "| Dataset | Pass | Fail | Invalid | Error | Total |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for dataset, counter in sorted(dataset_counts.items()):
        total = sum(counter.values())
        lines.append(f"| {dataset} | {counter.get('Pass', 0)} | {counter.get('Fail', 0)} | {counter.get('Invalid', 0)} | {counter.get('Error', 0)} | {total} |")
    lines.extend(["", "## Per Case", "", "| Dataset | File | Status | Best Round | Best Result | C File | WP Output |", "| --- | --- | --- | ---: | --- | --- | --- |"])
    for record in records:
        c_file = record.get("successful_saved_file") or record.get("failed_saved_file", "")
        wp_output = record.get("failure_wp_output", "")
        lines.append(f"| {record['dataset']} | {record['filename']} | {record['final_status']} | {record.get('best_attempt', '')} | {record.get('best_result_type', '')} | {c_file} | {wp_output} |")
    (out_root / "baseline2_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

"""清理 baseline2 旧输出和早期兼容目录。"""
def clean_output(out_root: Path) -> None:

    for directory_name in ("successful_files", "failed_cases", "failed_files", "wp_outputs", "generated_specs", "wp_logs", "cases", "llm_logs", "best_files", "prompt_logs"):
        directory = out_root / directory_name
        if directory.exists():
            shutil.rmtree(directory)
    for file_name in ("baseline2_summary.md", "baseline2_console.txt", "baseline2_summary.json", "baseline2_results.jsonl", "baseline2_summary.csv"):
        file_path = out_root / file_name
        if file_path.exists():
            file_path.unlink()

"""脚本入口。"""
def main(argv: Optional[Sequence[str]] = None) -> int:
    
    args = parse_args(argv)
    autobench_dir = Path(args.autobench_dir).resolve()
    out_root = Path(args.out_root).resolve()
    cases = discover_cases(autobench_dir, args.datasets, args.dataset_limit, args.limit)
    if args.dry_run:
        print(f"Selected {len(cases)} case(s)")
        for dataset, count in sorted(Counter(case.dataset for case in cases).items()):
            print(f"{dataset}: {count}")
        return 0
    if args.overwrite and out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    if not args.resume:
        clean_output(out_root)
    with RunLogger(out_root / "baseline2_console.txt") as logger:
        client = LLMClient(load_model_config(Path(args.config).resolve(), args.model, args.override_base_url), logger.log)
        records: List[Dict[str, Any]] = []
        for index, case in enumerate(cases, 1):
            logger.log(f"[{index}/{len(cases)}] baseline2 {case.dataset}/{case.filename}")
            records.append(run_case(args, client, case, out_root))
        write_reports(out_root, records)
        logger.log(f"Summary: {out_root / 'baseline2_summary.md'}")
        logger.log(f"Successful files: {out_root / 'successful_files'}")
        logger.log(f"Failed cases: {out_root / 'failed_cases'}")
        logger.log(f"Console log: {out_root / 'baseline2_console.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
