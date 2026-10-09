#!/usr/bin/env python3
"""Estimate spoken duration; does not measure footage, pauses, or retention."""

import argparse
import json
import math
from pathlib import Path
import re
import sys


def estimate(text, wpm=150):
    if isinstance(wpm, bool) or not math.isfinite(wpm) or wpm <= 0:
        raise ValueError("wpm must be finite and positive")
    words = len(re.findall(r"\S+", text))
    duration = words / wpm * 60
    if not math.isfinite(duration):
        raise ValueError("duration estimate exceeds numeric range")
    return {"words": words, "wpm": wpm, "estimated_spoken_seconds": duration,
            "notice": "Whitespace-based estimate for supplied spoken text only; add pauses and visuals."
            " Not measured runtime, and less useful for languages without word spacing."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Spoken text file or - for stdin")
    parser.add_argument("--wpm", type=float, default=150)
    args = parser.parse_args()
    try:
        text = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        print(json.dumps(estimate(text, args.wpm), indent=2, allow_nan=False))
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
