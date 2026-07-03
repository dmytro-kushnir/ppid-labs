# Приклад звіту — лабораторна робота № 3

> Зразок для **повної оцінки**: hex транзакції, mock-скан, скрін GUI, порівняння USB-A / USB-C, пояснення рівня ФС.

---

**Титульний аркуш**

- Дисципліна: PPID  
- Лабораторна робота № 3  
- Студент: **PETRENKO**  
- Варіант: **1** (mock USB: SanDisk Cruzer Mass Storage)

---

## 1. Мета роботи

Опанувати транзакцію USB 2.0 (Token → Data → Handshake), mock-сканування пристроїв і передачу даних на рівні моделі та файлової системи.

## 2. Короткі теоретичні відомості

**Транзакція USB 2.0 (OUT):** Host → Token (OUT) → Data (DATA0) → Handshake (ACK).

**Порівняння роз’ємів:**

| Контакт / функція | USB-A (типовий) | USB-C (оглядово) |
|-------------------|-----------------|------------------|
| Живлення | VBUS, GND | VBUS, GND |
| Дані | D+, D− | TX/RX пари (симетрично) |
| Роль host/device | фіксована | CC1/CC2 (PD) |
| Кількість контактів | 4 (+ shield) | 24 |

**Рівень ПЗ:** запис через `usb_gui` у `tempfile` — **файлова система**, не kernel USB device driver.

## 3. Хід роботи

### 3.1. Параметри варіанту

| Параметр | Значення |
|----------|----------|
| Повідомлення | `PETRENKO` |
| Mock-пристрій | SanDisk Cruzer (Mass Storage) |
| VID:PID | 0781:5567 |

### 3.2. Побудова транзакції (hex)

```bash
python3 -m host.usb_transaction --message "PETRENKO"
```

Вивід:

```text
Фази: TOKEN → DATA → HANDSHAKE
Пакет 1: e1 81 00
Пакет 2: c3 50 45 54 52 45 4e 4b 4f e7 f4
Пакет 3: d2
```

Пояснення: пакет 2 містить ASCII-байти `PETRENKO` (`50 45 54 52 45 4E 4B 4F`) у полі DATA.

### 3.3. Mock-сканування

```bash
python3 -m host.usb_scan
```

```text
Mock USB enumeration (fixtures/usb_devices.json):
...
0781:5567 Mass Storage @ 480 Mbps (High Speed) — SanDisk Cruzer (Mass Storage)
...
```

У реальній системі аналог: `lsusb` (Linux) або Диспетчер пристроїв (Windows).

### 3.4. GUI — скан, властивості, запис

```bash
python3 -m host.usb_gui
```

Дії: **Сканувати** → обрати **SanDisk Cruzer** → переглянути VID:PID, class, volume/format → записати `PETRENKO` у `.txt`.

**[СКРІНШОТ: вікно `usb_gui` — listBox з mock-пристроями після «Сканувати», панель властивостей SanDisk (Mass Storage, FAT32, 16 GB), повідомлення про успішний запис у temp-директорію]**

### 3.5. Структура транзакції (схема)

```text
Host ──Token OUT──► Device
Host ──Data DATA0──► Device   (payload: PETRENKO)
Host ◄──Handshake ACK── Device
```

NRZI-кодування для цих даних наведено в лабораторній роботі № 2.

## 4. Висновки

Реалізовано модель USB-транзакції та mock-enumeration. Запис через GUI — рівень ФС, не драйвер пристрою. USB-C додає CC-лінії та симетричні пари для SuperSpeed; USB-A — класична 4-контактна схема D+/D−.

## 5. Додаток — текст програм

Лістинги `host/usb_transaction.py`, `host/usb_scan.py`, `host/usb_gui.py` — з методички.

## 6. Демонстрація

На захисті: hex-дамп + `usb_gui` (скан → запис) + пояснити, чому це не kernel driver.
