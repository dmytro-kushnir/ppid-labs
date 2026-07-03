#!/usr/bin/env python3
"""Build docs/lab-praktikum-2026.md from template + repo sources."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

INCLUDE_RE = re.compile(r"^\{\{include:([^}]+)\}\}\s*$")

LANG_BY_SUFFIX = {
    ".py": "python",
    ".json": "json",
    ".txt": "text",
    ".md": "markdown",
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


def build(template_path: Path, output_path: Path, root: Path) -> str:
    lines = template_path.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        match = INCLUDE_RE.match(stripped)
        if match:
            out.append(render_include(root, match.group(1)))
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
