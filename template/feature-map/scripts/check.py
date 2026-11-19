#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
FEATURES = ROOT / "features"
TEMPLATE = FEATURES / "_template.md"
STATUS_VALUES = {"planned", "in-progress", "implemented", "n/a"}
REQUIRED_KEYS = ("id", "title", "status", "last_verified", "related")
FEATURE_ID = re.compile(r"[A-Z][A-Z0-9]*")

errors: list[str] = []


def error(path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(REPO)}: {message}")


def parse_frontmatter(path: Path, text: str) -> dict | None:
    if not text.startswith("---\n"):
        error(path, "missing frontmatter")
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        error(path, "unterminated frontmatter")
        return None
    data: dict = {}
    current_map: dict | None = None
    for raw in text[4:end].splitlines():
        line = raw.split(" #", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("  ") and current_map is not None:
            key, _, value = line.strip().partition(":")
            current_map[key.strip()] = value.strip()
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value == "":
            current_map = {}
            data[key] = current_map
        elif value.startswith("[") and value.endswith("]"):
            current_map = None
            data[key] = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        else:
            current_map = None
            data[key] = value
    return data


def platforms() -> tuple[str, ...]:
    if not TEMPLATE.exists():
        error(TEMPLATE, "is missing; its status keys name the platforms")
        return ()
    template = parse_frontmatter(TEMPLATE, TEMPLATE.read_text(encoding="utf-8")) or {}
    status = template.get("status")
    if not isinstance(status, dict) or not status:
        error(TEMPLATE, "needs a status map; its keys name the platforms")
        return ()
    return tuple(status)


def check_spec(path: Path, text: str, fm: dict, platform_names: tuple[str, ...]) -> str | None:
    for key in REQUIRED_KEYS:
        if key not in fm:
            error(path, f"frontmatter is missing '{key}'")
    feature_id = fm.get("id", "")
    if not FEATURE_ID.fullmatch(feature_id):
        error(path, f"feature id '{feature_id}' must be upper case letters and digits")
        return None
    status = fm.get("status")
    if not isinstance(status, dict):
        error(path, f"status must be a map with {', '.join(platform_names)}")
    else:
        for platform in platform_names:
            value = status.get(platform)
            if value not in STATUS_VALUES:
                error(path, f"status.{platform} is '{value}', expected one of {sorted(STATUS_VALUES)}")
        for platform in status:
            if platform not in platform_names:
                error(path, f"status.{platform} is not a platform, expected {', '.join(platform_names)}")
    try:
        date.fromisoformat(str(fm.get("last_verified", "")))
    except ValueError:
        error(path, "last_verified must be YYYY-MM-DD")
    if not isinstance(fm.get("related", []), list):
        error(path, "related must be an inline list, for example [SESSION, ROLES]")
    if not re.search(r"^# ", text, re.MULTILINE):
        error(path, "missing H1 title")
    return feature_id


def check_requirement_ids(path: Path, text: str, feature_id: str, seen: dict) -> None:
    for match in re.finditer(r"^\|\s*([A-Z][A-Z0-9]*-\d+)\s*\|", text, re.MULTILINE):
        requirement = match.group(1)
        if not re.fullmatch(rf"{feature_id}-\d{{3}}", requirement):
            error(path, f"requirement '{requirement}' should look like {feature_id}-NNN")
        if requirement in seen:
            error(path, f"requirement '{requirement}' is also defined in {seen[requirement]}")
        seen[requirement] = path.relative_to(REPO)


def index_rows(index_text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in index_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and FEATURE_ID.fullmatch(cells[0]):
            rows[cells[0]] = cells
    return rows


def check_index_status(index_path: Path, path: Path, row: list[str], fm: dict, platform_names: tuple[str, ...]) -> None:
    status = fm.get("status")
    if not isinstance(status, dict) or len(row) < 4:
        return
    expected = " / ".join(str(status.get(platform)) for platform in platform_names)
    actual = " / ".join(part.strip() for part in re.split(r"\s+/\s+", row[3]))
    if actual != expected:
        error(index_path, f"status for {row[0]} is '{actual}', but {path.name} says '{expected}'")


def check_links(path: Path, text: str) -> None:
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        resolved = (path.parent / target.split("#", 1)[0]).resolve()
        outside_repository = REPO not in resolved.parents and resolved != REPO
        if not outside_repository and not resolved.exists():
            error(path, f"broken link '{target}'")


def main() -> int:
    platform_names = platforms()
    index_path = ROOT / "INDEX.md"
    index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    if not index_text:
        error(index_path, "is missing or empty")
    rows = index_rows(index_text)
    feature_ids: dict[str, Path] = {}
    requirement_ids: dict[str, Path] = {}
    related: dict[Path, list[str]] = {}

    for path in sorted(FEATURES.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(path, text)
        if fm is None:
            continue
        feature_id = check_spec(path, text, fm, platform_names)
        if feature_id is None:
            continue
        if feature_id in feature_ids:
            error(path, f"feature id '{feature_id}' is also used by {feature_ids[feature_id]}")
        feature_ids[feature_id] = path.relative_to(REPO)
        check_requirement_ids(path, text, feature_id, requirement_ids)
        if f"(features/{path.name})" not in index_text:
            error(index_path, f"does not link features/{path.name}")
        if feature_id in rows:
            check_index_status(index_path, path, rows[feature_id], fm, platform_names)
        if isinstance(fm.get("related"), list):
            related[path] = fm["related"]

    for feature_id, path in feature_ids.items():
        if feature_id not in rows:
            error(index_path, f"has no row for {feature_id} ({path})")

    for path, ids in related.items():
        for related_id in ids:
            if related_id not in rows:
                error(path, f"related id '{related_id}' has no row in INDEX.md")

    for path in sorted(ROOT.rglob("*.md")):
        check_links(path, path.read_text(encoding="utf-8"))

    for line in errors:
        print(f"error: {line}")
    print(f"{len(feature_ids)} spec(s), {len(requirement_ids)} requirement(s), {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
