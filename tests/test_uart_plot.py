"""Tests for UART timing plot helpers (lab 2)."""

from encoding.uart_plot import (
    char_to_frame_bits_from_format,
    parse_line_format,
    transmission_time,
)


def test_parse_line_format_8n1():
    fmt = parse_line_format("8N1")
    assert fmt.data_bits == 8
    assert fmt.parity == "N"
    assert fmt.stop_bits == 1
    assert fmt.label == "8N1"


def test_parse_line_format_7e1():
    fmt = parse_line_format("7E1")
    assert fmt.data_bits == 7
    assert fmt.parity == "E"
    assert fmt.stop_bits == 1


def test_parse_line_format_8n2():
    fmt = parse_line_format("8N2")
    assert fmt.data_bits == 8
    assert fmt.parity == "N"
    assert fmt.stop_bits == 2


def test_char_to_frame_bits_8n1_no_parity():
    # 'A' = 0x41 = 01000001 -> start 0 + data + stop 1
    frame = char_to_frame_bits_from_format("A", "8N1")
    assert frame.startswith("0")
    assert "01000001" in frame
    assert frame.endswith("1")
    assert len(frame) == 1 + 8 + 1  # start + data + stop


def test_char_to_frame_bits_7e1_has_parity():
    frame = char_to_frame_bits_from_format("A", "7E1")
    assert len(frame) == 1 + 7 + 1 + 1  # start + 7 data + parity + stop


def test_char_to_frame_bits_8n2_two_stop_bits():
    frame = char_to_frame_bits_from_format("A", "8N2")
    assert frame.endswith("11")
    assert len(frame) == 1 + 8 + 2


def test_transmission_time_scales_with_baud():
    t_fast = transmission_time("AB", baud=9600, fmt="8N1")
    t_slow = transmission_time("AB", baud=4800, fmt="8N1")
    assert t_slow == t_fast * 2
