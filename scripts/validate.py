#!/usr/bin/env python3
"""Validate the shipped flat-frontmatter subset, local links, and resources."""

import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from sync_resources import NAMES, expected_resources


def validate_skill(folder):
    errors = []
    entry = folder / "SKILL.md"
    if not entry.is_file():
        return ["missing SKILL.md"]
    text = entry.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        return ["missing YAML frontmatter delimiters"]
    # The project intentionally uses a small valid YAML subset, not a new YAML parser.
    fields = {}
    for line in parts[1].strip().splitlines():
        match = re.fullmatch(r"(name|description): ([^\n]+)", line)
        if not match or match[1] in fields:
            errors.append("unsupported or duplicate frontmatter line")
        else:
            value = match[2]
            if ": " in value or " #" in value or value.startswith(("[", "{", "&", "*", "!", "|", ">", "'", '"')):
                errors.append("frontmatter must use safe plain scalar values")
            fields[match[1]] = value
    if fields.get("name") != folder.name or not re.fullmatch(r"fb-[a-z-]+", folder.name):
        errors.append("invalid skill name")
    if not fields.get("description") or len(fields.get("description", "")) > 1024:
        errors.append("missing/oversized description")
    if not parts[2].strip():
        errors.append("empty instructions")
    if re.search(r"\[TODO\]|\[INSERT\]|~/.claude|/plugin install", text, re.I):
        errors.append("unfinished scaffold or incompatible runtime dependency")
    for path in folder.rglob("*"):
        if path.is_symlink():
            errors.append("symlink inside skill: " + str(path))
        if path.is_file() and path.suffix == ".md":
            for target in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
                if re.match(r"[a-z]+://|#|mailto:", target):
                    continue
                destination = (path.parent / unquote(target.split("#", 1)[0])).resolve()
                if not destination.is_relative_to(folder.resolve()) or not destination.is_file():
                    errors.append("broken/outside local reference: " + str(path) + " -> " + target)
        elif path.is_file() and path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"))
            except SyntaxError as exc:
                errors.append(str(exc))
    return errors


def validate_repo(root=ROOT):
    errors = []
    folders = sorted(path.name for path in (root / "skills").iterdir() if path.is_dir())
    if folders != sorted("fb-" + name for name in NAMES):
        errors.append("skill inventory mismatch")
    for name in NAMES:
        errors.extend(name + ": " + error for error in validate_skill(root / "skills" / ("fb-" + name)))
    for source, target in expected_resources(root):
        if not target.is_file() or target.read_bytes() != source.read_bytes():
            errors.append("resource mismatch: " + str(target))
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+://|#|mailto:", target):
                continue
            destination = (path.parent / unquote(target.split("#", 1)[0])).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.is_file():
                errors.append("repository link broken/outside: " + str(path) + " -> " + target)
    try:
        plugin = json.loads((root / "plugin.json").read_text())
        for field in ("name", "version", "description", "license"):
            if not plugin.get(field):
                errors.append("plugin missing " + field)
        if plugin.get("version") != "0.1.0" or plugin.get("license") != "MIT":
            errors.append("release metadata mismatch")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    return errors


if __name__ == "__main__":
    issues = validate_repo()
    print(json.dumps({"skills": len(NAMES), "errors": issues, "result": "PASS" if not issues else "FAIL"}, indent=2))
    raise SystemExit(bool(issues))
