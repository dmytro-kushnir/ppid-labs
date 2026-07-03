# Examples index

Per-lab guides for the PPID 2026 practicum. Full methodology (reports, questions, variant table): **[docs/lab-praktikum-2026.md](../docs/lab-praktikum-2026.md)** — блоки A (лаб. 1–2), B (лаб. 3), C (лаб. 4–5).

| Lab | Folder | Guide | Приклад звіту |
|-----|--------|-------|---------------|
| **1** UART host↔device | [`lab1/`](lab1/) | [`lab1/lab1.md`](lab1/lab1.md) | [`lab1/report-example.md`](lab1/report-example.md) |
| **2** UART + NRZI plots | [`lab2/`](lab2/) | [`lab2/lab2.md`](lab2/lab2.md) | [`lab2/report-example.md`](lab2/report-example.md) |
| **3** USB model | [`lab3/`](lab3/) | [`lab3/lab3.md`](lab3/lab3.md) | [`lab3/report-example.md`](lab3/report-example.md) |
| **4** I²C sensor | [`lab4/`](lab4/) | [`lab4/lab4.md`](lab4/lab4.md) | [`lab4/report-example.md`](lab4/report-example.md) |
| **5** Capstone | [`lab5/`](lab5/) | [`lab5/lab5.md`](lab5/lab5.md) | [`lab5/report-example.md`](lab5/report-example.md) |

## Provided vs student work

| Provided in repo | Student delivers |
|------------------|------------------|
| UART/USB Python modules, Wokwi templates, reference GUIs (`signal_gui`, `usb_gui`) | Completed variant, **screenshots + generated PNG/logs** |
| `fixtures/variants.json` | Technical params per variant number; message = your surname (Latin A–Z) |
| pytest baseline | Defence demo, self-check answers |
| Diagram references in `docs/diagrams/` | Optional reading only (not mandatory report figures) |

Report model: see practicum §1.3 — evidence-based (screenshots, generated plots, logs, code).

## Quick start

```bash
pip install -r requirements.txt -r requirements-dev.txt
python3 -m pytest tests/ -v
```

See [docs/SETUP.md](../docs/SETUP.md) for Wokwi and virtual COM setup.
