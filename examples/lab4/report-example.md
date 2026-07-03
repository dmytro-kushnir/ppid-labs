# Приклад звіту — лабораторна робота № 4

> Зразок для **повної оцінки**: адреса I²C, Serial Monitor, скрін Logic Analyzer, порівняння I²C/SPI.

---

**Титульний аркуш**

- Дисципліна: PPID  
- Лабораторна робота № 4  
- Студент: **PETRENKO**  
- Варіант: **1** (датчик BME280, 9600 8N1 для UART — контекст capstone)

---

## 1. Мета роботи

Опанувати master–slave I²C: адресація, читання температури з I²C-датчика (BMP180 у Wokwi; BME280 на реальному залізі), аналіз SDA/SCL у Logic Analyzer.

## 2. Короткі теоретичні відомості

**I²C:** синхронна шина, лінії **SDA** (дані) та **SCL** (такт). Один master (ESP32), один або кілька slaves (BMP180/BME280).

**Транзакція:** START → адреса 7 біт + R/W → ACK → дані/регістри → STOP.

**Порівняння з SPI:**

| Критерій | I²C | SPI |
|----------|-----|-----|
| Дроти | 2 (+ GND) | 4+ (MOSI, MISO, SCK, CS) |
| Адресація | на шині (7 біт) | окремий CS на пристрій |
| Швидкість | нижча (100–400 kHz типово) | вища, потокові дані |

## 3. Хід роботи

### 3.1. Параметри варіанту

| Параметр | Значення |
|----------|----------|
| Датчик (Wokwi) | BMP180 (`board-bmp180`) |
| Датчик (варіант курсу) | BME280 |
| Адреса I²C (Wokwi) | **0x77** |
| Шина | SDA=GPIO21, SCL=GPIO22, 100 kHz |

### 3.2. Wokwi — scan та читання

Після запуску симуляції (`main.py` + `bmp180.py` + `diagram.json`):

```text
PPID Lab 4 — I2C sensor
I2C scan: ['0x77']
TEMP=24.0 PRESS=1013.2
TEMP=24.0 PRESS=1013.2
...
```

**[СКРІНШОТ: Wokwi — Serial Monitor з `I2C scan: ['0x77']` та TEMP/PRESS, board-bmp180 на схемі]**

### 3.3. Logic Analyzer

Під час симуляції Wokwi записав сигнали на **D0 (SDA)** та **D1 (SCL)**. Після Stop завантажено `wokwi-logic.vcd`. Файл відкрито в **PulseView** з декодером **I²C** (див. §1.4 методички, [Wokwi Logic Analyzer Guide](https://docs.wokwi.com/guides/logic-analyzer)). Альтернатива без встановлення — **[Surfer](https://surfer-project.org/)** у браузері ([app.surfer-project.org](https://app.surfer-project.org/)): сирий перегляд SDA/SCL, опис протоколу в тексті звіту. Під час `i2c.scan()` видно START, адресу `0x77`, ACK, STOP.

**[СКРІНШОТ: PulseView або Surfer — SDA/SCL (або рядок декодера I²C) під час адресації 0x77]**

### 3.4. Драйвер BMP180 (`bmp180.py`)

Окремий модуль — **драйвер пристрою** (I²C-протокол BMP180). У `main.py` лише `from bmp180 import BMP180` та цикл опитування. Це не Arduino Library Manager — у MicroPython бібліотека = файл `.py` у проєкті Wokwi.

## 4. Висновки

На шині виявлено BMP180 за адресою **0x77**. ESP32 — master; датчик — slave. Logic Analyzer підтверджує коректну адресацію. I²C зручніший за SPI за кількістю дротів.

## 5. Додаток — текст програми

Лістинги `main.py`, `bmp180.py`, `diagram.json` — з методички (блок C).

## 6. Демонстрація

На захисті: Wokwi live — `scan`, читання TEMP, показ Logic Analyzer.
