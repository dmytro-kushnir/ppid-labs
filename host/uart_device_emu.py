"""Lab 1 UART device emulator (virtual COM pair) — compulsory RX role.

Listens on one end of a linked pair, reads a line ending with ``\\r``,
prints an exchange block (hex / ACK), and replies ``ACK:<message>\\n``.

Pair with ``host.uart_pty_pair`` (or socat / com0com) and
``host.uart_host --wait-ack``.

Example (Linux/macOS, no socat)::

    # terminal 0
    python3 -m host.uart_pty_pair

    # terminal 1 (device / RX)
    python3 -m host.uart_device_emu --port /tmp/comB

    # terminal 2 (host / TX)
    python3 -m host.uart_host --message "IVANOV" --port /tmp/comA --wait-ack
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from host.uart_host import (
    DEFAULT_BAUD,
    DEFAULT_ENCODING,
    configure_port,
    decode_message,
    format_hex,
    open_port,
)


def build_ack(line: str, encoding: str = DEFAULT_ENCODING) -> bytes:
    return f"ACK:{line}\n".encode(encoding)


def handle_packet(packet: bytes, encoding: str = DEFAULT_ENCODING) -> tuple[str, bytes]:
    """Decode RX packet (…\\r) and build ACK reply. Returns (line, ack_bytes)."""
    line = decode_message(packet, encoding)
    return line, build_ack(line, encoding)


def serve_once(ser, encoding: str = DEFAULT_ENCODING) -> bool:
    """Read one frame, print exchange, send ACK. Returns False on empty/timeout."""
    packet = ser.read_until(expected=b"\r")
    if not packet:
        return False

    line, ack = handle_packet(packet, encoding)
    written = ser.write(ack)

    print("--- exchange ---")
    print(f"RX text: {line}")
    print(f"RX bytes ({len(packet)}): {format_hex(packet)}")
    print(f"TX ACK: ACK:{line}")
    print(f"TX bytes ({written}): {format_hex(ack)}")
    if written == len(ack) and line:
        print("Verify: OK")
    else:
        print("Verify: FAIL")
    print("--------------")
    return True


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lab 1 UART device emulator (compulsory RX on virtual COM)."
    )
    parser.add_argument(
        "--port",
        default="/tmp/comB",
        help="Peer port: /tmp/comB (uart_pty_pair), COM6 (com0com), …",
    )
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    parser.add_argument("--encoding", default=DEFAULT_ENCODING)
    parser.add_argument(
        "--once",
        action="store_true",
        help="Exit after one successful exchange (default: keep listening)",
    )
    args = parser.parse_args(argv)

    print("PPID Lab 1 — UART device emulator (RX)")
    print(f"Port: {args.port} | Baud: {args.baud}")
    print("Waiting for Host TX…")

    with open_port(args.port, args.baud, timeout=1.0) as ser:
        configure_port(ser, args.baud)
        while True:
            if serve_once(ser, args.encoding):
                if args.once:
                    return 0
            # empty read = timeout; keep looping unless --once already returned

    return 0


if __name__ == "__main__":
    sys.exit(main())
