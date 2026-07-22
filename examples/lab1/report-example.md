# Приклад звіту — лабораторна робота № 1

> Зразок для **повної оцінки**: **передавач (TX, host)** + **приймач (RX, `uart_device_emu`)** через віртуальну пару COM, `Verify: OK` на `ACK:…` — без UART-графіків (лаб. 2).

---

**Титульний аркуш**

- Дисципліна: PPID  
- Лабораторна робота № 1  
- Студент: **PETRENKO**  
- Варіант: **1** (9600 8N1)

---

## 1. Мета роботи

Опанувати налаштування передавального та приймального портів, ролі TX/RX та **живий** обмін повідомленням через UART (host ↔ device на ПК).

## 2. Короткі теоретичні відомості

**Передавач (TX)** ініціює передачу — запис байтів у лінію. **Приймач (RX)** зчитує кадр і відповідає `ACK:…`. У шаблоні host формат **захардкоджено як 8N1** (парність і діаграма кадру — у лаб. 2).

У цій лабораторній: **TX** — `host/uart_host.py`; **RX** — `host/uart_device_emu.py` на другій половині віртуальної пари (`uart_pty_pair` / com0com).

**Мінімум ліній DB9:** TXD (піна 3), RXD (піна 2), GND (піна 5). У спокої лінія — логічна **1** (idle); старт символу — біт **0**.

## 3. Хід роботи

### 3.1. Параметри варіанту

| Параметр | Значення |
|----------|----------|
| Повідомлення | `PETRENKO` |
| Baudrate | 9600 |
| Формат | 8N1 (захардкоджено в host) |
| Порти | `/tmp/comA` (TX) ↔ `/tmp/comB` (RX) |

### 3.2. Передавач (host, TX)

Спочатку самоперевірка запису на `loop://` (не роль RX):

```bash
python3 -m host.uart_host --message "PETRENKO" --baud 9600 --port loop://
```

```text
TX text: 'PETRENKO'
Надіслано байт: 9
TX hex: 50 45 54 52 45 4e 4b 4f 0d
RX text (loopback): 'PETRENKO'
Verify: OK
```

Потім обмін з приймачем (термінал 2 після запуску `uart_pty_pair` і emu):

```bash
python3 -m host.uart_host --message "PETRENKO" --port /tmp/comA --wait-ack
```

```text
TX text: 'PETRENKO'
Надіслано байт: 9
TX hex: 50 45 54 52 45 4e 4b 4f 0d
RX text: 'ACK:PETRENKO'
Verify: OK
```

### 3.3. Приймач (device, RX — `uart_device_emu`) — обов’язково

```bash
python3 -m host.uart_pty_pair          # термінал 0
python3 -m host.uart_device_emu --port /tmp/comB   # термінал 1
```

Вивід emu:

```text
--- exchange ---
RX text: PETRENKO
RX bytes (9): 50 45 54 52 45 4e 4b 4f 0d
TX ACK: ACK:PETRENKO
TX bytes (13): 41 43 4b 3a 50 45 54 52 45 4e 4b 4f 0a
Verify: OK
--------------
```

**[СКРІНШОТ: два термінали — emu exchange + host Verify: OK]**

### 3.4. Порівняння TX і RX

| Сторона | Результат |
|---------|-----------|
| Host TX | `TX hex: 50 45 54 52 45 4e 4b 4f 0d` |
| Device RX | ті самі байти; відповідь `ACK:PETRENKO`; host `Verify: OK` |

### 3.5. Перша літера (підготовка до лаб. 2)

| Символ | ASCII (dec / hex) | Нагадування |
|--------|-------------------|-------------|
| `P` | 80 / `0x50` | idle = 1; старт-біт = 0; повний кадр 8N1 — у лаб. 2 |

## 4. Висновки

Реалізовано **передавач** і **приймач** на ПК через віртуальну пару COM: байти реально проходять від TX до RX і назад як ACK. Для лінії достатньо TXD/RXD/GND. UART-графіки — у лаб. 2; Wokwi ESP32 — з лаб. 4.

## 5. Додаток — текст програм

`host/uart_host.py`, `host/uart_device_emu.py`, `host/uart_pty_pair.py` — з методички.

## 6. Демонстрація

На захисті: пояснити **хто TX, хто RX**; показати live `uart_pty_pair` + emu + `uart_host --wait-ack`; назвати контакти TXD/RXD/GND.
