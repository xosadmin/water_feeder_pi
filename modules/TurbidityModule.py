"""
File: TurbidityModule
Author: Hanxun
Description:
"""
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class TurbidityModule:
    def __init__(self, id, sensor_channel):
        self.id = id
        self.sensor_channel = sensor_channel
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)

        if self.sensor_channel == 0:
            self.chan = AnalogIn(self.ads, ADS.P0) #A0
        elif self.sensor_channel == 1:
            self.chan = AnalogIn(self.ads, ADS.P1) #A1
        elif self.sensor_channel == 2:
            self.chan = AnalogIn(self.ads, ADS.P2) #A2
        elif self.sensor_channel == 3:
            self.chan = AnalogIn(self.ads, ADS.P3) #A3
        else:
            raise ValueError("Invalid sensor channel. Use 0-3 for ADS1115 channels.")
        
    def map_value(self, value, left_min, left_max, right_min, right_max):
        left_span = left_max - left_min
        value_scaled = (value - left_min) / left_span

        right_span = right_max - right_min
        result = right_min + (value_scaled * right_span)
        if result < 0:
            result = 0.00
        return result

    def read_turbidity(self):
        voltage = self.chan.voltage
        scaled_value = -1120.4 * voltage ** 2 + 5742.3 * voltage - 4352.9
        mapped_value = self.map_value(scaled_value, 0, 3000, 0, 6)
        return f'{mapped_value:.2f}'
