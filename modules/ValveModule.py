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
    self.close()

  def open(self):
    GPIO.output(self.pin, GPIO.HIGH)
    self.state = 'open'
    print("Valve opened.")

  def close(self):
    GPIO.output(self.pin, GPIO.LOW)
    self.state = 'closed'
    print("Valve closed.")

  def get_status(self):
    return self.state

  def cleanup(self):
    GPIO.cleanup(self.pin)
    print("Valve GPIO cleaned up.")
