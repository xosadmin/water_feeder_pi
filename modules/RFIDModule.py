"""
File: RFIDModule.py
Author: Jean Wang
Description: 
"""
import RPi.GPIO as GPIO

class RFIDModule:
  def __init__(self, pin):
    self.pin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.pin, GPIO.IN)
  
  def read_rfid(self):
    # Work here
    pass
  
  def cleanup(self):
    GPIO.cleanup()