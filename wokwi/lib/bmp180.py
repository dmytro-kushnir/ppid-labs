# BMP180 driver for MicroPython (based on robert-hh/BMP085_BMP180, MIT)
# Wokwi: board-bmp180 (I2C 0x77). Real hardware course variants: BME280.

from ustruct import unpack as unp
import time


class BMP180:
    def __init__(self, i2c):
        self._i2c = i2c
        self._addr = 0x77
        self._delays = (7, 8, 14, 28)
        self._sign = time.ticks_diff(1, 0)
        cal = unp(
            ">hhhHHHhhhhh",
            self._i2c.readfrom_mem(self._addr, 0xAA, 22),
        )
        (self._AC1, self._AC2, self._AC3, self._AC4, self._AC5, self._AC6,
         self._B1, self._B2, self._MB, self._MC, self._MD) = cal
        self._oversample = 2
        self._ut = bytearray(2)
        self._mlx = bytearray(3)
        self._cmd = bytearray(1)
        self._B5 = 0
        self._gauge = self._make_gauge()
        for _ in range(128):
            next(self._gauge)
            time.sleep_ms(1)

    def _make_gauge(self):
        while True:
            self._cmd[0] = 0x2E
            self._i2c.writeto_mem(self._addr, 0xF4, self._cmd)
            t0 = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), t0) * self._sign <= 5:
                yield None
            self._i2c.readfrom_mem_into(self._addr, 0xF6, self._ut)

            self._cmd[0] = 0x34 | (self._oversample << 6)
            self._i2c.writeto_mem(self._addr, 0xF4, self._cmd)
            t0 = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), t0) * self._sign <= self._delays[self._oversample]:
                yield None
            self._i2c.readfrom_mem_into(self._addr, 0xF6, self._mlx)
            yield True

    def blocking_read(self):
        while next(self._gauge) is None:
            pass

    @property
    def temperature(self):
        next(self._gauge)
        x1 = ((unp(">H", self._ut)[0] - self._AC6) * self._AC5) >> 15
        x2 = (self._MC << 11) // (x1 + self._MD)
        self._B5 = x1 + x2
        return ((self._B5 + 8) >> 4) / 10.0

    @property
    def pressure(self):
        self.temperature
        up = (((self._mlx[0] << 16) + (self._mlx[1] << 8) + self._mlx[2])
              >> (8 - self._oversample))
        b6 = self._B5 - 4000
        x1 = (self._B2 * ((b6 * b6) >> 12)) >> 11
        x2 = (self._AC2 * b6) >> 11
        b3 = (((self._AC1 * 4 + x1 + x2) << self._oversample) + 2) >> 2
        x1 = (self._AC3 * b6) >> 13
        x2 = (self._B1 * ((b6 * b6) >> 12)) >> 16
        x3 = ((x1 + x2) + 2) >> 2
        b4 = (self._AC4 * (x3 + 32768)) >> 15
        b7 = (up - b3) * (50000 >> self._oversample)
        p = (b7 * 2) // b4
        x1 = (((p >> 8) * (p >> 8)) * 3038) >> 16
        x2 = (-7357 * p) // 65536
        return (p + (x1 + x2 + 3791) // 16) / 100
