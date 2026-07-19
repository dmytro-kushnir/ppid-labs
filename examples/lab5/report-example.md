# Приклад звіту — лабораторна робота № 5

> Зразок для **повної оцінки**: діаграма компонентів, Serial log (`0x77`, `TEMP=...`), CSV, графік PNG, пояснення шарів ПЗ.

---

**Титульний аркуш**

- Дисципліна: PPID  
- Лабораторна робота № 5 (capstone)  
- Студент: **PETRENKO**  
- Варіант: **1** (poll 500 ms, 9600 8N1)

---

## 1. Мета роботи

Інтегрувати I²C (датчик), UART (телеметрія `TEMP=...`) та host-обробку (CSV, графік) у вузол моніторингу.

## 2. Короткі теоретичні відомості та діаграма компонентів

**Шари ПЗ (від датчика до CSV):**

```text
BMP180 (периферія)
  → HAL I²C (machine.I2C, прошивка)
  → застосунок ESP32 (формування TEMP=...)
  → UART / Serial
  → log-файл (my_log.txt)
  → capstone_host (парсинг, CSV, matplotlib)
  → (опційно) mock USB FS
```

**Діаграма компонентів (з методички):**

```mermaid
flowchart LR
  BMP[BMP180] -->|I2C| ESP[ESP32]
  ESP -->|UART TEMP=...| Log[Serial log]
  Log --> Host[capstone_host]
  Host --> CSV[CSV]
  Host --> Plot[plot PNG]
```

## 3. Хід роботи

### 3.1. Параметри

| Параметр | Значення |
|----------|----------|
| Датчик (Wokwi) | BMP180 (`board-bmp180`), адреса **0x77** |
| Інтервал опитування | 500 ms (`INTERVAL_MS`) |
| Формат телеметрії | `TEMP=<value>\r\n` |
| UART | 9600 8N1 |

### 3.2. Embedded (Wokwi)

Файли: `main.py`, `diagram.json`, `bmp180.py`. Збережено Serial Monitor у `my_log.txt`:

```text
PPID Lab 5 — Capstone node
I2C: ['0x77']
TEMP=22.1
TEMP=22.3
TEMP=22.5
TEMP=22.4
TEMP=22.8
```

**[СКРІНШОТ: Wokwi capstone — Serial Monitor з рядками TEMP=...]**

### 3.3. Host — парсинг, CSV, графік

```bash
python3 -m host.capstone_host --input my_log.txt --plot capstone_plot.png --csv readings.csv
```

Вивід:

```text
Знайдено зчитувань: 5
CSV: readings.csv
Графік: capstone_plot.png
```

**[СКРІНШОТ: графік matplotlib — вісь X: номер зчитування, вісь Y: температура °C; файл `capstone_plot.png`]**

Фрагмент `readings.csv`:

```text
sample,temp_c
2,22.1
3,22.3
4,22.5
```

**[СКРІНШОТ або фрагмент: відкритий CSV у редакторі / таблиця в звіті]**

### 3.4. Опційно — export mock USB

```bash
python3 -m host.capstone_host --input my_log.txt --plot capstone_plot.png --csv readings.csv --export-usb
```

CSV копіюється у temp-директорію mock Mass Storage (аналог лаб. 3).

## 4. Висновки

Capstone об’єднує UART (лаб. 1–2) та I²C (лаб. 4). Драйвер датчика — у прошивці (`bmp180.py` / `machine.I2C`); на ПК — лише парсинг `TEMP=...` і візуалізація. Узгоджений формат рядка між ESP32 і `capstone_host` потрібен для коректного CSV.

## 5. Додаток — текст програм

Лістинги `wokwi/lab05-capstone/main.py`, `host/capstone_host.py` — з методички.

## 6. Демонстрація

На захисті: Wokwi (live TEMP) → `capstone_host` → показати `capstone_plot.png` і пояснити шари ПЗ.
