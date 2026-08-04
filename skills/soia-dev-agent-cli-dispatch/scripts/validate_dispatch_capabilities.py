#!/usr/bin/env python3
# @created_by claude opus 4.6
# @created_at 2026-08-04 11:43:03
# @modified_by gpt-5.6-sol
# @modified_at 2026-08-04 11:43:03
# @version 0.1.0
# @description Validate the dispatch capability and usage registry without third-party YAML dependencies.
# @changelog Add schema, workflow, executor, and reference-path checks for dispatch-capabilities.yml.
"""Validate dispatch-capabilities.yml and its referenced files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog_lib  # noqa: E402


EXPECTED_EXECUTORS = {
    "codex", "claude", "pi", "agy", "gemini", "kimi", "opencode", "qwen", "qodercli"
}
EXPECTED_WORKFLOWS = {
    "easy-code-and-analysis", "medium-code-and-review",
    "hard-code-review-and-design", "documentation-and-content",
}
REQUIRED_FIELDS = {
    "command", "dispatch_supported", "matrix_supported", "verification_status",
    "prompt_transport", "structured_output", "model_integrity", "usage_evidence",
    "auto_routing", "reference",
}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = catalog_lib.load_catalog(path)
    except (OSError, catalog_lib.CatalogError) as exc:
        return [f"cannot load {path}: {exc}"]

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    skill = data.get("skill")
    if not isinstance(skill, dict):
        errors.append("skill must be a mapping")
    else:
        for field in ("name", "display_name", "version", "purpose", "triggers"):
            if field not in skill:
                errors.append(f"skill: missing field {field}")
        if skill.get("name") != "soia-dev-agent-cli-dispatch":
            errors.append("skill.name must be soia-dev-agent-cli-dispatch")

    usage = data.get("usage")
    if not isinstance(usage, dict):
        errors.append("usage must be a mapping")
    else:
        for field in ("prerequisites", "auto_route", "explicit_dispatch", "verified_pi_example", "receipt_fields"):
            if field not in usage:
                errors.append(f"usage: missing field {field}")

    workflows = data.get("supported_workflows")
    if not isinstance(workflows, list):
        errors.append("supported_workflows must be a list")
    else:
        actual_workflows = {item.get("id") for item in workflows if isinstance(item, dict)}
        missing_workflows = EXPECTED_WORKFLOWS - actual_workflows
        if missing_workflows:
            errors.append(f"missing workflows: {sorted(missing_workflows)}")
        for item in workflows:
            if not isinstance(item, dict):
                errors.append("supported_workflows: each entry must be a mapping")
                continue
            for field in ("id", "label", "complexity", "dispatch_mode", "recommended_executors", "status", "suitable_for", "avoid_for"):
                if field not in item:
                    errors.append(f"workflow {item.get('id')!r}: missing field {field}")

    executors = data.get("executors")
    if not isinstance(executors, dict):
        return errors + ["executors must be a mapping"]

    actual = set(executors)
    missing = EXPECTED_EXECUTORS - actual
    extra = actual - EXPECTED_EXECUTORS
    if missing:
        errors.append(f"missing executors: {sorted(missing)}")
    if extra:
        errors.append(f"unknown executors: {sorted(extra)}")

    root = path.parent.parent
    for name, entry in executors.items():
        if not isinstance(entry, dict):
            errors.append(f"{name}: entry must be a mapping")
            continue
        missing_fields = REQUIRED_FIELDS - set(entry)
        if missing_fields:
            errors.append(f"{name}: missing fields: {sorted(missing_fields)}")
        for field in ("dispatch_supported", "matrix_supported"):
            if not isinstance(entry.get(field), bool):
                errors.append(f"{name}.{field}: must be boolean")
        if not isinstance(entry.get("auto_routing"), list):
            errors.append(f"{name}.auto_routing: must be a list")
        reference = entry.get("reference")
        if not isinstance(reference, str) or not (root / reference).is_file():
            errors.append(f"{name}.reference: missing file {reference!r}")
    return errors


def run_selftest() -> int:
    path = Path(__file__).resolve().parents[1] / "references" / "dispatch-capabilities.yml"
    errors = validate(path)
    print("=== validate_dispatch_capabilities.py selftest ===")
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print(f"[PASS] {len(EXPECTED_EXECUTORS)} executor entries and reference paths are valid")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    path = args.file or Path(__file__).resolve().parents[1] / "references" / "dispatch-capabilities.yml"
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"valid: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
