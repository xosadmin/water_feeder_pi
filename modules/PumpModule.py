"""
File: PumpModule
Author: 
Description: Turn on/off water pump based on the following conditions:
1. If bowl valve is open, turn on.
2. If bowl valve is closed, turn off.
3. If water waste tank is full, turn off
"""
import RPi.GPIO as GPIO

class PumpModule:
  def __init__(self, pin):
    self.pin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.pin, GPIO.IN)

  def start(self):
    # Work here
    pass

  def stop(self):
    # Work here
    pass

  def get_status(self):
    # Work here
    pass

  def cleanup(self):
    GPIO.cleanup()