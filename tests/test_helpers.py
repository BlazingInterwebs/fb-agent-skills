import copy
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


compare = module("comparison", ROOT / "shared/compare.py")
editorial = module("editorial", ROOT / "skills/fb-human/scripts/editorial.py")
timing = module("timing", ROOT / "skills/fb-video/scripts/timing.py")
sys.path.insert(0, str(ROOT / "scripts"))
import install
import validate
from sync_resources import NAMES, expected_resources


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        with (ROOT / "examples/observations.csv").open(newline="", encoding="utf-8") as stream:
            self.rows = list(csv.DictReader(stream))

    def last(self, rows=None, **kwargs):
        return compare.analyze(self.rows if rows is None else rows, **kwargs)["observations"][-1]

    def test_target_excluded(self):
        result = self.last()
        self.assertEqual(result["baseline_n"], 11)
        self.assertEqual(result["baseline_median"], 10)
        self.assertEqual(result["multiple"], 20)
        self.assertEqual(result["metric"], "reactions")

    def test_missing_not_zero(self):
        for unknown in (None, ""):
            with self.subTest(unknown=unknown):
                rows = copy.deepcopy(self.rows)
                rows[-1]["value"] = unknown
                result = self.last(rows)
                self.assertEqual(result["status"], "missing_metric")
                self.assertIsNone(result["value"])
                self.assertIsNone(result["multiple"])

    def test_zero_baseline_abstains(self):
        rows = copy.deepcopy(self.rows)
        for row in rows[:-1]:
            row["value"] = "0"
        self.assertEqual(self.last(rows)["status"], "zero_baseline")
        self.assertIsNone(self.last(rows)["multiple"])

    def test_insufficient_abstains(self):
        result = self.last(self.rows[:3])
        self.assertEqual(result["status"], "insufficient_baseline")
        self.assertIsNone(result["multiple"])

    def test_cohort_dimensions_separate(self):
        for field, value in {"account": "b", "surface": "group", "format": "text",
                             "visibility": "private", "metric": "views", "unit": "seconds",
                             "definition": "new-definition", "age_hours": "24"}.items():
            with self.subTest(field=field):
                rows = copy.deepcopy(self.rows)
                rows[-1][field] = value
                self.assertEqual(self.last(rows)["status"], "insufficient_baseline")

    def test_paid_excluded(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["distribution"] = "paid"
        self.assertEqual(self.last(rows)["status"], "paid_excluded")

    def test_paid_opt_in_still_separate(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["distribution"] = "paid"
        self.assertEqual(self.last(rows, include_paid=True)["status"], "insufficient_baseline")
        for row in rows:
            row["distribution"] = "paid"
        self.assertEqual(self.last(rows, include_paid=True)["multiple"], 20)

    def test_unknown_promotion_excluded(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["distribution"] = "unknown"
        self.assertEqual(self.last(rows)["status"], "unknown_distribution")

    def test_unknown_visibility_excluded(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["visibility"] = "unknown"
        self.assertEqual(self.last(rows)["status"], "unknown_visibility")

    def test_nonfinite_negative_boolean_rejected(self):
        for value in ("nan", "inf", "-1", True):
            with self.subTest(value=value):
                rows = copy.deepcopy(self.rows)
                rows[-1]["value"] = value
                with self.assertRaises(ValueError):
                    self.last(rows)

    def test_invalid_unit_range(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["unit"] = "fraction"
        with self.assertRaises(ValueError):
            self.last(rows)

    def test_timezone_required(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["observed_at"] = "2026-10-01T12:00:00"
        with self.assertRaises(ValueError):
            self.last(rows)

    def test_duplicate_snapshot_rejected(self):
        rows = self.rows + [dict(self.rows[0], age_hours="24")]
        with self.assertRaises(ValueError):
            self.last(rows)

    def test_missing_schema_rejected(self):
        with self.assertRaises(ValueError):
            compare.analyze([{"value": 20}])

    def test_extra_fields_preserved(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["note"] = "synthetic"
        self.assertEqual(self.last(rows)["note"], "synthetic")

    def test_parameters_rejected(self):
        for kwargs in ({"min_baseline": 0}, {"min_baseline": True},
                       {"age_window_hours": 0}, {"age_window_hours": float("nan")}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.last(**kwargs)

    def test_age_bucket_width(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["age_hours"] = "170"
        self.assertEqual(self.last(rows)["multiple"], 20)
        self.assertEqual(self.last(rows, age_window_hours=1)["status"], "insufficient_baseline")

    def test_overflow_abstains(self):
        rows = copy.deepcopy(self.rows)
        for row in rows[:-1]:
            row["value"] = 1e-300
        rows[-1]["value"] = 1e300
        self.assertEqual(self.last(rows)["status"], "ratio_overflow")
        json.dumps(compare.analyze(rows), allow_nan=False)

    def test_empty_dataset_valid(self):
        self.assertEqual(compare.analyze([])["observations"], [])

    def test_large_finite_median(self):
        rows = copy.deepcopy(self.rows[:11])
        for row in rows:
            row["value"] = 1e308
        result = self.last(rows)
        self.assertEqual(result["multiple"], 1)
        self.assertEqual(result["baseline_median"], 1e308)
        json.dumps(compare.analyze(rows), allow_nan=False)

    def test_age_numeric_overflow_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["age_hours"] = 1e308
        with self.assertRaises(ValueError):
            self.last(rows, age_window_hours=1e-300)

    def test_cli_csv_json_and_arbitrary_cwd(self):
        with tempfile.TemporaryDirectory() as cwd:
            csv_run = subprocess.run([sys.executable, "-B", str(ROOT / "skills/fb-audit/scripts/compare.py"),
                                      str(ROOT / "examples/observations.csv")], cwd=cwd,
                                     capture_output=True, text=True)
            json_run = subprocess.run([sys.executable, "-B", str(ROOT / "skills/fb-research/scripts/compare.py"), "-"],
                                      input=json.dumps(self.rows), cwd=cwd, capture_output=True, text=True)
        self.assertEqual(csv_run.returncode, 0, csv_run.stderr)
        self.assertEqual(json_run.returncode, 0, json_run.stderr)
        self.assertEqual(json.loads(csv_run.stdout), json.loads(json_run.stdout))

    def test_cli_invalid_input(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "shared/compare.py"), "-"],
                                input="not json", capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Input error", result.stderr)


class EditorialTests(unittest.TestCase):
    def test_preserves_unicode_quotes_emoji_joiners_urls_and_facts(self):
        text = "\u201cAuthentic\u201d \u2014 $4,200 \u0915\u094d\u200d\u0937 \U0001f469\u200d\U0001f4bb https://example.com/path\n"
        self.assertEqual(editorial.review(text)["text"], text)

    def test_flags_not_replacements(self):
        text = "In today's fast-paced world it always works. Thoughts?"
        result = editorial.review(text)
        self.assertEqual(result["text"], text)
        self.assertEqual(len(result["flags"]), 3)
        for flag in result["flags"]:
            self.assertEqual(text[flag["start"]:flag["end"]], flag["excerpt"])
        self.assertNotIn("score", result)

    def test_short_and_empty_text(self):
        self.assertEqual(editorial.review("Thanks, Jo.")["text"], "Thanks, Jo.")
        self.assertEqual(editorial.review("")["flags"], [])

    def test_inspection_never_deletes(self):
        text = "One\u200bTwo\ufeffThree\u00adFour"
        result = editorial.review(text)
        self.assertEqual(result["text"], text)
        self.assertEqual(len(result["flags"]), 3)

    def test_cli_preserves_original(self):
        text = "Actual draft\nThoughts?\n"
        result = subprocess.run([sys.executable, "-B", str(ROOT / "skills/fb-human/scripts/editorial.py"), "-"],
                                input=text, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["text"], text)


class TimingTests(unittest.TestCase):
    def test_word_estimate(self):
        self.assertEqual(timing.estimate("one two three", 180)["estimated_spoken_seconds"], 1)

    def test_empty(self):
        self.assertEqual(timing.estimate("")["estimated_spoken_seconds"], 0)

    def test_bad_wpm(self):
        for value in (0, -1, float("nan"), float("inf"), True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                timing.estimate("words", value)

    def test_cli(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "skills/fb-video/scripts/timing.py"), "-", "--wpm", "180"],
                                input="one two three", capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["estimated_spoken_seconds"], 1)

    def test_duration_overflow_rejected(self):
        with self.assertRaises(ValueError):
            timing.estimate("many words", 1e-320)


class PackagingTests(unittest.TestCase):
    def test_repository_valid(self):
        self.assertEqual(validate.validate_repo(), [])

    def test_common_resources_identical(self):
        for source, target in expected_resources():
            self.assertEqual(source.read_bytes(), target.read_bytes(), str(target))

    def test_individual_installed_skill_self_contained(self):
        with tempfile.TemporaryDirectory() as destination:
            receipt = install.install(destination, ["fb-post", "fb-audit"])
            self.assertEqual(len(receipt), 2)
            for name in ("fb-post", "fb-audit"):
                self.assertEqual(validate.validate_skill(Path(destination) / name), [])
            result = subprocess.run([sys.executable, "-B", str(Path(destination) / "fb-audit/scripts/compare.py"),
                                     str(ROOT / "examples/observations.csv")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_existing_file_or_folder_preflight_no_writes(self):
        with tempfile.TemporaryDirectory() as destination:
            marker = Path(destination) / "fb-post"
            marker.write_text("user content")
            with self.assertRaises(FileExistsError):
                install.install(destination, ["fb-video", "fb-post"])
            self.assertEqual(marker.read_text(), "user content")
            self.assertFalse((Path(destination) / "fb-video").exists())

    def test_dry_run_no_destination_created(self):
        with tempfile.TemporaryDirectory() as parent:
            target = Path(parent) / "new"
            self.assertEqual(install.install(target, ["fb-post"], True)[0]["status"], "dry-run")
            self.assertFalse(target.exists())

    def test_traversal_unknown_duplicate_refused(self):
        with tempfile.TemporaryDirectory() as destination:
            for names in (["../other"], ["fb-nope"], ["fb-post", "fb-post"], []):
                with self.subTest(names=names), self.assertRaises(ValueError):
                    install.install(destination, names)

    def test_broken_local_reference_detected(self):
        with tempfile.TemporaryDirectory() as parent:
            folder = Path(parent) / "fb-post"
            folder.mkdir()
            (folder / "SKILL.md").write_text("---\nname: fb-post\ndescription: Test post drafting.\n---\n[Missing](missing.md)\n")
            self.assertTrue(any("broken/outside" in e for e in validate.validate_skill(folder)))

    def test_all_skill_names_and_licenses(self):
        self.assertEqual(len(NAMES), 13)
        for name in NAMES:
            self.assertEqual((ROOT / "skills" / ("fb-" + name) / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())


if __name__ == "__main__":
    unittest.main()
