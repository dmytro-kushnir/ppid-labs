"""Create a linked virtual COM pair without socat (Linux/macOS).

Bridges two PTYs and optionally symlinks them to ``/tmp/comA`` and ``/tmp/comB``.
Leave this process running while you use ``uart_host`` and ``uart_device_emu``.

Example::

    # terminal 0
    python3 -m host.uart_pty_pair

    # terminal 1
    python3 -m host.uart_device_emu --port /tmp/comB

    # terminal 2
    python3 -m host.uart_host --message "IVANOV" --port /tmp/comA --wait-ack

Windows: use com0com instead (this module needs ``pty``).
"""

from __future__ import annotations

import argparse
import os
import pty
import select
import sys
from pathlib import Path


def _symlink(link: Path, target: str) -> None:
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(target)


def bridge_pair(link_a: Path, link_b: Path) -> int:
    master_a, slave_a = pty.openpty()
    master_b, slave_b = pty.openpty()
    name_a = os.ttyname(slave_a)
    name_b = os.ttyname(slave_b)
    # Keep slave FDs open so the PTYs stay alive; clients open the same tty by name.

    try:
        _symlink(link_a, name_a)
        _symlink(link_b, name_b)
    except OSError as exc:
        print(f"Could not create symlinks {link_a} / {link_b}: {exc}", file=sys.stderr)
        print(f"Use ports directly:\n  A: {name_a}\n  B: {name_b}", file=sys.stderr)
        link_a_s, link_b_s = name_a, name_b
    else:
        link_a_s, link_b_s = str(link_a), str(link_b)

    print("PPID Lab 1 — virtual COM pair (no socat)")
    print(f"  {link_a_s}  ↔  {link_b_s}")
    print(f"  ({name_a} ↔ {name_b})")
    print("Leave this running. Ctrl+C to stop.")
    print()
    print("Then:")
    print(f"  python3 -m host.uart_device_emu --port {link_b_s}")
    print(f'  python3 -m host.uart_host --message "IVANOV" --port {link_a_s} --wait-ack')
    sys.stdout.flush()

    try:
        while True:
            readable, _, _ = select.select([master_a, master_b], [], [])
            for src, dst in ((master_a, master_b), (master_b, master_a)):
                if src not in readable:
                    continue
                try:
                    data = os.read(src, 4096)
                except OSError:
                    return 1
                if not data:
                    continue
                os.write(dst, data)
    except KeyboardInterrupt:
        print("\nPair stopped.")
    finally:
        for fd in (master_a, master_b, slave_a, slave_b):
            try:
                os.close(fd)
            except OSError:
                pass
        for link in (link_a, link_b):
            try:
                if link.is_symlink():
                    link.unlink()
            except OSError:
                pass
    return 0


def main(argv: list[str] | None = None) -> int:
    if os.name == "nt":
        print(
            "uart_pty_pair needs Linux/macOS. On Windows use com0com "
            "(see docs/SETUP.md).",
            file=sys.stderr,
        )
        return 1

    parser = argparse.ArgumentParser(
        description="Linked PTY pair for optional lab 1 PC exchange (no socat)"
    )
    parser.add_argument("--link-a", default="/tmp/comA", help="symlink for host TX")
    parser.add_argument("--link-b", default="/tmp/comB", help="symlink for device emu")
    args = parser.parse_args(argv)
    return bridge_pair(Path(args.link_a), Path(args.link_b))


if __name__ == "__main__":
    sys.exit(main())
