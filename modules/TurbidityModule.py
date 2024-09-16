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

    def read_turbidity(self):
        scaled_value = int((self.chan.voltage * 1023) / 5.0)
        return f'{scaled_value:.2f}'
