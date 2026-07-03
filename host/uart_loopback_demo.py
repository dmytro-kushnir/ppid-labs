"""Loopback demo for lab 1 without virtual COM drivers."""

from __future__ import annotations

from host.uart_host import (
    configure_port,
    encode_message,
    format_hex,
    open_port,
    receive_message,
)

MESSAGE = "SAMPLE"
PORT = "loop://"
EXPECTED_ACK = f"ACK:{MESSAGE}"


def main() -> None:
    """Simulate TX + device ACK using a single loop:// port (no COM drivers)."""
    payload = encode_message(MESSAGE)
    with open_port(PORT, timeout=1) as ser:
        configure_port(ser)
        ser.write(payload)
        packet = ser.read_until(expected=b"\r")
        ser.write(b"ACK:" + packet + b"\n")
        reply = receive_message(ser, until=b"\n")
        print(f"TX text: {MESSAGE!r}")
        print(f"TX hex: {format_hex(payload)}")
        print(f"RX text: {reply!r}")
        if reply == EXPECTED_ACK:
            print("Verify: OK")
        else:
            print(f"Verify: FAIL (очікувалось {EXPECTED_ACK!r})")


if __name__ == "__main__":
    main()
