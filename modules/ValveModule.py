"""
File: ValveModule
Author: Mike Bernal
Description: This module controls the valves using RPi.GPIO library.
"""
import RPi.GPIO as GPIO

class ValveModule:
  def __init__(self, pin):
    self.pin = pin
    self.state = 'closed'
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(self.pin, GPIO.OUT)
    self.close()  # Initialize with valve closed

  def open(self):
    if self.state == 'closed':
      GPIO.output(self.pin, GPIO.HIGH)
      self.state = 'open'
      print("Valve opened.")
  
  def close(self):
    if self.state == 'open':
      GPIO.output(self.pin, GPIO.LOW)
      self.state = 'closed'
      print("Valve closed.")
  
  def get_status(self):
    return self.state

  def cleanup(self):
    GPIO.cleanup()
    print("Valve GPIO cleaned up.")
