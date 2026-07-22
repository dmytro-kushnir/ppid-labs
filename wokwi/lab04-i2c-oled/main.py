# PPID lab 4 (OLED variants 4, 6, 9) — I2C SSD1306 display (Wokwi)
# Wokwi files: this main.py + diagram.json (here) + ssd1306.py (wokwi/lib/)
# Display: wokwi-ssd1306 (I2C 0x3C). Task: show your surname (Latin A-Z).

from machine import I2C, Pin
import time

from ssd1306 import SSD1306_I2C

# TODO: replace with your surname in Latin letters (variants.json message rule).
SURNAME = "IVANOV"

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

print("PPID Lab 4 — I2C OLED")
addrs = i2c.scan()
print("I2C scan:", [hex(a) for a in addrs])

oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)
oled.text("PPID Lab 4", 0, 0)
oled.text("I2C OLED 0x3C", 0, 16)
oled.text(SURNAME, 0, 40)
oled.show()
print("OLED: shown", SURNAME)

while True:
    time.sleep(1)
