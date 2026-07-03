# PPID lab 5 — Capstone: I2C sensor + UART telemetry (Wokwi)
# Wokwi files: this main.py + diagram.json (here) + bmp180.py (wokwi/lib/)

from machine import I2C, Pin, UART
import time

from bmp180 import BMP180

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
uart = UART(1, baudrate=9600, tx=17, rx=16)
INTERVAL_MS = 500

sensor = BMP180(i2c)

print("PPID Lab 5 — Capstone node")
print("I2C:", [hex(a) for a in i2c.scan()])

while True:
    try:
        sensor.blocking_read()
        line = "TEMP={:.1f}\r\n".format(sensor.temperature)
        uart.write(line.encode("utf-8"))
        print(line.strip())
    except OSError as e:
        print("ERR:", e)
    time.sleep_ms(INTERVAL_MS)
