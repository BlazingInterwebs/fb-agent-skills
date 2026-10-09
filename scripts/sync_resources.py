#!/usr/bin/env python3
"""Bundle canonical shared resources; --check makes no changes."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("audit", "comment", "dm", "group", "human", "plan", "post",
         "presence", "reply", "repurpose", "research", "story", "video")


def expected_resources(root=ROOT):
    for name in NAMES:
        folder = root / "skills" / ("fb-" + name)
        for source in sorted((root / "shared").glob("*.md")):
            yield source, folder / "references" / source.name
        yield root / "LICENSE", folder / "LICENSE"
    for name in ("audit", "research"):
        yield root / "shared" / "compare.py", root / "skills" / ("fb-" + name) / "scripts" / "compare.py"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    mismatches = []
    for source, target in expected_resources():
        if not target.is_file() or source.read_bytes() != target.read_bytes():
            mismatches.append(str(target.relative_to(ROOT)))
            if not args.check:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
    if args.check and mismatches:
        print("Resources out of sync: " + ", ".join(mismatches), file=sys.stderr)
        return 1
    print("Shared resources verified" if args.check else "Shared resources bundled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
