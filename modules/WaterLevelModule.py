"""
File: ValveModule
Author: Jias
Description:
"""
import RPi.GPIO as GPIO

class WaterLevelModule:
  def __init__(self, pin):
    self.pin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.pin, GPIO.out)

  def is_low(self):
    # Work here
    pass

  def get_water_level(self):
    # Work here
    pass

  def cleanup(self):
    GPIO.cleanup(self.pin)
