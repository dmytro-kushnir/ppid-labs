# PPID course documentation

Markdown materials for **Peripheral Devices, Interfaces and Drivers** (LPNU).

| Document | Description |
|----------|-------------|
| [lab-praktikum-2026.md](lab-praktikum-2026.md) | **Практикум 2026** — Вступ, блоки A–C (теорія → лаби → зразки звітів → програми), додатки A–D; [індекс програм](lab-praktikum-2026.md#appendix-c) |
| [lab-praktikum-2026.template.md](lab-praktikum-2026.template.md) | Шаблон practicum (`{{include:…}}`); не редагуйте `.md` вручну |
| [lectures-supplement-2026.md](lectures-supplement-2026.md) | Lectures supplement — classification, embedded platforms, USB-C, DP/HDMI |
| [lectures-teaching-plan-2026.md](lectures-teaching-plan-2026.md) | **План проведення 15 лекцій** (для викладача) |
| [course-overview-2026.md](course-overview-2026.md) | Marp presentation for the first class |
| [SETUP.md](SETUP.md) | Environment setup for this repo |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Software layers (host / device / USB mock) |
| [diagrams/](diagrams/) | Reusable Mermaid diagrams |

Per-lab quick guides: [examples/](../examples/).

### Оновлення practicum

Лістинги програм підставляються з файлів репозиторію:

```bash
python3 scripts/build_standalone.py              # згенерувати lab-praktikum-2026.md
python3 scripts/build_standalone.py --check      # CI: перевірити актуальність
```

Після зміни `host/`, `encoding/`, `wokwi/` або шаблону — перезапустіть збірку.
