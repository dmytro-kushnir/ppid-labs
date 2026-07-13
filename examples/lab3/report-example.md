# Приклад звіту — лабораторна робота № 3

> Зразок для **повної / максимальної оцінки**: hex транзакції, mock-скан, скрін GUI + `cat` у temp, **запис на реальну флешку** ([lab3.md](lab3.md) §6), коротка таблиця USB-A / USB-C, пояснення рівня ФС.

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

Пояснення пакета 2 (Data DATA0):

- Payload: **8 байт** (довжина `PETRENKO`; мінімум у програмі — 8, коротші прізвища доповнюються `\x00`).
- ASCII у DATA: `50 45 54 52 45 4E 4B 4F`.
- Після payload — CRC (`e7 f4`); на початку пакета — PID DATA0 (`c3`).
- Ті самі ASCII-байти, що в `TX hex` лаб. 1 і на діаграмах лаб. 2.

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

Дії: **Сканувати** → обрати **SanDisk Cruzer (Mass Storage)** → переглянути VID:PID, class, volume/format → у поле ввести `PETRENKO` → **Записати на mock-накопичувач**.

Список пристроїв у GUI — з `fixtures/usb_devices.json` (mock), не сканування USB-портів ПК.

Після «Готово» програма показала шлях, наприклад:

```text
Записано на SanDisk Cruzer (Mass Storage):
/var/folders/.../T/ppid_usb_g6ktqg22/message.txt
```

Перевірка вмісту (GUI ще відкритий):

```bash
cat /var/folders/.../T/ppid_usb_g6ktqg22/message.txt
```

```text
PETRENKO
```

Тобто записано **прізвище** у файл `message.txt` у temp-теці `ppid_usb_*` — рівень **ФС**, не передача по USB-шині.

**[СКРІНШОТ: вікно `usb_gui` — combobox з mock-пристроями, панель властивостей SanDisk (Mass Storage, FAT32, 16 GB), діалог «Готово» з повним шляхом до `message.txt`]**

### 3.5. Запис на реальну флешку (для максимальної оцінки)

Вставлено USB-накопичувач. Власний скрипт знайшов removable-томи, наприклад:

```text
/Volumes/NO NAME
```

Властивості обраного тома:

| Поле | Приклад |
|------|---------|
| Шлях / буква | `/Volumes/NO NAME` |
| Мітка | `NO NAME` або ваша мітка |
| Формат | `FAT32` / `exFAT` / … |
| Розмір / вільно | напр. 14.9 ГБ / 14.8 ГБ |

Записано прізвище і перевірено:

```bash
# шляхи — приклади; у звіті — ваші
cat "/Volumes/NO NAME/message.txt"
```

```text
PETRENKO
```

**[СКРІНШОТ: список removable-томів + властивості + Finder/Explorer з `message.txt`]**

Це той самий рівень **ФС**, що й `ppid_usb_*`: ОС уже має драйвер Mass Storage; студентський код лише пише файл на змонтований том.

### 3.6. Структура транзакції (схема)

```text
Host ──Token OUT──► Device
Host ──Data DATA0──► Device   (payload: PETRENKO)
Host ◄──Handshake ACK── Device
```

NRZI-кодування для цих даних наведено в лабораторній роботі № 2.

## 4. Висновки

Реалізовано модель USB-транзакції (hex) та mock-enumeration. Запис у temp і на **реальну флешку** — рівень файлової системи, не USB device driver у ядрі. USB-C додає CC-лінії; USB-A — схема контактів D+/D−.

## 5. Додаток — текст програм

Лістинги `host/usb_transaction.py`, `host/usb_scan.py`, `host/usb_gui.py` — з методички.

## 6. Демонстрація

На захисті: hex-дамп + `usb_gui` (скан → запис → `cat` у temp) + **запис на флешку** (removable → `message.txt` → `cat` на томі) + пояснити, чому і temp, і флешка — рівень **ФС**, не kernel USB driver. Див. [lab3.md](lab3.md) §6.

> Без флешки — здача можлива за кроками 1–4, але **не максимальна** оцінка.
