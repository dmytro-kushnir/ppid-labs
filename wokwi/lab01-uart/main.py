# PPID lab 1 — UART echo on ESP32 (Wokwi MicroPython)
# Import this folder into https://wokwi.com/projects/new/micropython-esp32

import time

from machine import Pin, UART

BAUD = 9600
uart = UART(1, baudrate=BAUD, tx=17, rx=16, timeout=100)
led = Pin(2, Pin.OUT)
led.value(0)


def bytes_hex(data: bytes) -> str:
    return " ".join("{:02x}".format(b) for b in data)


def blink_led(times: int = 3) -> None:
    for _ in range(times):
        led.value(1)
        time.sleep_ms(120)
        led.value(0)
        time.sleep_ms(80)


def send_ack(line: str) -> None:
    rx_packet = (line + "\r").encode("utf-8")
    ack = "ACK:" + line
    tx_packet = ack.encode("utf-8") + b"\r\n"

    print("--- verify ---")
    print("RX text:", line)
    print("RX bytes UTF-8 ({}): {}".format(len(rx_packet), bytes_hex(rx_packet)))
    written = uart.write(tx_packet)
    print("TX ACK:", ack)
    print("UART1 TX GPIO17 ({} B): {}".format(written, bytes_hex(tx_packet)))
    if ack == "ACK:" + line and written == len(tx_packet):
        print("Verify: OK")
    else:
        print("Verify: FAIL")
    print("--------------")

    blink_led()


print("PPID Lab 1 — UART device ready")
print("Baud:", BAUD, "| UART1 TX=GPIO17 RX=GPIO16 | LED=GPIO2")

while True:
    line = input("Enter your message: ").strip()
    if line:
        send_ack(line)
