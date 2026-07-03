# Лабораторна робота № 2: Візуалізація UART та USB NRZI

## Мета

Побудувати амплітудно-часові діаграми UART і NRZI для заданого повідомлення; розрахувати час передачі.

> **Повна методичка:** [lab-praktikum-2026.md](../../docs/lab-praktikum-2026.md)  
> **Повідомлення:** ваше **прізвище латиницею** (те саме, що в лаб. 1).  
> **Baudrate:** з [variants.json](../../fixtures/variants.json) за номером варіанту

## Теоретичні відомості (стисло)

1. **T_такт = 1 / baudrate**; символ UART = старт + дані + парність? + стоп.
2. Між символами в завданні — пауза **1 такт**.
3. **NRZI (USB 2.0):** 0 → зміна рівня, 1 → без зміни; **bit stuffing** після 6 одиниць.

## Що в репозиторії

| Шлях | Призначення |
|------|-------------|
| [encoding/uart_plot.py](../../encoding/uart_plot.py) | Діаграма UART, розрахунок часу |
| [encoding/usb_nrzi.py](../../encoding/usb_nrzi.py) | NRZI + bit stuffing, графік |
| [host/signal_gui.py](../../host/signal_gui.py) | **Довідковий** GUI: UART + NRZI, **експорт PNG** |
| [tests/test_usb_nrzi.py](../../tests/test_usb_nrzi.py) | Перевірка NRZI |

## Кроки

```bash
python3 -m encoding.uart_plot --message "IVANOV" --baud 9600
python3 -m encoding.usb_nrzi --message "IVANOV"
python3 -m host.signal_gui
python3 -m pytest tests/test_usb_nrzi.py -v
```

1. Побудувати діаграми для **всього** повідомлення варіанту.
2. Експортувати **2 PNG** (UART + NRZI) — з CLI або кнопкою «Save PNG» у `signal_gui`.
3. Розрахувати час передачі UART.
4. У звіті порівняти NRZI (USB 2.0) з 8b/10b (USB 3.x) — supplement лекція 2.

## Формула часу

```text
T_символ = (1 + N_даних + парність? + N_стоп) × (1 / baudrate)
T_повідомлення ≈ n_символів × T_символ + паузи
```

## Зміст звіту

Мета, теорія, **2 PNG** (UART + NRZI), розрахунок часу, код, демонстрація.

> **Приклад звіту:** [report-example.md](report-example.md)
