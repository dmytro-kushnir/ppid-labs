#!/usr/bin/env python3
"""Build docs/lab-praktikum-2026.md from template + repo sources."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

INCLUDE_RE = re.compile(r"^\{\{include:([^}]+)\}\}\s*$")
VARIANTS_TABLE_RE = re.compile(r"^\{\{variants_table:([^}]+)\}\}\s*$")

LANG_BY_SUFFIX = {
    ".py": "python",
    ".json": "json",
    ".txt": "text",
    ".md": "markdown",
}

SENSOR_LABELS = {
    "OLED": "I²C OLED",
    "BME280": "BME280",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def render_include(root: Path, rel_path: str) -> str:
    path = root / rel_path.strip()
    if not path.is_file():
        raise FileNotFoundError(f"Include not found: {rel_path} (expected {path})")
    content = path.read_text(encoding="utf-8")
    if content and not content.endswith("\n"):
        content += "\n"
    lang = LANG_BY_SUFFIX.get(path.suffix.lower(), "")
    opening = f"```{lang}" if lang else "```"
    return f"{opening}\n{content}```\n"


def sensor_label(sensor: str) -> str:
    return SENSOR_LABELS.get(sensor, sensor)


def render_variants_table(root: Path, rel_path: str) -> str:
    path = root / rel_path.strip()
    if not path.is_file():
        raise FileNotFoundError(f"Variants JSON not found: {rel_path} (expected {path})")
    payload: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    variants = payload.get("variants")
    if not isinstance(variants, list) or not variants:
        raise ValueError(f"No variants[] in {rel_path}")

    lines = [
        "| № | Baudrate | Формат | Датчик (лаб. 4) | Інтервал, мс (лаб. 5) | Mock USB (лаб. 3) |",
        "|---|----------|--------|-----------------|----------------------|-------------------|",
    ]
    for row in variants:
        lines.append(
            "| {id} | {baud} | {format} | {sensor} | {poll} | {usb} |".format(
                id=row["id"],
                baud=row["baud"],
                format=row["format"],
                sensor=sensor_label(str(row["sensor"])),
                poll=row["poll_ms"],
                usb=row["mock_usb_name"],
            )
        )
    return "\n".join(lines) + "\n"


def build(template_path: Path, output_path: Path, root: Path) -> str:
    lines = template_path.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        include_match = INCLUDE_RE.match(stripped)
        variants_match = VARIANTS_TABLE_RE.match(stripped)
        if include_match:
            out.append(render_include(root, include_match.group(1)))
        elif variants_match:
            out.append(render_variants_table(root, variants_match.group(1)))
        else:
            out.append(line)
    text = "".join(out)
    output_path.write_text(text, encoding="utf-8")
    return text


def check_up_to_date(template_path: Path, output_path: Path, root: Path) -> bool:
    built = build(template_path, output_path.with_suffix(".md.tmp"), root)
    current = output_path.read_text(encoding="utf-8")
    output_path.with_suffix(".md.tmp").unlink(missing_ok=True)
    return built == current


def main(argv: list[str] | None = None) -> int:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--template",
        type=Path,
        default=root / "docs" / "lab-praktikum-2026.template.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "docs" / "lab-praktikum-2026.md",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if output is stale relative to template/includes",
    )
    args = parser.parse_args(argv)

    if not args.template.is_file():
        print(f"Template missing: {args.template}", file=sys.stderr)
        return 1

    if args.check:
        if not args.output.is_file():
            print(f"Output missing: {args.output}", file=sys.stderr)
            return 1
        if not check_up_to_date(args.template, args.output, root):
            print(
                "Practicum markdown is out of date. Run: python scripts/build_standalone.py",
                file=sys.stderr,
            )
            return 1
        print("Practicum markdown is up to date.")
        return 0

    build(args.template, args.output, root)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
