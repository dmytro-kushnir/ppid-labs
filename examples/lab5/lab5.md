# Лабораторна робота № 5: Capstone — вузол моніторингу

## Мета

Інтегрувати I²C (датчик) → UART (`TEMP=...`) → host (CSV + графік) у міні-систему моніторингу.

> **Повна методичка:** [lab-praktikum-2026.md](../../docs/lab-praktikum-2026.md)

## Що використовуємо в цій лабі

| | |
|---|---|
| Embedded | [Wokwi MicroPython ESP32](https://wokwi.com/projects/new/micropython-esp32) |
| Датчик на схемі | **BMP180** (`board-bmp180`), I²C **0x77** |
| Файли Wokwi | `main.py` + `diagram.json` з [lab05-capstone/](../../wokwi/lab05-capstone/) + `bmp180.py` з [wokwi/lib/](../../wokwi/lib/bmp180.py) |
| Host | [host/capstone_host.py](../../host/capstone_host.py) |

> Інтервал опитування — поле `poll_ms` у [variants.json](../../fixtures/variants.json) → змініть `INTERVAL_MS` у `main.py`. Поле `sensor` = `BME280` — тип завдання; **у Wokwi завжди BMP180** (як у лаб. 4).

## Архітектура

Скопіюйте діаграму у звіт (не малюйте від руки). Детальніше: [docs/diagrams/capstone-components.md](../../docs/diagrams/capstone-components.md).

```mermaid
flowchart LR
  BMP[BMP180] -->|I2C| ESP[ESP32]
  ESP -->|UART TEMP=...| Log[Serial log]
  Log --> Host[capstone_host.py]
  Host --> CSV[CSV]
  Host --> Plot[plot PNG]
```

## Кроки

### 1. Embedded у Wokwi

1. Відкрити [Wokwi MicroPython ESP32](https://wokwi.com/projects/new/micropython-esp32).
2. Створити **три файли** з репозиторію:
   - `main.py` ← [wokwi/lab05-capstone/main.py](../../wokwi/lab05-capstone/main.py)
   - `diagram.json` ← [wokwi/lab05-capstone/diagram.json](../../wokwi/lab05-capstone/diagram.json)
   - `bmp180.py` ← [wokwi/lib/bmp180.py](../../wokwi/lib/bmp180.py)
3. У `main.py` виставити `INTERVAL_MS` = `poll_ms` вашого варіанту.
4. **▶ Start** — у Serial Monitor:

```text
PPID Lab 5 — Capstone node
I2C: ['0x77']
TEMP=...
TEMP=...
```

5. **Опційно:** клацніть **BMP180** → слайдери temperature — змініть кілька разів, щоб у логу були різні `TEMP=` (графік буде змістовніший).
6. Скопіюйте вивід Serial Monitor у файл **`my_log.txt`** у корені репозиторію (або поруч з ним). У файлі мають бути рядки саме у форматі `TEMP=...` — інакше host нічого не знайде.

### 2. Host: лог → CSV + графік

З кореня репозиторію:

```bash
python3 -m host.capstone_host --input my_log.txt --plot capstone_plot.png --csv readings.csv
```

Очікуваний вивід:

```text
Знайдено зчитувань: …
CSV: readings.csv
Графік: capstone_plot.png
```

У звіті: фрагмент `my_log.txt`, файл/таблиця `readings.csv`, скрін `capstone_plot.png`.

Опційно (як лаб. 3): додати `--export-usb`.

> Якщо host «не бачить» зчитувань — перевірте, що в `my_log.txt` є рядки `TEMP=22.1` (без зайвих пробілів у префіксі). Для швидкої перевірки самої програми можна тимчасово: `python3 -m host.capstone_host --input sample_log.txt` ([sample_log.txt](../../sample_log.txt)).

### 3. У звіті обов’язково

1. Діаграма компонентів (mermaid вище) + коротко шари ПЗ ([ARCHITECTURE.md](../../docs/ARCHITECTURE.md)).
2. Фрагмент Serial log (`I2C: ['0x77']`, рядки `TEMP=...`).
3. CSV (`readings.csv`) + графік PNG.
4. Висновок: де драйвер датчика (прошивка), де парсер на ПК; навіщо однаковий формат `TEMP=...`.

## Зміст звіту (чеклист)

1. Мета.
2. Діаграма компонентів + шари ПЗ.
3. Хід роботи: `my_log.txt`, `readings.csv`, `capstone_plot.png`.
4. Висновки (драйвери / узгодження `TEMP=...`).
5. Додаток — `main.py` / `capstone_host` (з методички).
6. Демонстрація: Wokwi live TEMP → host → графік.

> **Приклад звіту:** [report-example.md](report-example.md)
