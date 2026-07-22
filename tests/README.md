# Tests

Baseline regression tests for the PPID lab toolkit. They verify UART message encoding / optional device emu, USB NRZI/bit stuffing, and USB OUT transaction building.

## Run

```bash
pip3 install -r requirements.txt -r requirements-dev.txt
python3 -m pytest tests/ -v
```

## What is covered

| Module | Tests |
|--------|-------|
| `host/uart_host.py` | Message ends with `\r`, cp1251 roundtrip, ACK verify helper |
| `host/uart_device_emu.py` | ACK framing; pty Host↔Device exchange (Unix) |
| `encoding/uart_plot.py` | Line-format parsing, frame bits, transmission time |
| `encoding/usb_nrzi.py` | Bit length, bit stuffing, NRZI levels |
| `host/usb_transaction.py` | Token→Data→Handshake phases, PIDs, payload size |
| `host/capstone_host.py` | Log parsing, CSV/plot output, mock USB export |

## Lab reports

Students run `pytest` locally to verify host/encoding code before the defence. Wokwi labs (4, 5) are demonstrated via simulation screenshots, not pytest.

## CI

GitHub Actions runs this suite on push/PR (Python 3.11 and 3.12).
