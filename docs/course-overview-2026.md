---
marp: true
theme: default
paginate: true
lang: uk
header: 'PPID — огляд курсу 2026'
footer: 'Львівська політехніка, кафедра ЕОМ'
style: |
  section.lead h1 { font-size: 1.6em; }
  section.lead p { font-size: 0.95em; }
  blockquote { border-left: 4px solid #666; padding-left: 1em; font-style: italic; }
  table { font-size: 0.85em; }
---

<!--
  Інструкція для викладача:
  1. Розширення "Marp for VS Code" → Open Preview → Export PDF/PPTX.
  2. Це оглядова презентація для першого заняття, не покроковий конспект лекцій.
  3. Детальний план кожної з 15 лекцій — lectures-teaching-plan-2026.md.
  4. Зображення: https://dmytro-kushnir.github.io/images/apps/ppid/ (див. Додаток).
-->

<!-- _class: lead -->

# Периферійні пристрої, інтерфейси та драйвери

**Дисципліна PPID · Комп’ютерна інженерія (КСМ)**  
Львівська політехніка · кафедра ЕОМ · 2026

---

## Мета дисципліни

Курс формує системне розуміння того, **як периферійні пристрої з’єднуються з обчислювальною системою** на рівні інтерфейсів, протоколів і програмної підтримки (драйвери, API, прикладні бібліотеки).

Після семестру студент повинен вміти:

- класифікувати інтерфейси за типом передачі, топологією та роллю в системі;
- пояснити стек підтримки периферії від firmware до прикладної програми;
- застосовувати на практиці **UART**, модель **USB-транзакції** та роботу з шиною **I²C**.

---

## Результати навчання

| Компетенція | Зміст |
|-------------|--------|
| Послідовний обмін | Кадр **8N1**, baud, parity, flow control; host (pyserial) і MCU (UART) |
| USB | Топологія зірка, endpoints, типи передач; відмінність ФС від device driver |
| Шини MCU | Порівняння CAN, SPI, I²C; адресація, підключення на embedded-платах |
| Магістралі ПК | Еволюція ISA → PCIe; NVMe vs SATA |
| Введення/виведення | HID, DP/HDMI, USB Audio — рівень класів пристроїв |

---

## Структура семестру (15 лекцій)

| № | Тема | Практикум |
|---|------|-----------|
| 1 | RS-232C, UART, COM-драйвери | лаб. 1, 2 |
| 2 | USB: транзакції, драйвери | лаб. 2, 3 |
| 3 | CL, CAN | — |
| 4 | MIL-STD-1553B | — |
| 5 | SPI | — |
| 6 | I²C | лаб. 4, 5 |
| 7 | Q-BUS, ISA, EISA | — |
| 8 | PCI, PCIe, AGP | — |
| 9 | Centronics, IEEE-488 | — |
| 10 | ATA, SATA, SCSI | — |
| 11 | Аналогові периферійні пристрої | — |
| 12 | Драйвери зовнішніх ЗП | — |
| 13 | Драйвери введення | — |
| 14 | Драйвери виведення | — |
| 15 | Мовлення (введення/виведення) | — |

Детальний план кожної лекції — `lectures-teaching-plan-2026.md`.

---

## Навчальні матеріали

| Документ | Призначення |
|----------|-------------|
| `lectures.pdf` | Офіційний конспект лекцій (2025) |
| `lectures-supplement-2026.md` | Оновлення після 2025: USB-C, PCIe, embedded, DP/HDMI |
| `lectures-teaching-plan-2026.md` | План проведення 15 лекцій (для викладача) |
| `lab-praktikum-2026.md` | Повний practicum (5 лаб; блоки A–C, [індекс програм](lab-praktikum-2026.md#appendix-c)) |
| Сайт курсу | `/#/peripheral-devices/` |

Репозиторій з кодом і прикладами: [github.com/dmytro-kushnir/ppid-labs](https://github.com/dmytro-kushnir/ppid-labs)

---

## Класифікація інтерфейсів

Терміни **UK / EN** — *simplex*, *half-duplex*, *full-duplex*, *serial*, *parallel*, *asynchronous*, *synchronous*.

### За напрямком передачі (duplex)

| Режим (UK / EN) | Приклади в курсі |
|-----------------|------------------|
| Симплекс / *simplex* | Датчик → MCU (один напрям) |
| Напівдуплекс / *half-duplex* | RS-485, CAN, I²C |
| Повний дуплекс / *full-duplex* | RS-232 (TX/RX), SPI, USB |

### За способом передачі бітів (serial vs parallel)

| Тип (UK / EN) | Приклади | Лекції |
|---------------|----------|--------|
| Послідовний / *serial* | RS-232, USB, CAN, SPI, I²C | 1–6 |
| Паралельний / *parallel* | Centronics, GPIB | 9 |
| Магістраль / *bus* | ISA, PCI, PCIe, CAN, I²C | 3, 7–8 |

### За топологією

| Топологія (UK / EN) | Приклад | Лекція |
|---------------------|---------|--------|
| Point-to-point | RS-232, USB host–device | 1–2 |
| Шина / *bus* | CAN, I²C, RS-485 | 1, 3, 6 |
| Зірка / *star* | USB hub, PCIe root complex | 2, 8 |

---

## Рівні програмної підтримки

<!-- IMAGE: піраміда firmware → driver → API → lib → app -->

![Рівні ПЗ](https://dmytro-kushnir.github.io/images/apps/ppid/placeholder-driver-stack.png)

```text
Периферійний пристрій
    → firmware
    → драйвер ядра ОС
    → API операційної системи
    → прикладні бібліотеки (pyserial, HID API)
    → програма користувача
```

**Приклад (USB-флешка):** `write()` → ФС (ext4/NTFS) → block layer → `usb-storage` → xHCI → USB bus.

**Приклад (UART на Pi):** `read()` на `/dev/ttyAMA0` → tty driver → UART SoC → GPIO TX/RX.

На лабораторних — **pyserial** / API ОС; на MCU — регістри UART або HAL.

---

## Платформи embedded

<!-- IMAGE: фото RPi + ESP32 + Jetson з підписами портів -->

![Embedded плати](https://dmytro-kushnir.github.io/images/apps/ppid/placeholder-embedded-boards.png)

| Платформа | OS | Інтерфейси PPID |
|-----------|-----|-----------------|
| **Raspberry Pi 4/5** | Linux | USB, GbE, HDMI, GPIO UART/SPI/I²C, PCIe (Pi 5) |
| **ESP32** | FreeRTOS / Arduino | UART, SPI, I²C, CAN (TWAI), USB-CDC (S2/S3) |
| **Jetson Nano** | Linux (ARM) | USB 3, GbE, HDMI, GPIO UART/SPI/I²C, M.2 |
| **STM32 Nucleo** | bare-metal / RTOS | USART, SPI, I²C, CAN, USB device |

Лабораторні PPID — на ПК і в Wokwi; лекції 3–6 — теорія для підключення на макетці.

---

<!-- _class: lead -->

# Блок A
## Комунікаційні порти (лекції 1–2)

---

## RS-232 / UART

**Кадр (типово 8N1):** `START(0)` → 8 data bits (LSB first) → parity (опц.) → `STOP(1)`  
Час біта: **T = 1 / baud** (напр. 115200 бод → ≈8,7 мкс на біт)

<!-- IMAGE: осцилограма кадру UART -->

![RS-232](https://dmytro-kushnir.github.io/images/apps/ppid/placeholder-rs232-timing.png)

| Де зустрінете | Інтерфейс |
|---------------|-----------|
| Лаб. 1 (ПК + Wokwi) | pyserial, ESP32 `machine.UART` |
| Raspberry Pi | `/dev/ttyAMA0`, `/dev/serial0` |
| ESP32 / STM32 | `Serial`, `HAL_UART`, USB-UART на Nucleo |
| Промисловість | **RS-485** (диференційна пара, шина) |

Flow control: **RTS/CTS** (апаратний) або XON/XOFF (програмний).

---

## USB: host, device, endpoints

Топологія **зірка**; обмін — **транзакції** (Token → Data → Handshake).

<!-- IMAGE: Token → Data → Handshake -->

![USB](https://dmytro-kushnir.github.io/images/apps/ppid/placeholder-usb-transaction.png)

| Поняття | Зміст |
|---------|--------|
| **Endpoint** | Адресована черга IN/OUT (напр. bulk EP1) |
| **Descriptor** | Опис пристрою, конфігурації, endpoints |
| **Transfer types** | control, **bulk** (флешка), interrupt (HID), isochronous (аудіо) |
| **NRZI** | Кодування **USB 2.0**; SuperSpeed — **8b/10b**; USB4 — **128b/132b** |

**RPi/Jetson** — USB **host**; **ESP32-S3** — USB **device** (CDC).

---

## USB-C і сучасні покоління USB

| Сигнал / роль | Призначення |
|---------------|-------------|
| **VBUS** | Живлення 5 V (PD — до 240 Вт EPR) |
| **CC1/CC2** | Орієнтація кабеля, роль host/device, PD negotiation |
| **D+/D−** | USB 2.0 |
| **SSTX± / SSRX±** | SuperSpeed (USB 3.x) |

<!-- IMAGE: піни USB-C -->

![USB-C](https://dmytro-kushnir.github.io/images/apps/ppid/placeholder-usb-c-ports.png)

| Покоління | Швидкість (огляд) |
|-----------|-------------------|
| USB 2.0 | до 480 Мбіт/с, NRZI |
| USB 3.2 Gen 2×2 | до 20 Гбіт/с |
| USB4 / USB4 2.0 | до 40 / 80 Гбіт/с |

**DRP** на ноутбуці: заряджання або живлення периферії. **Alt mode:** DisplayPort, Thunderbolt.

---

<!-- _class: lead -->

# Практикум 2026
## П’ять лабораторних робіт

---

## Склад практикуму

Практикум містить **5 лабораторних**. Фізичне залізо не обов’язкове.

| Лаб | Тема | Лекції | Інструменти |
|-----|------|--------|-------------|
| 1 | UART host ↔ device (віртуальна пара) | 1 | pyserial, `uart_device_emu` |
| 2 | Діаграми UART та NRZI | 1–2 | matplotlib, pytest |
| 3 | Модель USB 2.0 (mock) | 2 | Python, tkinter |
| 4 | Шина I²C | 6 | Wokwi, Logic Analyzer |
| 5 | Capstone: датчик → UART → ПК | 1, 6 | Wokwi + CSV/графік |

Повна методичка: `lab-praktikum-2026.md` — **Вступ → Частина I → блоки A–C** (теорія, лаби, зразки звітів, лістинги програм) → додатки A–D.

---

## Повідомлення та варіанти

**Повідомлення** для лаб. **1–3** і запису в mock USB (лаб. 3) — **прізвище студента** великими **латинськими** літерами A–Z (без пробілів; транслітерація).

| Ситуація | Приклад |
|----------|---------|
| Прізвище «Ivanov» | `IVANOV` |
| Подвійне прізвище | без пробілу: `IVANOVPETRENKO` |

Технічні параметри (baud, parity, stop bits) — за **номером варіанту** з таблиці в practicum.

---

## Стек технологій

| Компонент | Технологія |
|-----------|------------|
| Мова / середовище | **Python 3.11+**, MicroPython (Wokwi) |
| Послідовний порт | **pyserial**, `machine.UART` |
| Діаграми | **matplotlib**, **`signal_gui`** (PNG) |
| Mock USB | tempfile, tkinter |
| Порти / симуляція | Wokwi, com0com, socat, `loop://` |

Звіт базується на **доказах виконання**: скріни програм, програмні графіки, логи. Ручні flowchart не обов’язкові.

**Важливо:** лаб. 3 моделює USB-транзакцію в user space — це **не** kernel device driver. Запис у temp-директорію — рівень файлової системи.

---

<!-- _class: lead -->

# Блок B
## Польові шини (лекції 3–6)

---

## CAN, SPI, I²C — порівняння

<!-- IMAGE: CAN bus -->

![CAN](https://dmytro-kushnir.github.io/images/apps/ppid/placeholder-can-bus.png)

| Інтерфейс | Топологія | Ключові сигнали | Типове застосування |
|-----------|-----------|-----------------|---------------------|
| **CAN** | Шина, арбітраж | CAN_H, CAN_L | Авто ECU, робототехніка |
| **SPI** | Master–slave | MOSI, MISO, SCK, CS | Flash, дисплей, радіо |
| **I²C** | Шина, адресація | SDA, SCL | Сенсори, EEPROM, RTC |

**CAN:** домінантний `0` перемагає рецесивний `1`; bit stuffing; CAN FD — більший payload.

**SPI:** режими CPOL/CPHA 0–3; окремий **CS** на кожен slave.

**I²C:** open-drain, pull-up 2.2–4.7 kΩ; **clock stretching**; адреса 7 біт.

---

<!-- _class: lead -->

# Блок C
## Магістралі ПК (лекції 7–10)

---

## Еволюція магістралей і накопичувачів

<!-- IMAGE: PCIe + M.2 -->

![PCIe](https://dmytro-kushnir.github.io/images/apps/ppid/placeholder-pcie-nvme.png)

| Етап | Інтерфейс | Статус |
|------|-----------|--------|
| Міні/ПК 1980–90-х | Q-BUS, ISA, EISA | історичні (лек. 7) |
| Розширення ПК | PCI → **PCIe** (лек. 8) | сучасний стандарт |
| Накопичувачі | ATA → SATA → **NVMe** (лек. 10) | NVMe поверх PCIe |

| SATA SSD | NVMe SSD |
|----------|----------|
| Кабель, AHCI | M.2, PCIe |
| ~600 МБ/с | Гігабайти/с |

Драйвер блочного пристрою ≠ драйвер **файлової системи** (лек. 12).

---

## Паралельні інтерфейси (лекція 9)

**Centronics** — паралельний порт принтера (legacy; заміна USB і мережею).

**IEEE-488 (GPIB)** — лабораторні осцилографи та джерела живлення; у нових системах — **USB** або **LXI (Ethernet)**.

---

<!-- _class: lead -->

# Блок D
## Введення та виведення (лекції 11–15)

---

## Аналогові сигнали (лек. 11)

- **АЦП / ЦАП** — перетворення між аналоговим датчиком і цифровим процесором.
- **I²S / PDM** — цифрова передача аудіо між мікросхемами.
- Застосування: звукові карти, IoT, PLC (4–20 мА).

---

## Введення (лек. 13) і виведення (лек. 14)

**Введення:** USB **HID** — стандартні дескриптори для клавіатури, миші, геймпада; ОС обробляє без драйвера від виробника.

**Виведення:** принтери (CUPS, IPP); відео — **HDMI 2.1** / **DisplayPort 2.1** через GPU (DRM/KMS), не COM-порт.

<!-- IMAGE: HDMI, DP, USB-C на ноутбуці -->

![DP HDMI](https://dmytro-kushnir.github.io/images/apps/ppid/placeholder-dp-hdmi.png)

Ноутбук → USB-C → монітор: **DisplayPort alt mode**.

---

## Мовлення (лек. 15)

- **USB Audio Class** — гарнітура «plug-and-play».
- Ланцюг: мікрофон → АЦП → обробка → ASR/TTS (сучасні системи — ML у хмарі або на пристрої).

---

## Мережеві інтерфейси (огляд)

Ethernet **не входить** до 15 лекцій PDF; деталі TCP/IP — курс «Комп’ютерні мережі».

| Рівень | Аналогія в PPID |
|--------|-----------------|
| NIC на PCIe | периферія на магістралі (лек. 8) |
| Драйвер NIC | як USB Mass Storage driver |
| `socket()` у програмі | як `write()` на `E:\` |

Периферія по мережі: IPP-принтер, NAS, LXI-прилад. Промисловість: EtherCAT, PROFINET (поруч із CAN).

---

<!-- _class: lead -->

# Організація навчання

---

## Чеклист готовності до захисту

- [ ] Лаб. 1: `uart_device_emu` + host `--wait-ack`; скріни та логи (без обов’язкових flowchart)
- [ ] Лаб. 2: 2 PNG (UART + NRZI); `pytest tests/`
- [ ] Лаб. 3: USB-транзакція + mock GUI; **чому це не kernel driver**
- [ ] Лаб. 4: I²C scan + Logic Analyzer у Wokwi
- [ ] Лаб. 5: capstone — датчик → UART → CSV/графік на ПК
- [ ] Порівняння USB-A і USB-C (лаб. 3)
- [ ] Відповіді на питання самоперевірки з practicum і supplement

---

## Порядок роботи з матеріалами

1. **Ця презентація** — загальна карта курсу (перше заняття).
2. **Supplement, класифікація** — перед кожною новою темою.
3. **`lectures.pdf`, лекція N** — базова теорія для заліку.
4. **`lectures-teaching-plan-2026.md`** — план заняття (для викладача).
5. **`lab-praktikum-2026.md`** — виконання лабораторних.

На заліку оцінюється **розуміння** інтерфейсів і рівнів ПЗ, а не заучування назв застарілого обладнання.

---

## Питання для самоперевірки

1. Розпишіть кадр **8N1** і час передачі байта при baud = 9600.
2. Чим **bulk endpoint** USB відрізняється від **interrupt**? Де на Pi — Mass Storage?
3. Датчик на **I²C** vs **SPI**: коли оберете кожен для IMU на ESP32?

Відповіді: лекції 1–2, 5–6, supplement «Платформи embedded».

---

<!-- _class: lead -->

# Питання?

**Викладач:** Парамуд Ярослав Степанович  
**Кафедра ЕОМ** · Львівська політехніка

[Сайт курсу](https://dmytro-kushnir.github.io/#/peripheral-devices/)  
[Документація курсу](https://github.com/dmytro-kushnir/ppid-labs/tree/main/docs)

---

# Додаток: перелік ілюстрацій

Замініть PNG на сайті (`public/images/apps/ppid/` у репозиторії dmytro-kushnir.github.io):

| Файл | Що вставити |
|------|-------------|
| `placeholder-driver-stack.png` | Піраміда: firmware → driver → API → app |
| `placeholder-rs232-timing.png` | Осцилограма кадру UART |
| `placeholder-usb-transaction.png` | Token–Data–Handshake |
| `placeholder-usb-c-ports.png` | Схема USB-C: CC, VBUS, D+/D− |
| `placeholder-can-bus.png` | CAN bus або ECU |
| `placeholder-pcie-nvme.png` | PCIe слот + M.2 NVMe |
| `placeholder-dp-hdmi.png` | Порти ноутбука або док-станція |
| `placeholder-embedded-boards.png` | RPi + ESP32 + Jetson з підписами |

*Оновлена версія: академічний огляд курсу, практикум 2026.*
