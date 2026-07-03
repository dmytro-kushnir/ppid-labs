"""Tests for USB NRZI encoding (lab 2)."""

from encoding.usb_nrzi import (
    bit_stuff,
    char_nrzi_bits,
    char_to_bits,
    message_to_bits,
    nrzi_encode,
    nrzi_encode_with_stuffing,
)


def test_message_to_bits_length():
    bits = message_to_bits("AB")
    assert len(bits) == 16


def test_bit_stuff_inserts_zero_after_six_ones():
    raw = "1111110"
    stuffed = bit_stuff(raw)
    assert stuffed == "11111100"


def test_nrzi_toggle_on_zero():
    levels = nrzi_encode("010")
    assert levels == [1, 0, 0, 1]


def test_nrzi_hold_on_one():
    levels = nrzi_encode("11", initial_level=1)
    assert levels == [1, 1, 1]


def test_char_nrzi_bits_single_byte():
    raw, stuffed, levels = char_nrzi_bits("A")
    assert raw == char_to_bits("A")
    assert len(levels) == len(stuffed) + 1
    assert levels[0] == 1


def test_char_nrzi_bits_matches_full_message_prefix():
    message = "AB"
    char_raw, char_stuffed, char_levels = char_nrzi_bits("A")
    full_raw, full_stuffed, full_levels = nrzi_encode_with_stuffing("A")
    assert char_raw == full_raw
    assert char_stuffed == full_stuffed
    assert char_levels == full_levels
    assert message_to_bits(message).startswith(char_raw)
