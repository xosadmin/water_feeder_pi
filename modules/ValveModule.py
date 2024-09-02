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
    GPIO.setup(self.pin, GPIO.out)
    self.close()

  def open(self):
    if self.state == 'closed':
      GPIO.output(self.pin, GPIO.HIGH)
      self.state = 'open'
      print(f"Valve opened.")
    
  def close(self):
    if self.state == 'open':
      GPIO.output(self.pin, GPIO.LOW)
      self.state = 'closed'
      print(f"Valve closed.")

  def cleanup(self):
    GPIO.cleanup(self.pin)
