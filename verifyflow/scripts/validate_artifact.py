#!/usr/bin/env python3
"""Read-only, bounded validation for one local artifact."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def detect_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix in {".csv", ".tsv"}:
        return "csv"
    return "text"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"artifact is not valid UTF-8 text: {exc}") from exc


def validate_json(path: Path) -> tuple[str, list[str]]:
    value = json.loads(read_text(path))
    if isinstance(value, dict):
        return "object", list(value.keys())
    if isinstance(value, list):
        return "array", []
    return type(value).__name__, []


def validate_csv(path: Path) -> tuple[str, list[str]]:
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter=delimiter))
    if not rows:
        raise ValueError("table is empty")
    width = len(rows[0])
    if width == 0:
        raise ValueError("header row is empty")
    for index, row in enumerate(rows[1:], start=2):
        if len(row) != width:
            raise ValueError(f"row {index} has {len(row)} columns; expected {width}")
    return f"table:{len(rows)-1}-rows", rows[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only validation of one local artifact.")
    parser.add_argument("--path", required=True, help="Local artifact path")
    parser.add_argument("--type", choices=("auto", "file", "dir", "text", "json", "csv"), default="auto")
    parser.add_argument("--min-bytes", type=int, default=0)
    parser.add_argument("--max-bytes", type=int)
    parser.add_argument("--required", action="append", default=[], help="Required JSON key, CSV header, or text substring")
    parser.add_argument("--forbid", action="append", default=[], help="Forbidden text substring")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        return fail(f"path does not exist: {path}")
    if path.is_symlink():
        return fail(f"refusing to validate symlink: {path}")
    if args.min_bytes < 0 or (args.max_bytes is not None and args.max_bytes < 0):
        return fail("byte limits must be non-negative")
    if args.max_bytes is not None and args.min_bytes > args.max_bytes:
        return fail("--min-bytes cannot exceed --max-bytes")

    if path.is_dir():
        if args.type not in {"auto", "dir"}:
            return fail(f"expected a file for type={args.type}, found directory")
        entries = sorted(item.name for item in path.iterdir())
        for required in args.required:
            if required not in entries:
                return fail(f"required directory entry missing: {required}")
        print(f"PASS: directory={path} entries={len(entries)}")
        return 0

    if not path.is_file():
        return fail(f"path is neither a regular file nor directory: {path}")
    if args.type == "dir":
        return fail(f"expected a directory, found file: {path}")

    size = path.stat().st_size
    if size < args.min_bytes:
        return fail(f"size {size} is below minimum {args.min_bytes} bytes")
    if args.max_bytes is not None and size > args.max_bytes:
        return fail(f"size {size} exceeds maximum {args.max_bytes} bytes")

    mode = detect_type(path) if args.type == "auto" else args.type
    try:
        if mode == "json":
            kind, available = validate_json(path)
            for required in args.required:
                if required not in available:
                    return fail(f"required JSON key missing: {required}")
        elif mode == "csv":
            kind, available = validate_csv(path)
            for required in args.required:
                if required not in available:
                    return fail(f"required table header missing: {required}")
        else:
            kind = "file" if mode == "file" else "text"
            text = read_text(path) if (args.required or args.forbid or mode == "text") else ""
            for required in args.required:
                if required not in text:
                    return fail(f"required text not found: {required!r}")
            for forbidden in args.forbid:
                if forbidden in text:
                    return fail(f"forbidden text found: {forbidden!r}")
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as exc:
        return fail(str(exc))

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"PASS: path={path} type={kind} bytes={size} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
