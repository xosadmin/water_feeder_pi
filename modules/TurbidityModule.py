"""
File: TurbidityModule
Author: Hanxun
Description:
"""
import RPi.GPIO as GPIO

class TurbidityModule:
  def __init__(self, id, pin):
    self.id = id
    self.pin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.pin, GPIO.IN)

  def get_turbidity(self):
    # Work here
    pass

  def cleanup(self):
    GPIO.cleanup()
