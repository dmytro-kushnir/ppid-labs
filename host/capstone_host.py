"""Capstone host: parse sensor log and plot (PPID lab 5)."""

from __future__ import annotations

import argparse
import csv
import re
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt

TEMP_RE = re.compile(r"TEMP=(-?\d+(?:\.\d+)?)")


def parse_log_lines(lines: list[str]) -> list[tuple[int, float]]:
    readings: list[tuple[int, float]] = []
    for i, line in enumerate(lines):
        match = TEMP_RE.search(line)
        if not match:
            continue
        try:
            value = float(match.group(1))
        except ValueError:
            # Skip malformed readings (e.g. noisy serial line) instead of crashing.
            continue
        readings.append((i, value))
    return readings


def parse_log_file(path: Path) -> list[tuple[int, float]]:
    if not path.is_file():
        repo_sample = Path(__file__).resolve().parent.parent / "sample_log.txt"
        hint = (
            f"Файл не знайдено: {path}\n"
            f"Для швидкого тесту: python3 -m host.capstone_host\n"
            f"(за замовчуванням — {repo_sample})\n"
            f"Або з Wokwi збережіть Serial Monitor у my_log.txt і передайте --input my_log.txt"
        )
        raise FileNotFoundError(hint)
    text = path.read_text(encoding="utf-8", errors="replace")
    return parse_log_lines(text.splitlines())


def write_csv(readings: list[tuple[int, float]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sample", "temp_c"])
        writer.writerows(readings)


def plot_readings(readings: list[tuple[int, float]], out_path: Path) -> None:
    if not readings:
        raise ValueError("No TEMP= readings found in log")
    xs = [r[0] for r in readings]
    ys = [r[1] for r in readings]
    plt.figure(figsize=(8, 4))
    plt.plot(xs, ys, marker="o")
    plt.xlabel("Зразок")
    plt.ylabel("Температура, °C")
    plt.title("PPID Capstone — моніторинг")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def export_to_mock_usb(csv_path: Path, usb_dir: Path) -> Path:
    usb_dir.mkdir(parents=True, exist_ok=True)
    target = usb_dir / csv_path.name
    target.write_bytes(csv_path.read_bytes())
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Capstone host log processor")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "sample_log.txt",
        help="Serial log with TEMP=... lines (default: sample_log.txt in repo)",
    )
    parser.add_argument("--plot", type=Path, default=Path("capstone_plot.png"))
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("readings.csv"),
        help="Write parsed temperatures to this CSV",
    )
    parser.add_argument("--export-usb", action="store_true")
    args = parser.parse_args(argv)

    readings = parse_log_file(args.input)
    print(f"Знайдено зчитувань: {len(readings)}")

    write_csv(readings, args.csv)
    plot_readings(readings, args.plot)
    print(f"CSV: {args.csv}")
    print(f"Графік: {args.plot}")

    if args.export_usb:
        with tempfile.TemporaryDirectory(prefix="ppid_usb_export_") as tmp:
            exported = export_to_mock_usb(args.csv, Path(tmp) / "mock_usb")
            print(f"Експорт на mock USB: {exported}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
