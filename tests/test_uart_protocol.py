"""Tests for UART message encoding (lab 1)."""

from host.uart_host import decode_message, encode_message, format_hex, verify_loopback_reply


def test_encode_message_ends_with_cr():
    payload = encode_message("SAMPLE", "cp1251")
    assert payload.endswith(b"\r")


def test_roundtrip_cp1251():
    text = "TEST"
    encoded = encode_message(text, "cp1251")
    decoded = decode_message(encoded + b"\n", "cp1251")
    assert decoded == text


def test_verify_loopback_reply():
    assert verify_loopback_reply("IVANOV", "IVANOV")
    assert not verify_loopback_reply("IVANOV", "PETRENKO")


def test_format_hex():
    assert format_hex(b"\rAB") == "0d 41 42"


def test_open_loop_port():
    from host.uart_host import open_port

    with open_port("loop://", timeout=0.5) as ser:
        ser.write(b"ping\r")
        assert ser.read_until(expected=b"\r") == b"ping\r"
