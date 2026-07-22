# Setup

## Python (labs 1–3, 5 host)

```bash
git clone https://github.com/dmytro-kushnir/ppid-labs.git
cd ppid-labs
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
python3 -m pytest tests/ -v
```

## Variants

Assignment parameters (baud, format, sensor, poll interval) are in [fixtures/variants.json](../fixtures/variants.json). **Message** = student surname in **uppercase Latin letters A–Z** (e.g. `IVANOV`); full rules in [lab-praktikum-2026.md](lab-praktikum-2026.md) §1.6.

## Wokwi (labs 4, 5)

1. Open [new MicroPython ESP32 project](https://wokwi.com/projects/new/micropython-esp32).
2. Copy from `wokwi/lab04-i2c-sensor/` / `wokwi/lab05-capstone/` (`main.py`, `diagram.json`) plus `wokwi/lib/bmp180.py`.
3. Start simulation; use Serial Monitor.
4. **Logic Analyzer:** stop simulation to download `wokwi-logic.vcd`; open in PulseView — see [Wokwi Logic Analyzer Guide](https://docs.wokwi.com/guides/logic-analyzer), methodichka §1.4, and [Surfer web fallback](SETUP.md#surfer--web-fallback-lab-4) if PulseView is unavailable.

## PulseView (lab 4 — Logic Analyzer)

Wokwi exports `wokwi-logic.vcd` when you stop the simulation. Open it in **PulseView** (recommended) or GTKWave.

**Install once** — full list: [sigrok Downloads](https://sigrok.org/wiki/Downloads). Usage: [Wokwi Logic Analyzer Guide](https://docs.wokwi.com/guides/logic-analyzer).

| OS | Install |
|----|---------|
| **Windows** | Download **PulseView (64bit)** `.exe` from [sigrok Downloads](https://sigrok.org/wiki/Downloads); run installer. |
| **Linux** | Download **PulseView (64bit)** AppImage; `chmod +x pulseview-*.AppImage` then run it. Or use your distro's `pulseview` package if available. |
| **macOS** | Download **PulseView (64bit)** DMG from [sigrok Downloads](https://sigrok.org/wiki/Downloads); drag to Applications. Official build is **x86_64** (on Apple Silicon it usually runs via Rosetta). See [sigrok — Mac OS X](https://sigrok.org/wiki/Mac_OS_X). If macOS blocks launch: `xattr -cr /Applications/PulseView.app` |

**Open capture:** PulseView → **Open** → ▼ → **Import Value Change Dump data…** → `wokwi-logic.vcd` → downsampling **50** → add **I²C** decoder (lab 4: SDA=D0, SCL=D1).

**What to look for:** channels **SDA** and **SCL** (often labeled **D0**/**D1**); idle mostly high (`1`); short **bursts** of transitions = I²C transactions. With the I²C decoder you should see address **0x77** and ACK. The VCD is digital wire levels only — not Serial `TEMP=...` text.

## Surfer — web fallback (lab 4)

If PulseView is unavailable (common on newer macOS), use **[Surfer](https://surfer-project.org/)** in the browser: [app.surfer-project.org](https://app.surfer-project.org/). Drag and drop `wokwi-logic.vcd`, add channels **D0** and **D1** (SDA/SCL for lab 4). Screenshot the waveforms for your report.

**What to look for (same as PulseView, without decoder labels):** SDA/SCL mostly idle high; **bursts** of activity = I²C traffic. Surfer shows **raw digital waves only** — no I²C protocol decoder. Describe START, address, ACK, STOP in text, or rely on Serial Monitor (`I2C scan: ['0x77']`). For decoded I²C labels, prefer PulseView when it works ([Wokwi Logic Analyzer Guide](https://docs.wokwi.com/guides/logic-analyzer)).

## Virtual COM ports (lab 1)

### `--port` quick reference

| Scenario | `--port` | OS |
|----------|----------|-----|
| TX self-check | `loop://` | all |
| USB-UART | `COM3`, … | Windows |
| USB-UART | `/dev/ttyUSB0`, `/dev/ttyACM0` | Linux |
| USB-UART | `/dev/cu.usbserial-*` | macOS |
| Virtual pair (**compulsory** Host↔Device) | `COM5` / `COM6` (com0com) | Windows |
| Virtual pair (**compulsory** Host↔Device) | `/tmp/comA`, `/tmp/comB` (`uart_pty_pair` or socat) | Linux/macOS |

Examples:

```bash
python3 -m host.uart_host --message "IVANOV"              # loop:// (TX self-check)
python3 -m host.uart_host --message "IVANOV" --port COM5
python3 -m host.uart_host --message "IVANOV" --port /dev/ttyUSB0
python3 -m host.uart_host --message "IVANOV" --port /tmp/comA --wait-ack
```

**Linux/macOS** — create a linked pair (**required** for the graded exchange; no extra install):

```bash
python3 -m host.uart_pty_pair
# leave running; creates /tmp/comA ↔ /tmp/comB
```

Alternative: [socat](http://www.dest-unreach.org/socat/) (`brew install socat` on macOS):

```bash
socat -d -d pty,raw,echo=0,link=/tmp/comA pty,raw,echo=0,link=/tmp/comB
```

**Windows:** [com0com](https://com0com.sourceforge.net/) — create a linked port pair (e.g. COM5 ↔ COM6).

**TX only:** `python3 -m host.uart_host` defaults to `loop://` (echo self-check). **Lab 1 receiver is `uart_device_emu`** on the other end of the virtual pair.

### Compulsory: PC Host↔Device over virtual COM

```bash
# terminal 0 — keep the pair alive
python3 -m host.uart_pty_pair

# terminal 1 — device emulator (RX)
python3 -m host.uart_device_emu --port /tmp/comB          # Windows: --port COM6

# terminal 2 — host (TX)
python3 -m host.uart_host --message "IVANOV" --port /tmp/comA --wait-ack
```

Host prints `TX hex` and `Verify: OK` when it receives `ACK:IVANOV`. Emulator prints `--- exchange ---` with hex / ACK.

## Offline labs

Labs **1** (PC path), **2**, and **3** run offline. Labs **4** and **5** need internet for Wokwi.
