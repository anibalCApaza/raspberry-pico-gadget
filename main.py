#   RST - Reset:                     Pico GP8 (11)
#   CE - Chip Enable / Chip select : Pico GP5 ( 7)
#   DC - Data/Command :              Pico GP4 ( 6)
#   Din - Serial Input (Mosi):       Pico GP7 (10)
#   Clk - SPI Clock:                 Pico GP6 ( 9)
#   Vcc:                             Pico 3V3 (36)
#   BL :                             Pico GP9(12)
#   Gnd:                             Pico GND (38)

import pcd8544_fb
import time
import machine

spi = machine.SPI(0)

spi = machine.SPI(
    0, baudrate=2000000, polarity=0, phase=0, sck=machine.Pin(6), mosi=machine.Pin(7)
)

cs = machine.Pin(5)
dc = machine.Pin(4)
rst = machine.Pin(8)

bl = machine.Pin(9, machine.Pin.OUT, value=1)

lcd = pcd8544_fb.PCD8544_FB(spi, cs, dc, rst)


# Código configurable


class TemperatureDisplay:
    def __init__(self) -> None:
        self.sensor_temp = machine.ADC(4)
        self.conversion_factor = 3.3 / (65535)

    def display_temp(self, string_temperature: str):
        lcd.text("-NerdCave-", 2, 0, 1)
        lcd.text(string_temperature, 0, 12, 1)
        lcd.clear()
        lcd.show()
        time.sleep(2)

    def read_temp(self) -> str:
        reading = self.sensor_temp.read_u16() * self.conversion_factor
        temperature = 27 - (reading - 0.706) / 0.001721
        formatted_temperature = "{:.2f}".format(temperature)
        string_temperature = str("Temp:" + formatted_temperature)
        print(string_temperature)

        return string_temperature


if __name__ == "__main__":
    temperature_display = TemperatureDisplay()
    while True:
        temperature = temperature_display.read_temp()
        temperature_display.display_temp(temperature)
        lcd.fill(0)
