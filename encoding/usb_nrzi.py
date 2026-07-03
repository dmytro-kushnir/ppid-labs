"""USB NRZI encoding and bit stuffing for PPID lab 2."""

from __future__ import annotations

import argparse
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

SYNC_RAW = "01010100"  # KJKJKJKK before NRZI (educational simplification)


def char_to_bits(ch: str) -> str:
    return format(ord(ch), "08b")


def message_to_bits(message: str) -> str:
    return "".join(char_to_bits(c) for c in message)


def bit_stuff(bits: str) -> str:
    """Insert 0 after six consecutive 1 bits."""
    out: List[str] = []
    ones = 0
    for b in bits:
        out.append(b)
        if b == "1":
            ones += 1
            if ones == 6:
                out.append("0")
                ones = 0
        else:
            ones = 0
    return "".join(out)


def nrzi_encode(bits: str, initial_level: int = 1) -> List[int]:
    levels = [initial_level]
    for b in bits:
        if b == "0":
            levels.append(1 - levels[-1])
        else:
            levels.append(levels[-1])
    return levels


def nrzi_bits_string(bits: str, initial_level: int = 1) -> str:
    levels = nrzi_encode(bits, initial_level)
    return "".join(str(level) for level in levels[1:])


def nrzi_encode_with_stuffing(message: str) -> tuple[str, str, List[int]]:
    raw = message_to_bits(message)
    stuffed = bit_stuff(raw)
    levels = nrzi_encode(stuffed)
    return raw, stuffed, levels


def char_nrzi_bits(ch: str) -> tuple[str, str, List[int]]:
    """Encode a single character: raw 8 bits -> bit stuffing -> NRZI levels."""
    raw = char_to_bits(ch)
    stuffed = bit_stuff(raw)
    levels = nrzi_encode(stuffed)
    return raw, stuffed, levels


def _plot_levels(levels: List[int], title: str) -> Figure:
    times = list(range(len(levels)))
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.step(times, levels, where="post")
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlabel("Біт (індекс)")
    ax.set_ylabel("NRZI рівень")
    ax.set_title(title)
    ax.grid(True)
    fig.tight_layout()
    return fig


def plot_nrzi_to_figure(message: str) -> Tuple[Figure, str, str, List[int]]:
    raw, stuffed, levels = nrzi_encode_with_stuffing(message)
    title = f"USB NRZI: {message!r} (raw {len(raw)} біт, stuffed {len(stuffed)})"
    fig = _plot_levels(levels, title)
    return fig, raw, stuffed, levels


def plot_nrzi_char_to_figure(message: str, index: int) -> Tuple[Figure, str, str, List[int]]:
    if not message:
        raise ValueError("Message is empty")
    if index < 0 or index >= len(message):
        raise IndexError(f"index out of range: {index}")
    ch = message[index]
    raw, stuffed, levels = char_nrzi_bits(ch)
    title = f"USB NRZI: {ch!r} (символ {index} з {message!r})"
    fig = _plot_levels(levels, title)
    return fig, raw, stuffed, levels


def plot_nrzi(message: str, show: bool = True) -> None:
    fig, _, _, _ = plot_nrzi_to_figure(message)
    if show:
        plt.show()
    else:
        plt.close(fig)


def plot_nrzi_char(message: str, index: int, show: bool = True) -> None:
    fig, _, _, _ = plot_nrzi_char_to_figure(message, index)
    if show:
        plt.show()
    else:
        plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="USB NRZI plot")
    parser.add_argument("--message", default="АБ")
    parser.add_argument("--char-index", type=int, default=None)
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args(argv)

    if args.char_index is not None:
        raw, stuffed, levels = char_nrzi_bits(args.message[args.char_index])
        print("Символ:", args.message[args.char_index])
    else:
        raw, stuffed, levels = nrzi_encode_with_stuffing(args.message)
    print("Біти (raw):", raw)
    print("Після bit stuffing:", stuffed)
    print("NRZI рівні:", levels)

    if args.char_index is not None:
        plot_nrzi_char(args.message, args.char_index, show=not args.no_show)
    else:
        plot_nrzi(args.message, show=not args.no_show)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
