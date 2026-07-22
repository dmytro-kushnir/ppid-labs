# Shared Wokwi MicroPython modules

**`bmp180.py`** — I²C driver for `board-bmp180` (labs 4 and 5, sensor variants).

**`ssd1306.py`** — I²C driver for `wokwi-ssd1306` OLED at `0x3C` (lab 4 OLED variants 4, 6, 9).

In Wokwi, create **File → New file → `<driver>.py`** and paste the module you need next to `main.py` and `diagram.json` from the lab folder:

| Variant type | Lab folder | Driver |
|--------------|-----------|--------|
| Sensor (BME280/BMP180) | `lab04-i2c-sensor/`, `lab05-capstone/` | `bmp180.py` |
| OLED (variants 4, 6, 9) | `lab04-i2c-oled/` | `ssd1306.py` |

Full listing in methodichka **E.4** (block C, appendix).
