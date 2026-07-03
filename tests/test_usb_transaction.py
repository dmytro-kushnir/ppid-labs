"""Tests for USB transaction builder (lab 3)."""

from host.usb_transaction import (
    PID_ACK,
    PID_DATA0,
    PID_OUT,
    build_out_transaction,
    transaction_phases,
)


def test_out_transaction_has_three_phases():
    packets = build_out_transaction("TEST", "utf-8")
    assert len(packets) == 3
    assert transaction_phases(packets) == ["TOKEN", "DATA", "HANDSHAKE"]


def test_token_packet_starts_with_out_pid():
    packets = build_out_transaction("X", "utf-8")
    assert packets[0][0] == PID_OUT


def test_data_packet_pid():
    packets = build_out_transaction("X", "utf-8")
    assert packets[1][0] == PID_DATA0


def test_handshake_is_ack():
    packets = build_out_transaction("X", "utf-8")
    assert packets[2][0] == PID_ACK


def test_data_payload_min_length():
    packets = build_out_transaction("A", "utf-8")
    data_pkt = packets[1]
    assert len(data_pkt) >= 1 + 8 + 2  # pid + min payload + crc
