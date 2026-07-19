"""Tests for capstone host log parsing."""

import tempfile
from pathlib import Path

import pytest

from host.capstone_host import export_to_mock_usb, main, parse_log_file, parse_log_lines


def test_parse_log_lines_ignores_header() -> None:
    lines = [
        "PPID Lab 5 — Capstone node",
        "I2C: ['0x77']",
        "TEMP=22.1",
        "TEMP=23.0",
    ]
    readings = parse_log_lines(lines)
    assert readings == [(2, 22.1), (3, 23.0)]


def test_parse_log_file_sample() -> None:
    path = Path(__file__).resolve().parent.parent / "sample_log.txt"
    readings = parse_log_file(path)
    assert len(readings) == 10
    assert readings[0][1] == 22.1


def test_parse_log_file_missing(tmp_path: Path) -> None:
    missing = tmp_path / "no_such_log.txt"
    with pytest.raises(FileNotFoundError, match="sample_log.txt"):
        parse_log_file(missing)


def test_export_to_mock_usb(tmp_path: Path) -> None:
    csv_path = tmp_path / "readings.csv"
    csv_path.write_text("sample,temp_c\n0,22.1\n", encoding="utf-8")
    usb = tmp_path / "mock_usb"
    exported = export_to_mock_usb(csv_path, usb)
    assert exported == usb / "readings.csv"
    assert exported.read_text(encoding="utf-8") == csv_path.read_text(encoding="utf-8")


def test_main_export_usb_leaves_no_orphan_mkdtemp(tmp_path: Path) -> None:
    plot = tmp_path / "plot.png"
    csv_path = tmp_path / "readings.csv"
    assert main(["--plot", str(plot), "--csv", str(csv_path), "--export-usb"]) == 0
    assert plot.is_file()
    assert csv_path.is_file()
    assert not list(Path(tempfile.gettempdir()).glob("ppid_usb_export_*"))


def test_main_writes_csv_and_plot(tmp_path: Path) -> None:
    plot = tmp_path / "plot.png"
    csv_path = tmp_path / "out.csv"
    assert main(["--plot", str(plot), "--csv", str(csv_path)]) == 0
    text = csv_path.read_text(encoding="utf-8")
    assert "sample,temp_c" in text
    assert "22.1" in text
