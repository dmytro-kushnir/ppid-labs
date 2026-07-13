"""UART host utilities for PPID lab 1."""

from __future__ import annotations

import argparse
import sys
from typing import Optional

import serial

DEFAULT_BAUD = 9600
DEFAULT_ENCODING = "cp1251"


def open_port(
    name: str,
    baud: int = DEFAULT_BAUD,
    timeout: float = 1.0,
) -> serial.Serial:
    # Lab 1 keeps line format fixed at 8N1; parity/stop variants are explored in lab 2.
    kwargs = {
        "baudrate": baud,
        "bytesize": serial.EIGHTBITS,
        "parity": serial.PARITY_NONE,
        "stopbits": serial.STOPBITS_ONE,
        "timeout": timeout,
    }
    # loop:// and other URL schemes need serial_for_url (Serial() treats them as paths)
    try:
        if "://" in name:
            return serial.serial_for_url(name, **kwargs)
        return serial.Serial(port=name, **kwargs)
    except serial.SerialException as exc:
        hint = ""
        if name.startswith("/tmp/com") or name.startswith("/dev/tty"):
            hint = (
                "\nHint (Linux/macOS): start a virtual pair first:\n"
                "  python3 -m host.uart_pty_pair\n"
                "Or install socat and create /tmp/comA ↔ /tmp/comB (see docs/SETUP.md)."
            )
        raise serial.SerialException(f"{exc}{hint}") from None


def configure_port(ser: serial.Serial, baud: int = DEFAULT_BAUD) -> None:
    ser.baudrate = baud
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE


def encode_message(text: str, encoding: str = DEFAULT_ENCODING) -> bytes:
    return (text + "\r").encode(encoding)


def decode_message(data: bytes, encoding: str = DEFAULT_ENCODING) -> str:
    return data.decode(encoding, errors="replace").strip("\r\n")


def send_message(
    ser: serial.Serial,
    text: str,
    encoding: str = DEFAULT_ENCODING,
) -> int:
    payload = encode_message(text, encoding)
    return ser.write(payload)


def receive_message(
    ser: serial.Serial,
    encoding: str = DEFAULT_ENCODING,
    until: bytes = b"\r",
) -> str:
    data = ser.read_until(expected=until)
    return decode_message(data, encoding)


def exchange_loopback(
    ser: serial.Serial,
    text: str,
    encoding: str = DEFAULT_ENCODING,
) -> str:
    """Send and read echo on loop:// port."""
    send_message(ser, text, encoding)
    return receive_message(ser, encoding)


def format_hex(data: bytes) -> str:
    return " ".join(f"{b:02x}" for b in data)


def verify_loopback_reply(sent: str, reply: str) -> bool:
    return reply == sent


def verify_ack_reply(sent: str, reply: str) -> bool:
    return reply == f"ACK:{sent}"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="UART host send/receive")
    parser.add_argument(
        "--port",
        default="loop://",
        help="loop:// (all OS), COM5 (Windows), /dev/ttyUSB0 (Linux), /tmp/comA (socat)",
    )
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    parser.add_argument("--message", default="SAMPLE")
    parser.add_argument("--encoding", default=DEFAULT_ENCODING)
    parser.add_argument(
        "--wait-ack",
        action="store_true",
        help="Wait for ACK:… from peer (use with uart_device_emu on virtual COM)",
    )
    args = parser.parse_args(argv)

    with open_port(args.port, args.baud, timeout=2) as ser:
        configure_port(ser, args.baud)
        payload = encode_message(args.message, args.encoding)
        nbytes = send_message(ser, args.message, args.encoding)
        print(f"TX text: {args.message!r}")
        print(f"Надіслано байт: {nbytes}")
        print(f"TX hex: {format_hex(payload)}")
        if args.port.startswith("loop"):
            # Echo self-check of TX write — not the device RX role (use --wait-ack + emu).
            reply = receive_message(ser, args.encoding)
            print(f"RX text (loopback): {reply!r}")
            if verify_loopback_reply(args.message, reply):
                print("Verify: OK")
            else:
                print(f"Verify: FAIL (очікувалось {args.message!r})")
        elif args.wait_ack:
            reply = receive_message(ser, args.encoding, until=b"\n")
            print(f"RX text: {reply!r}")
            expected = f"ACK:{args.message}"
            if verify_ack_reply(args.message, reply):
                print("Verify: OK")
            else:
                print(f"Verify: FAIL (очікувалось {expected!r})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
