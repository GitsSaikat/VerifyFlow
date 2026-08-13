#!/usr/bin/env python3
"""Read-only, bounded directory or file summary; never follows symlinks."""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from collections import Counter
from pathlib import Path


def classify(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_dir():
        return "directory"
    if path.is_file():
        return "file"
    return "other"


def file_digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Print a bounded, read-only summary of a local path.")
    parser.add_argument("--path", default=".", help="Path to summarize")
    parser.add_argument("--max-entries", type=int, default=100, help="Maximum immediate directory entries to display")
    parser.add_argument("--hash-file", action="store_true", help="Include SHA-256 only when the target is one regular file")
    args = parser.parse_args()

    if args.max_entries < 1:
        print("ERROR: --max-entries must be at least 1", file=sys.stderr)
        return 2
    path = Path(args.path)
    if not path.exists() and not path.is_symlink():
        print(f"ERROR: path does not exist: {path}", file=sys.stderr)
        return 1

    kind = classify(path)
    print(f"path: {path}")
    print(f"type: {kind}")
    if path.is_symlink():
        print(f"target: {os.readlink(path)}")
        print("note: symlink target was not traversed")
        return 0
    if path.is_file():
        print(f"bytes: {path.stat().st_size}")
        if args.hash_file:
            print(f"sha256: {file_digest(path)}")
        return 0
    if not path.is_dir():
        return 0

    entries = sorted(path.iterdir(), key=lambda item: item.name.lower())
    counts = Counter(classify(item) for item in entries)
    print(f"entries: {len(entries)}")
    print("counts: " + ", ".join(f"{name}={counts[name]}" for name in sorted(counts)))
    shown = entries[:args.max_entries]
    for item in shown:
        item_kind = classify(item)
        detail = f"{item.stat().st_size} bytes" if item_kind == "file" else (f"-> {os.readlink(item)}" if item_kind == "symlink" else "")
        print(f"- {item_kind}: {item.name}" + (f" ({detail})" if detail else ""))
    if len(entries) > len(shown):
        print(f"note: {len(entries)-len(shown)} additional immediate entries not shown")
    print("note: summary is read-only, non-recursive, and does not follow symlinks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
