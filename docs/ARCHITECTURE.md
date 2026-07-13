# Software layers (PPID labs)

| Level | Example | Labs |
|-------|---------|------|
| Protocol model | NRZI, Token/Data/Handshake | 2, 3 |
| HAL / library | pyserial; `machine.UART` / `machine.I2C` (Wokwi) | 1; 4–5 |
| OS API | `pathlib`, `tempfile`, tkinter | 2 (reference GUI), 3, 5 |
| Physical bus (simulated) | Wokwi Logic Analyzer | 4 |

## Lab 1: host ↔ device

```
Python host (uart_host)  ←→  virtual COM pair (uart_pty_pair / com0com)  ←→  uart_device_emu
```

`loop://` is TX self-check only. Reference GUI `host/signal_gui.py` is for lab 2.
## Lab 2: signal visualization

```
encoding/uart_plot.py, encoding/usb_nrzi.py  ←→  CLI or host/signal_gui.py (reference)
```

## Lab 3: USB levels

```
Your Python model (usb_transaction.py)     — educational byte-level OUT transaction
Mock enumeration (fixtures/usb_devices.json) — stands in for lsusb / Device Manager
GUI + tempfile                             — stands in for Mass Storage filesystem API
(usb_gui: scan + device properties panel)
```

Real USB device drivers live in the OS kernel; this practicum does not implement them.

## Lab 5: capstone

```
BME280 → I2C → ESP32 firmware → UART → host parser → CSV + matplotlib → optional mock USB export
```

See [diagrams/capstone-components.md](diagrams/capstone-components.md).
