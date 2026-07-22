"""UART frame timing diagrams for PPID lab 2."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import List, Literal, Optional, Tuple

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

ParityMode = Literal["N", "E", "O"]

# TTL logic levels: idle/mark (1) -> high, start/space (0) -> low.
# (RS-232 uses inverted voltage on the wire; see §теорія. Data bits are drawn
# MSB-first for readability — the physical line order is LSB-first.)


@dataclass(frozen=True)
class LineFormat:
    data_bits: int
    parity: ParityMode
    stop_bits: int

    @property
    def label(self) -> str:
        return f"{self.data_bits}{self.parity}{self.stop_bits}"


def parse_line_format(fmt: str) -> LineFormat:
    """Parse UART line format strings such as 8N1, 7E1, 8N2."""
    fmt = fmt.strip().upper()
    if len(fmt) != 3:
        raise ValueError(f"Invalid line format: {fmt!r}")
    data_bits = int(fmt[0])
    parity = fmt[1]
    stop_bits = int(fmt[2])
    if data_bits not in (5, 6, 7, 8):
        raise ValueError(f"Unsupported data bits: {data_bits}")
    if parity not in ("N", "E", "O"):
        raise ValueError(f"Unsupported parity: {parity}")
    if stop_bits not in (1, 2):
        raise ValueError(f"Unsupported stop bits: {stop_bits}")
    return LineFormat(data_bits=data_bits, parity=parity, stop_bits=stop_bits)


def _parity_bit(data_bits: str, parity_mode: ParityMode) -> str:
    if parity_mode == "N":
        return ""
    ones = data_bits.count("1")
    if parity_mode == "E":
        return "0" if ones % 2 == 0 else "1"
    return "1" if ones % 2 == 0 else "0"


def char_to_frame_bits(
    ch: str,
    data_bits: int = 8,
    parity_mode: ParityMode = "N",
    stop_bits: int = 1,
) -> str:
    value = ord(ch)
    mask = (1 << data_bits) - 1
    data = format(value & mask, f"0{data_bits}b")
    parity = _parity_bit(data, parity_mode)
    stop = "1" * stop_bits
    return "0" + data + parity + stop


def char_to_frame_bits_from_format(ch: str, fmt: str | LineFormat = "8N1") -> str:
    line = parse_line_format(fmt) if isinstance(fmt, str) else fmt
    return char_to_frame_bits(ch, line.data_bits, line.parity, line.stop_bits)


def message_to_frames(message: str, fmt: str | LineFormat = "8N1") -> List[str]:
    line = parse_line_format(fmt) if isinstance(fmt, str) else fmt
    return [char_to_frame_bits(c, line.data_bits, line.parity, line.stop_bits) for c in message]


def frames_to_signal(
    frames: List[str],
    bit_time: float = 1.0,
    gap_bits: int = 1,
) -> Tuple[List[float], List[int]]:
    times: List[float] = []
    levels: List[int] = []
    t = 0.0

    for frame in frames:
        for bit in frame:
            level = 1 if bit == "1" else 0
            times.extend([t, t + bit_time])
            levels.extend([level, level])
            t += bit_time
        times.extend([t, t + gap_bits * bit_time])
        levels.extend([levels[-1], levels[-1]])
        t += gap_bits * bit_time

    return times, levels


def bits_per_symbol(fmt: str | LineFormat = "8N1") -> int:
    line = parse_line_format(fmt) if isinstance(fmt, str) else fmt
    parity_count = 0 if line.parity == "N" else 1
    return 1 + line.data_bits + parity_count + line.stop_bits


def transmission_time(
    message: str,
    baud: int,
    fmt: str | LineFormat = "8N1",
    gap_bits: int = 1,
) -> float:
    bit_time = 1.0 / baud
    per_char = (bits_per_symbol(fmt) + gap_bits) * bit_time
    return len(message) * per_char


def _plot_signal(
    times: List[float],
    levels: List[int],
    title: str,
) -> Figure:
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.step(times, levels, where="post")
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlabel("Час, с")
    ax.set_ylabel("Рівень (лог.)")
    ax.set_title(title)
    ax.grid(True)
    fig.tight_layout()
    return fig


def plot_to_figure(
    message: str,
    baud: int = 9600,
    fmt: str = "8N1",
    char_index: Optional[int] = None,
    gap_bits: int = 1,
) -> Tuple[Figure, float]:
    line = parse_line_format(fmt)
    if char_index is not None:
        if not message:
            raise ValueError("Message is empty")
        if char_index < 0 or char_index >= len(message):
            raise IndexError(f"char_index out of range: {char_index}")
        plot_message = message[char_index]
        frames = message_to_frames(plot_message, line)
        title = (
            f"UART {line.label}: {plot_message!r} "
            f"(символ {char_index} з {message!r}) @ {baud} бод"
        )
        duration = transmission_time(plot_message, baud, line, gap_bits)
    else:
        frames = message_to_frames(message, line)
        duration = transmission_time(message, baud, line, gap_bits)
        title = f"UART {line.label}: {message!r} @ {baud} бод, T≈{duration:.4f} с"

    bit_time = 1.0 / baud
    times, levels = frames_to_signal(frames, bit_time=bit_time, gap_bits=gap_bits)
    fig = _plot_signal(times, levels, title)
    return fig, duration


def plot_message(
    message: str,
    baud: int = 9600,
    show: bool = True,
    fmt: str = "8N1",
    char_index: Optional[int] = None,
) -> float:
    fig, duration = plot_to_figure(message, baud, fmt, char_index)
    if show:
        plt.show()
    else:
        plt.close(fig)
    return duration


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plot UART timing diagram")
    parser.add_argument("--message", default="IVANOV")
    parser.add_argument("--baud", type=int, default=9600)
    parser.add_argument("--format", default="8N1", dest="line_format")
    parser.add_argument("--char-index", type=int, default=None)
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args(argv)

    duration = plot_message(
        args.message,
        args.baud,
        show=not args.no_show,
        fmt=args.line_format,
        char_index=args.char_index,
    )
    print(f"Розрахований час передачі: {duration:.6f} с")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
