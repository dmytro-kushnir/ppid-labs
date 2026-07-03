#!/usr/bin/env python3
"""Generate labeled placeholder PNG figures for docs/lab-praktikum-2026."""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

FIGURES: list[tuple[str, str, str]] = [
    (
        "rs232-db9-connector.png",
        "Рис. A.1. Приклад використання 9-контактного з'єднувача послідовного порта",
        "Ілюстрація методички",
    ),
    (
        "rs232-timing.png",
        "Рис. A.2. Часові діаграми передачі символу для інтерфейсу RS-232C (ТТЛ та RS-232C)",
        "Ілюстрація методички",
    ),
    (
        "rs232-db25-db9-pinout.png",
        "Рис. A.3. Розташування контактів з'єднувачів DB25P та DB9P",
        "Ілюстрація методички",
    ),
    (
        "rs232-4wire.png",
        "Рис. A.4. Схема 4-провідного з'єднання для RS-232C",
        "Ілюстрація методички",
    ),
    (
        "rs232-word-format.png",
        "Рис. A.5. Формат слова у логічних рівнях для RS-232C",
        "Ілюстрація методички",
    ),
    (
        "rs232-signal-levels.png",
        "Рис. A.6. Рівні сигналів RS-232C на передавальному та приймаючому кінцях",
        "Ілюстрація методички",
    ),
    (
        "uart-waveform-example.png",
        "Рис. A.7. Приклад амплітудно-часової діаграми UART (uart_plot / signal_gui)",
        "Замініть виходом програми студента",
    ),
    (
        "usb-nrzi-coding.png",
        "Рис. A.8. Кодування NRZI при посимвольній передачі даних (USB 2.0)",
        "Ілюстрація методички",
    ),
    (
        "usb-connectors.png",
        "Рис. B.1. Типи з'єднувачів USB (A/B; оглядово USB-C)",
        "Ілюстрація методички",
    ),
    (
        "usb-gui-example.png",
        "Рис. B.2. Вікно програми usb_gui (сканування, властивості, запис)",
        "Замініть скріном usb_gui",
    ),
    (
        "i2c-timing.png",
        "Рис. C.1. Часова діаграма I²C (START, адреса, ACK, дані, STOP)",
        "Ілюстрація методички",
    ),
    (
        "i2c-logic-analyzer.png",
        "Рис. C.2. Декодування SDA/SCL у PulseView (Logic Analyzer Wokwi)",
        "Замініть скріном PulseView",
    ),
]


def wrap_lines(text: str, width: int = 52) -> list[str]:
    return textwrap.wrap(text, width=width) or [text]


def render_placeholder(output: Path, caption: str, pdf_ref: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=120)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    box = Rectangle(
        (0.05, 0.18),
        0.9,
        0.72,
        linewidth=2,
        edgecolor="#666666",
        facecolor="#e8e8e8",
        linestyle="--",
    )
    ax.add_patch(box)

    ax.text(
        0.5,
        0.54,
        "PLACEHOLDER",
        ha="center",
        va="center",
        fontsize=28,
        fontweight="bold",
        color="#888888",
        alpha=0.85,
    )
    ax.text(
        0.5,
        0.40,
        pdf_ref,
        ha="center",
        va="center",
        fontsize=11,
        color="#666666",
        style="italic",
    )

    y = 0.08
    for line in wrap_lines(caption):
        ax.text(0.5, y, line, ha="center", va="bottom", fontsize=10, color="#222222")
        y -= 0.045

    fig.tight_layout(pad=0.4)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    out_dir = root / "docs" / "images"
    for filename, caption, pdf_ref in FIGURES:
        path = out_dir / filename
        render_placeholder(path, caption, pdf_ref)
        print(f"Wrote {path}")
    print(f"Generated {len(FIGURES)} placeholders in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
