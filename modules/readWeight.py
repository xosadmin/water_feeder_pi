"""
File: readWeight.py
Description: Get the weight of the object using HX711 sensor
Reference: https://github.com/DFRobot/DFRobot_HX711_I2C
"""

import sys
import time
from .DFRobot_HX711_I2C import *

class readWeight:
    def __init__(self, iic_mode=0x03, iic_address=0x64, calibration_value=223.7383270263672):
        self.iic_mode = iic_mode
        self.iic_address = iic_address
        self.calibration_value = calibration_value
        self.hx711 = DFRobot_HX711_I2C(self.iic_mode, self.iic_address)

    def begin(self):
        """Initialize the sensor."""
        self.hx711.begin()
        self.hx711.set_calibration(self.calibration_value)
        self.hx711.peel()  # Initialize or reset

    def read_weight(self, samples=50):
        try:
            weight = self.hx711.read_weight(samples)
            # if weight < 0:
            #     weight = 0.00
            return weight
        except KeyboardInterrupt:
            print("\nMeasurement stopped by user.")
