"""
File: RFIDModule.py
Author: Jean Wang
Description: Identify pets that approach the water feeder and track their water consumptions
"""

import time
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from datetime import datetime
import logging
from .readWeight import readWeight
from .httpModule import HTTPModule

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class RFIDModule:
    def __init__(self,server_address):
        self.reader = SimpleMFRC522()
        self.tag_present = False
        self.start_time = None
        self.debounce_time = 0.5
        self.current_id = None
        self.water_weight = readWeight()
        self.water_weight.begin()
        self.http = HTTPModule(server=server_address)

    def read_rfid(self):
        try:
            while True:
                id, _ = self.reader.read_no_block()
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
            time.sleep(1)
            self.start_weight = self.water_weight.read_weight()
            logging.info(f'{id} starts drinking water')
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
        time.sleep(1)
        self.end_weight = self.water_weight.read_weight()
        self.duration = self.end_time - self.start_time
        logging.info(f'{self.current_id} stops drinking water')
        logging.info(f'Total time: {self.duration}')
        consumption = round(self.start_weight - self.end_weight,2)
        logging.info(f'Total consumption: {consumption} ml')
        self.http.uploadDrinkData(self.current_id,consumption)

    def cleanup(self):
        GPIO.cleanup()
        logging.info("GPIO cleanup completed")
