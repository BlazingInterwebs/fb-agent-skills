#!/usr/bin/env python3
"""Return original text and contextual editorial flags; never rewrite or score."""

import argparse
import json
from pathlib import Path
import re
import sys

RULES = (
    ("generic_opening", re.compile(r"\bin (?:today's|this) (?:fast[- ]paced|ever[- ]changing) world\b", re.I),
     "Check whether this framing adds context or matches the supplied voice."),
    ("unsupported_certainty", re.compile(r"\b(?:guaranteed results|guaranteed growth|everyone will|always works)\b", re.I),
     "Check scope and evidence; do not replace certainty with invented proof."),
    ("engagement_request", re.compile(r"\b(?:like and share|tag \d+ friends|comment yes|agree\?|thoughts\?)", re.I),
     "Review purpose in context. A genuine question may be appropriate."),
    ("inspect_character", re.compile("[\u200b\ufeff\u00ad]"),
     "Inspect the character in context; do not remove meaningful language characters automatically."),
)


def review(text):
    flags = []
    for kind, pattern, reason in RULES:
        for match in pattern.finditer(text):
            flags.append({"kind": kind, "start": match.start(), "end": match.end(),
                          "excerpt": match.group(), "reason": reason})
    return {"text": text, "flags": flags,
            "notice": "Contextual editorial review only; no AI authorship or growth prediction."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="UTF-8 text file, or - for stdin")
    args = parser.parse_args()
    try:
        text = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        print(json.dumps(review(text), ensure_ascii=False, indent=2))
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
