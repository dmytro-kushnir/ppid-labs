# PPID lab 4 — I2C environmental sensor (Wokwi)
# Wokwi files: this main.py + diagram.json (here) + bmp180.py (wokwi/lib/)
# Sensor: board-bmp180 (I2C 0x77). Course variants on real hardware: BME280.

from machine import I2C, Pin
import time

from bmp180 import BMP180

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

print("PPID Lab 4 — I2C sensor")
addrs = i2c.scan()
print("I2C scan:", [hex(a) for a in addrs])

sensor = BMP180(i2c)

while True:
    try:
        sensor.blocking_read()
        print("TEMP={:.1f} PRESS={:.1f}".format(sensor.temperature, sensor.pressure))
    except OSError as e:
        print("I2C error:", e)
    time.sleep(1)
