#!/usr/bin/env python3
"""Normalize supplied observations and compare against same-account medians."""

import argparse
import csv
from datetime import datetime
import io
import json
import math
from pathlib import Path
import statistics
import sys

REQUIRED = ("account", "post_id", "surface", "format", "visibility", "distribution",
            "metric", "unit", "definition", "value", "age_hours", "source_url", "observed_at")
COHORT = ("account", "surface", "format", "visibility", "distribution", "metric", "unit", "definition")
UNITS = ("count", "seconds", "fraction", "percent")


def number(value, field, missing=False):
    if value is None or value == "":
        if missing:
            return None
        raise ValueError(field + " is missing")
    if isinstance(value, bool):
        raise ValueError(field + " must be numeric, not boolean")
    try:
        result = float(value)
    except (ValueError, TypeError):
        raise ValueError(field + " must be numeric") from None
    if not math.isfinite(result) or result < 0:
        raise ValueError(field + " must be finite and nonnegative")
    return result


def normalize(rows):
    if not isinstance(rows, list):
        raise ValueError("JSON input must be an array of observations")
    normalized = []
    seen = set()
    for index, raw in enumerate(rows, 1):
        if not isinstance(raw, dict) or any(field not in raw for field in REQUIRED):
            raise ValueError("row %d must contain all required fields" % index)
        row = dict(raw)
        for field in REQUIRED:
            if field in ("value", "age_hours"):
                continue
            if not isinstance(row[field], str) or not row[field].strip():
                raise ValueError("row %d: %s must be nonempty text" % (index, field))
            row[field] = row[field].strip()
        if row["unit"] not in UNITS:
            raise ValueError("row %d: unsupported unit" % index)
        row["value"] = number(row["value"], "value", missing=True)
        row["age_hours"] = number(row["age_hours"], "age_hours")
        if row["value"] is not None:
            limit = {"fraction": 1, "percent": 100}.get(row["unit"])
            if limit is not None and row["value"] > limit:
                raise ValueError("row %d: value exceeds unit range" % index)
        try:
            captured = datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("row %d: observed_at must be ISO 8601" % index) from None
        if captured.tzinfo is None or captured.utcoffset() is None:
            raise ValueError("row %d: observed_at must include timezone" % index)
        # One observation per metric/post prevents duplicate exports inflating a baseline.
        key = (row["account"], row["surface"], row["post_id"], row["metric"])
        if key in seen:
            raise ValueError("row %d duplicates an account/surface/post/metric; select one snapshot" % index)
        seen.add(key)
        normalized.append(row)
    return normalized


def analyze(rows, min_baseline=10, age_window_hours=24, include_paid=False):
    if isinstance(min_baseline, bool) or not isinstance(min_baseline, int) or min_baseline < 1:
        raise ValueError("min_baseline must be a positive integer")
    age_window_hours = number(age_window_hours, "age_window_hours")
    if age_window_hours == 0:
        raise ValueError("age_window_hours must be positive")
    rows = normalize(rows)
    groups = {}
    assessments = []
    for row in rows:
        item = dict(row, baseline_n=0, baseline_median=None, multiple=None)
        if row["value"] is None:
            item["status"] = "missing_metric"
        elif row["visibility"] not in ("public", "friends", "private"):
            item["status"] = "unknown_visibility"
        elif row["distribution"] not in ("organic", "paid"):
            item["status"] = "unknown_distribution"
        elif row["distribution"] == "paid" and not include_paid:
            item["status"] = "paid_excluded"
        else:
            item["status"] = "pending"
            age_position = row["age_hours"] / age_window_hours
            if not math.isfinite(age_position):
                raise ValueError("age_hours / age_window_hours exceeds numeric range")
            bucket = math.floor(age_position)
            key = tuple(row[field] for field in COHORT) + (bucket,)
            groups.setdefault(key, []).append(item)
        assessments.append(item)
    for group in groups.values():
        for item in group:
            values = [other["value"] for other in group if other is not item]
            item["baseline_n"] = len(values)
            if len(values) < min_baseline:
                item["status"] = "insufficient_baseline"
                continue
            lower = statistics.median_low(values)
            upper = statistics.median_high(values)
            median = lower + (upper - lower) / 2
            item["baseline_median"] = median
            if median == 0:
                item["status"] = "zero_baseline"
            else:
                ratio = item["value"] / median
                if math.isfinite(ratio):
                    item["multiple"] = ratio
                    item["status"] = "compared"
                else:
                    item["status"] = "ratio_overflow"
    return {
        "method": "same-account comparable-post median; target excluded",
        "parameters": {"min_baseline": min_baseline, "age_window_hours": age_window_hours,
                       "include_paid": include_paid},
        "warnings": ["Age buckets are a heuristic; inspect actual age matching.",
                     "Visible response is not reach, retention, causality, or a viral prediction.",
                     "Sources, metric semantics, and hidden promotion require human verification."],
        "observations": assessments,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="CSV, JSON array, or - for JSON on stdin")
    parser.add_argument("--min-baseline", type=int, default=10)
    parser.add_argument("--age-window-hours", type=float, default=24)
    parser.add_argument("--include-paid", action="store_true")
    args = parser.parse_args()
    try:
        content = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8-sig")
        rows = list(csv.DictReader(io.StringIO(content))) if args.input.lower().endswith(".csv") else json.loads(content)
        result = analyze(rows, args.min_baseline, args.age_window_hours, args.include_paid)
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    except (OSError, ValueError) as exc:
        print("Input error: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
