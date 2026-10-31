#!/usr/bin/env python3
"""Validate a v1 release and update the one supported Python version field."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
HEADING = re.compile(r"^## \[([^]]+)\](?:[ \t]+-[ \t]+.*)?[ \t]*$", re.M)
PROJECT_VERSION = re.compile(r'^(version\s*=\s*)"([^"]+)"\s*$', re.M)


def version(value: str) -> tuple[int, int, int]:
    match = VERSION.fullmatch(value)
    if not match:
        raise ValueError("release-version must be stable X.Y.Z without a leading v")
    return tuple(map(int, match.groups()))


def validate_changelog(text: str, requested: str) -> None:
    headings = list(HEADING.finditer(text))
    unreleased = [h for h in headings if h.group(1).lower() == "unreleased"]
    if len(unreleased) != 1:
        raise ValueError("CHANGELOG.md must contain exactly one ## [Unreleased] heading")
    if sum(h.group(1) == requested for h in headings):
        raise ValueError(f"CHANGELOG.md already contains version {requested}")
    start = unreleased[0].end()
    following = next((h.start() for h in headings if h.start() > start), len(text))
    body = text[start:following]
    if not re.search(r"^\s*[-*+]\s+\S", body, re.M):
        raise ValueError("the Unreleased section must contain at least one list entry")


def validate_project_version(path: Path, requested: str) -> None:
    if path.name == "VERSION":
        current = path.read_text().strip()
        if version(current) >= version(requested):
            raise ValueError("release-version must be greater than VERSION")
        return
    match = PROJECT_VERSION.search(path.read_text())
    if not match:
        raise ValueError("pyproject.toml must contain a literal project version")
    if version(match.group(2)) >= version(requested):
        raise ValueError("release-version must be greater than pyproject.toml version")


def update_project_version(path: Path, requested: str) -> None:
    if path.name == "VERSION":
        path.write_text(f"{requested}\n")
        return
    text = path.read_text()
    updated, count = PROJECT_VERSION.subn(rf'\g<1>"{requested}"', text, count=1)
    if count != 1:
        raise ValueError("pyproject.toml must contain a literal project version")
    path.write_text(updated)


def version_file(path: Path | None) -> Path:
    if path:
        return path
    return Path("pyproject.toml") if Path("pyproject.toml").is_file() else Path("VERSION")


def release_notes(text: str, requested: str) -> str:
    headings = list(HEADING.finditer(text))
    found = [h for h in headings if h.group(1) == requested]
    if len(found) != 1:
        raise ValueError(f"CHANGELOG.md must contain exactly one version {requested}")
    start = found[0].end()
    following = next((h.start() for h in headings if h.start() > start), len(text))
    return text[start:following].strip()


def rollover_changelog(path: Path, requested: str, date: str) -> None:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise ValueError("release-date must be YYYY-MM-DD")
    text = path.read_text()
    validate_changelog(text, requested)
    headings = list(HEADING.finditer(text))
    unreleased = next(h for h in headings if h.group(1).lower() == "unreleased")
    following = next((h.start() for h in headings if h.start() > unreleased.end()), len(text))
    released = f"## [{requested}] - {date}"
    path.write_text(text[: unreleased.end()] + "\n\n" + released + text[unreleased.end() :])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "rollover", "update-version", "release-notes"))
    parser.add_argument("--version", required=True)
    parser.add_argument("--date")
    parser.add_argument("--changelog", type=Path, default=Path("CHANGELOG.md"))
    parser.add_argument("--version-file", type=Path)
    args = parser.parse_args()
    try:
        version(args.version)
        args.version_file = version_file(args.version_file)
        if args.command == "validate":
            validate_changelog(args.changelog.read_text(), args.version)
            validate_project_version(args.version_file, args.version)
        if args.command == "rollover":
            if not args.date:
                raise ValueError("rollover requires --date")
            rollover_changelog(args.changelog, args.version, args.date)
        if args.command == "update-version":
            validate_project_version(args.version_file, args.version)
            update_project_version(args.version_file, args.version)
            print(args.version_file)
        if args.command == "release-notes":
            print(release_notes(args.changelog.read_text(), args.version))
    except (OSError, ValueError) as error:
        print(f"::error::{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
