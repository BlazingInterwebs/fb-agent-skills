#!/usr/bin/env python3
"""Install selected self-contained skills without overwriting any existing path."""

import argparse
import hashlib
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from sync_resources import NAMES
from validate import validate_repo


def install(destination, names, dry_run=False):
    destination = Path(destination).expanduser().absolute()
    if not names or len(names) != len(set(names)) or any(name not in ("fb-" + n for n in NAMES) for name in names):
        raise ValueError("choose unique known fb-* skills")
    issues = validate_repo()
    if issues:
        raise ValueError("source validation failed: " + "; ".join(issues))
    for name in names:
        target = destination / name
        if target.exists() or target.is_symlink():
            raise FileExistsError("refusing to overwrite " + str(target))
    if dry_run:
        return [{"name": name, "destination": str(destination / name), "status": "dry-run"} for name in names]
    destination.mkdir(parents=True, exist_ok=True)
    receipt = []
    for name in names:
        source = ROOT / "skills" / name
        target = destination / name
        # copytree creates the destination exclusively; a racing existing path is not replaced.
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        count = 0
        for original in source.rglob("*"):
            if original.is_file() and "__pycache__" not in original.parts and original.suffix != ".pyc":
                copy = target / original.relative_to(source)
                if hashlib.sha256(original.read_bytes()).digest() != hashlib.sha256(copy.read_bytes()).digest():
                    raise OSError("verification failed: " + str(copy))
                count += 1
        receipt.append({"name": name, "destination": str(target), "files_verified": count, "status": "installed"})
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, help="explicit host-discovered skill directory")
    parser.add_argument("--skills", nargs="+", default=["fb-" + name for name in NAMES])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        import json
        print(json.dumps(install(args.destination, args.skills, args.dry_run), indent=2))
    except (OSError, ValueError) as exc:
        print(str(exc) + ". If a copy failed, inspect any partial newly created folders before retrying; existing skills were not replaced.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
