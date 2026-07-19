# PPID Labs (course toolkit)

> **Purpose** — give every student a working baseline for five laboratory works in **Peripheral Devices, Interfaces and Drivers** (PPID, LPNU): Python host tools, Wokwi ESP32 firmware templates, fixtures, and pytest checks. No physical hardware required.

Full practicum (objectives, reports, variant table, inline code listings): **[docs/lab-praktikum-2026.md](docs/lab-praktikum-2026.md)** — генерується з [`lab-praktikum-2026.template.md`](docs/lab-praktikum-2026.template.md) скриптом `scripts/build_standalone.py`.
Course home: **[dmytro-kushnir.github.io/#/peripheral-devices/](https://dmytro-kushnir.github.io/#/peripheral-devices/)**

---

## Project layout

| Path | Purpose |
|------|---------|
| [`host/`](host/) | Python on PC: UART, USB model, capstone log processor |
| [`encoding/`](encoding/) | UART and NRZI timing diagrams (matplotlib) |
| [`wokwi/`](wokwi/) | ESP32 MicroPython + `diagram.json` (labs 1, 4, 5) |
| [`fixtures/`](fixtures/) | Mock USB devices, assignment variants |
| [`tests/`](tests/) | Pytest suite ([tests/README.md](tests/README.md)) |
| [`examples/`](examples/) | Per-lab guides ([examples/README.md](examples/README.md)) |
| [`docs/`](docs/) | [Practicum](docs/lab-praktikum-2026.md), [supplement](docs/lectures-supplement-2026.md), [setup](docs/SETUP.md), [architecture](docs/ARCHITECTURE.md) |

---

## Quick start

```bash
git clone https://github.com/dmytro-kushnir/ppid-labs.git
cd ppid-labs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python3 -m pytest tests/ -v
```

### By lab

```bash
# Lab 1 — UART: TX host + RX uart_device_emu (virtual COM, compulsory)
python3 -m host.uart_pty_pair
# python3 -m host.uart_device_emu --port /tmp/comB
# python3 -m host.uart_host --message "IVANOV" --port /tmp/comA --wait-ack

# Lab 1 — TX self-check only (loop://); not the RX role
python3 -m host.uart_host --message "IVANOV"

# Lab 1 — with a real or virtual port
python3 -m host.uart_host --message "IVANOV" --port COM5          # Windows USB-UART or com0com
python3 -m host.uart_host --message "IVANOV" --port /dev/ttyUSB0 # Linux USB-UART
python3 -m host.uart_host --message "IVANOV" --port /tmp/comA     # Linux/macOS (pty pair)
# Lab 2 — signal plots
python3 -m encoding.uart_plot --message "IVANOV" --baud 9600
python3 -m encoding.usb_nrzi --message "IVANOV"
python3 -m host.signal_gui   # reference GUI (UART + NRZI tabs)

# Lab 3 — USB model
python3 -m host.usb_transaction --message "IVANOV"
python3 -m host.usb_scan
python3 -m host.usb_gui

# Lab 5 — capstone host (after Wokwi → my_log.txt)
python3 -m host.capstone_host --input my_log.txt --plot capstone_plot.png --csv readings.csv
```

Wokwi (labs 4–5): import `wokwi/lab04-i2c-sensor/` or `lab05-capstone/` — see [docs/SETUP.md](docs/SETUP.md).

### Lab 1: `--port` by platform

| Scenario | `--port` value | OS |
|----------|----------------|-----|
| No hardware (default) | `loop://` | all (Windows, Linux, macOS) |
| USB-UART adapter | `COM3`, `COM5`, … | Windows |
| USB-UART adapter | `/dev/ttyUSB0`, `/dev/ttyACM0` | Linux |
| USB-UART adapter | `/dev/cu.usbserial-*`, `/dev/cu.usbmodem*` | macOS |
| Virtual pair (**compulsory** Host↔Device) | `COM5` / `COM6` | Windows ([com0com](https://com0com.sourceforge.net/)) |
| Virtual pair (**compulsory** Host↔Device) | `/tmp/comA`, `/tmp/comB` | Linux/macOS (`uart_pty_pair`, see SETUP) |

`loop://` works the same on every OS (pyserial `serial_for_url`). Virtual COM tools differ by OS; see [docs/SETUP.md](docs/SETUP.md) § Virtual COM ports.

---

## Playground scope

| Lab | Repo provides | Students implement / report |
|-----|---------------|---------------------------|
| **1** UART host↔device | `uart_host.py`, `uart_device_emu.py`, `uart_pty_pair.py` | Live ACK exchange, defence demo |
| **2** Signal plots | `uart_plot.py`, `usb_nrzi.py`, `signal_gui.py` (reference) | Diagrams for full message, time calculation |
| **3** USB model | Transaction builder, mock scan, `usb_gui.py` | Transaction diagram, USB-A vs USB-C comparison |
| **4** I²C | Wokwi BMP180 (+ OLED variants) | `i2c.scan()`, Logic Analyzer screenshot |
| **5** Capstone | Wokwi telemetry + `capstone_host.py` | Component diagram, CSV plot, driver layers |

Assignment variants: [fixtures/variants.json](fixtures/variants.json) — **surname** as message (labs 1–3); **variant number** for baud, format, sensor.

---

## Related materials

| Resource | URL |
|----------|-----|
| Practicum 2026 | [docs/lab-praktikum-2026.md](docs/lab-praktikum-2026.md) |
| Lectures supplement | [docs/lectures-supplement-2026.md](docs/lectures-supplement-2026.md) |
| Course overview (Marp) | [docs/course-overview-2026.md](docs/course-overview-2026.md) |

---

## License

See [LICENSE](LICENSE).
