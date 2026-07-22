"""USB 2.0 transaction model for PPID lab 3."""

from __future__ import annotations

import argparse
import struct
from dataclasses import dataclass
from typing import Iterable, List

# USB 2.0 PID values (simplified educational subset)
PID_OUT = 0xE1
PID_IN = 0x69
PID_DATA0 = 0xC3
PID_DATA1 = 0x4B
PID_ACK = 0xD2
PID_NAK = 0x5A


@dataclass
class TokenPacket:
    pid: int
    addr: int
    endp: int

    def to_bytes(self) -> bytes:
        # Packed 11-bit ADDR (7) + ENDP (4) field. A real USB token packet also
        # appends a 5-bit CRC5 over this field; omitted here as an educational
        # simplification (see §теорія USB).
        addr_endp = ((self.addr & 0x7F) | ((self.endp & 0x0F) << 7)) & 0xFFFF
        return bytes([self.pid, addr_endp & 0xFF, (addr_endp >> 8) & 0xFF])


@dataclass
class DataPacket:
    pid: int
    payload: bytes

    def to_bytes(self) -> bytes:
        if len(self.payload) > 64:
            raise ValueError("Full-speed max data payload is 64 bytes")
        frame = bytes([self.pid]) + self.payload
        crc = _crc16(frame[1:])
        return frame + struct.pack("<H", crc)


@dataclass
class HandshakePacket:
    pid: int

    def to_bytes(self) -> bytes:
        return bytes([self.pid])


def _crc16(data: bytes) -> int:
    """Simplified educational CRC-16 (0x8005, reflected), used as the DATA
    packet checksum. NOTE: a real USB CRC-16 also inverts the final remainder
    (``^ 0xFFFF``); that step is intentionally omitted here so the produced
    bytes stay stable for the lab example — this is not a wire-accurate USB CRC.
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF


def build_out_transaction(message: str, encoding: str = "cp1251") -> List[bytes]:
    payload = message.encode(encoding)
    if len(payload) < 8:
        payload = payload + b"\x00" * (8 - len(payload))
    return [
        TokenPacket(PID_OUT, addr=1, endp=1).to_bytes(),
        DataPacket(PID_DATA0, payload).to_bytes(),
        HandshakePacket(PID_ACK).to_bytes(),
    ]


def transaction_phases(packets: Iterable[bytes]) -> List[str]:
    phases = []
    for pkt in packets:
        pid = pkt[0]
        if pid in (PID_OUT, PID_IN):
            phases.append("TOKEN")
        elif pid in (PID_DATA0, PID_DATA1):
            phases.append("DATA")
        else:
            phases.append("HANDSHAKE")
    return phases


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build USB OUT transaction")
    parser.add_argument("--message", default="IVANOV")
    parser.add_argument("--encoding", default="cp1251")
    args = parser.parse_args(argv)

    packets = build_out_transaction(args.message, args.encoding)
    phases = transaction_phases(packets)
    print("Фази:", " → ".join(phases))
    for i, pkt in enumerate(packets, 1):
        print(f"Пакет {i}: {pkt.hex(' ')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
