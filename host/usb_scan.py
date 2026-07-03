"""Mock USB device enumeration for PPID lab 3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Optional

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"
DEFAULT_FIXTURE = FIXTURES_DIR / "usb_devices.json"


def load_devices(path: Path = DEFAULT_FIXTURE) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data["devices"]


def get_device_by_name(name: str, path: Path = DEFAULT_FIXTURE) -> Optional[dict[str, Any]]:
    for dev in load_devices(path):
        if dev["name"] == name:
            return dev
    return None


def format_device(dev: dict[str, Any]) -> str:
    return (
        f"{dev['vid']}:{dev['pid']} "
        f"{dev['class']} @ {dev['speed']} — {dev['name']}"
    )


def _format_optional(value: Any, suffix: str = "") -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:g}{suffix}"
    return f"{value}{suffix}"


def format_device_details(dev: dict[str, Any]) -> str:
    lines = [
        f"VID:PID: {dev['vid']}:{dev['pid']}",
        f"Клас: {dev['class']}",
        f"Швидкість: {dev['speed']}",
        f"Назва: {dev['name']}",
        f"Мітка тому: {_format_optional(dev.get('volume_label'))}",
        f"Файлова система: {_format_optional(dev.get('drive_format'))}",
        f"Обсяг: {_format_optional(dev.get('total_gb'), ' ГБ')}",
        f"Вільно: {_format_optional(dev.get('free_gb'), ' ГБ')}",
    ]
    return "\n".join(lines)


def list_usb_devices(path: Path = DEFAULT_FIXTURE) -> list[str]:
    return [format_device(d) for d in load_devices(path)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List mock USB devices")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Path to usb_devices.json",
    )
    args = parser.parse_args(argv)

    print("Mock USB enumeration (fixtures/usb_devices.json):")
    print("У продакшені: lsusb (Linux) або Get-PnpDevice (Windows)\n")
    for line in list_usb_devices(args.fixture):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
