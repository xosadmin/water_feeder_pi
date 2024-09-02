"""
File: PumpModule
Author: Mike Bernal
Description: Turn on/off water pump based on the following conditions:
1. TODO If bowl valve is open, turn on.
2. TODO If bowl valve is closed, turn off.
3. TODO If water waste tank is full, turn off
4. DONE Manually on/off pump
5. DONE Get pump status
6. DONE Continously monitor pump status at certain interval
"""
import RPi.GPIO as GPIO
from time import sleep
class PumpModule:
  def __init__(self, pin):
    self.pin = pin
    self.pins_set = False
    # Set GPIO interface
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
    self.pins_set = True

    # Pump initially turned off
    GPIO.output(self.pin, GPIO.LOW)

  def start(self):
    GPIO.output(self.pin, GPIO.HIGH)
    

  def stop(self):
    GPIO.output(self.pin, GPIO.LOW)

  def get_status(self):
    return GPIO.input(self.pin)
  
  def monitor_status(self):
    try:
      while True:
        pump_status = self.get_status()
        print(f"Pump status: {'ON' if pump_status else 'OFF'}")
        sleep(5)
    except KeyboardInterrupt:
      print("Force stopping pump")
    finally:
      self.cleanup()

  def cleanup(self):
    if self.pins_set:
      GPIO.cleanup(self.pin)
      self.pins_set = False
