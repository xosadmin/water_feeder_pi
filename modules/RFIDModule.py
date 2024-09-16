"""
File: RFIDModule.py
Author: Jean Wang
Description: 
"""
import time
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class RFIDModule:
  def __init__(self):
    self.reader = SimpleMFRC522()
    self.tag_present = False
    self.start_time = None
    self.debounce_time = 0.5
    #assumptions will be replaced by actual readings
    self.intake_assumption = 30 # ml per minute
    self.tag_log = {635397131568: 'Harry', 383923372645: 'Ron', 427562945950: 'Draco'}
    self.current_id = None

  def read_rfid(self):
    try:
      while True:
        id, text = self.reader.read_no_block()  
        if id:
          self.tag_detected(id)
        else:
          self.tag_absent()
        time.sleep(0.1)
    except KeyboardInterrupt:
      logging.info("Program stopped by user")

  def tag_detected(self, id):
    if not self.tag_present:
      self.tag_present = True
      self.start_time = datetime.now()
      name = self.tag_log.get(id, "Unknown")
      logging.info(f'{name} starts drinking water')
      self.current_id = id

  def tag_absent(self):
    if self.tag_present:
      time.sleep(self.debounce_time)
      id_check, _ = self.reader.read_no_block()
      if not id_check:
        self.calculate_consumption()
        self.tag_present = False
        self.start_time = None

  def calculate_consumption(self):
    self.end_time = datetime.now()
    self.duration = self.end_time - self.start_time
    name = self.tag_log.get(self.current_id, "Unknown")
    logging.info(f'{name} stops drinking water')
    logging.info(f'Total time: {self.duration}')
    #assumptions will be replaced by actual readings
    consumption = self.duration.total_seconds() / 60 * self.intake_assumption
    logging.info(f'Total consumption: {consumption:.2f} ml')

  def cleanup(self):
    GPIO.cleanup()
    logging.info("GPIO cleanup completed")
