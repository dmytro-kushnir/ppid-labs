# Приклад звіту — лабораторна робота № 1

> Зразок для **повної оцінки**: явно розділені **передавач (TX, host)** і **приймач (RX, Wokwi)**, verify, скріни — без UART-графіків (лаб. 2).

---

**Титульний аркуш**

- Дисципліна: PPID  
- Лабораторна робота № 1  
- Студент: **PETRENKO**  
- Варіант: **1** (9600 8N1)

---

## 1. Мета роботи

Опанувати налаштування передавального та приймального портів, ролі TX/RX та модель обміну повідомленням через UART (host + ESP32 у Wokwi).

## 2. Короткі теоретичні відомості

**Передавач (TX)** ініціює передачу — запис байтів у лінію. **Приймач (RX)** зчитує кадр до `\r`. Параметри **baud, format** мають збігатися на обох сторонах.

У цій лабораторній: **TX** — `host/uart_host.py` (ПК); **RX** — прошивка ESP32 у Wokwi.

## 3. Хід роботи

### 3.1. Параметри варіанту (однакові для TX і RX)

| Параметр | Значення |
|----------|----------|
| Повідомлення | `PETRENKO` |
| Baudrate | 9600 |
| Формат | 8N1 |
| Порт host (TX) | `loop://` |

### 3.2. Передавач (host, TX)

Програма `host/uart_host.py`, функція `send_message()`.

```bash
python3 -m host.uart_host --message "PETRENKO" --baud 9600 --port loop://
```

Вивід:

```text
TX text: 'PETRENKO'
Надіслано байт: 9
TX hex: 50 45 54 52 45 4e 4b 4f 0d
RX text (loopback): 'PETRENKO'
Verify: OK
```

Роль TX: формування пакета `прізвище + \r`, запис у послідовний порт.

### 3.3. Приймач (device, RX — Wokwi ESP32)

Програма `wokwi/lab01-uart/main.py` — прийом рядка, verify, відповідь `ACK:...`.

На запит `Enter your message:` введено `PETRENKO`. Serial Monitor:

```text
Enter your message: PETRENKO
--- verify ---
RX text: PETRENKO
RX bytes UTF-8 (9): 50 45 54 52 45 4e 4b 4f 0d
TX ACK: ACK:PETRENKO
Verify: OK
--------------
```

**[СКРІНШОТ: Wokwi — Serial Monitor, блок verify, LED GPIO2, Logic Analyzer D0 на GPIO17]**

Роль RX: прийом повідомлення на device, перевірка цілісності, індикація LED.

### 3.4. Модель обміну

| Напрям | Хто | Результат |
|--------|-----|-----------|
| Host → Device | TX (`send_message`) | байти на лінії |
| Device → Host | RX відповідає `ACK:PETRENKO` | підтвердження |

Повідомлення на обох сторонах збігається; host — `Verify: OK`.

### 3.5. Опційно — loopback без Wokwi

```bash
python3 -m host.uart_loopback_demo
```

TX і RX в одному процесі на `loop://` — для перевірки без COM-драйверів (не замінює демонстрацію приймача на ESP32).

## 4. Висновки

Реалізовано **передавач** (host, pyserial) та **приймач** (ESP32, MicroPython). Окремі два застосунки на ПК не потрібні — друга сторона обміну це MCU. Блок verify підтверджує цілісність даних. UART-графіки — у лаб. 2.

## 5. Додаток — текст програм

`host/uart_host.py`, `host/uart_loopback_demo.py`, `wokwi/lab01-uart/main.py` — з методички.

## 6. Демонстрація

На захисті: пояснити **хто TX, хто RX**; показати Wokwi (приймач) + `uart_host` (передавач) з `Verify: OK`.
