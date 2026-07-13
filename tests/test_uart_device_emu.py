"""Tests for lab 1 UART device emulator (virtual COM)."""

from __future__ import annotations

from host.uart_device_emu import build_ack, handle_packet, serve_once
from host.uart_host import format_hex, verify_ack_reply


class _FakeSerial:
    """Minimal serial stand-in for serve_once (no OS pty/socat)."""

    def __init__(self, packet: bytes) -> None:
        self._packet = packet
        self.written = b""

    def read_until(self, expected: bytes = b"\r") -> bytes:
        if expected in self._packet or self._packet.endswith(expected):
            return self._packet
        return b""

    def write(self, data: bytes) -> int:
        self.written += data
        return len(data)


def test_build_ack():
    assert build_ack("IVANOV", "cp1251") == b"ACK:IVANOV\n"


def test_handle_packet():
    line, ack = handle_packet(b"IVANOV\r", "cp1251")
    assert line == "IVANOV"
    assert ack == b"ACK:IVANOV\n"
    assert format_hex(b"IVANOV\r") == "49 56 41 4e 4f 56 0d"


def test_verify_ack_reply():
    assert verify_ack_reply("IVANOV", "ACK:IVANOV")
    assert not verify_ack_reply("IVANOV", "IVANOV")


def test_serve_once_prints_and_acks(capsys):
    ser = _FakeSerial(b"IVANOV\r")
    assert serve_once(ser, "cp1251")
    assert ser.written == b"ACK:IVANOV\n"
    out = capsys.readouterr().out
    assert "--- exchange ---" in out
    assert "RX text: IVANOV" in out
    assert "Verify: OK" in out


def test_serve_once_empty_timeout():
    class EmptySerial:
        def read_until(self, expected: bytes = b"\r") -> bytes:
            return b""

        def write(self, data: bytes) -> int:
            raise AssertionError("should not write on empty read")

    assert not serve_once(EmptySerial(), "cp1251")
