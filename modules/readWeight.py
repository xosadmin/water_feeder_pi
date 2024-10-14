"""
File: readWeight.py
Description: Get the weight of the object using HX711 sensor
Reference: https://github.com/DFRobot/DFRobot_HX711_I2C
"""

import sys
from time import sleep
from .DFRobot_HX711_I2C import *

class readWeight:
    def __init__(self, iic_mode=0x03, iic_address=0x64, calibration_value=223.7383270263672):
        self.iic_mode = iic_mode
        self.iic_address = iic_address
        self.calibration_value = calibration_value
        self.hx711 = DFRobot_HX711_I2C(self.iic_mode, self.iic_address)
        self.last_valid_weight = 0  # Store the last valid weight

    def begin(self):
        """Initialize the sensor."""
        try:
            self.hx711.begin()
            self.hx711.set_calibration(self.calibration_value)
            self.hx711.peel()  # Initialize or reset
        except Exception as e:
            print(f"Error initializing HX711 sensor: {e}")
            sys.exit(1)

    def read_weight(self, samples=50, retry_limit=3):
        """Read weight from the sensor with retries."""
        attempt = 0
        while attempt < retry_limit:
            try:
                weight = self.hx711.read_weight(samples)
                if weight < 0:
                    weight = 0.00  # Correct negative weight values
                self.last_valid_weight = weight  # Store the last valid weight
                return weight
            except OSError as e:
                print(f"Error reading weight: {e}, attempt {attempt + 1} of {retry_limit}")
                attempt += 1
                sleep(0.1)  # Short delay before retrying

        print(f"Failed to read weight after {retry_limit} attempts, using last valid weight.")
        return self.last_valid_weight  # Return the last valid weight if retries fail

    def average_weight(self, num_samples=10, threshold=50):
        """Calculate average weight over multiple samples, ensuring 10 valid readings."""
        weights = []
        attempts = 0
        max_attempts = num_samples * 2  # Allow up to twice the number of attempts

        while len(weights) < num_samples and attempts < max_attempts:
            weight = self.read_weight()
            if weight is not None:
                weights.append(weight)
            else:
                print("Invalid reading, retrying...")
            attempts += 1
            sleep(0.1)

        # If no valid weights were collected
        if len(weights) == 0:
            print("No valid weight readings.")
            return 0  # Return 0 if no valid readings

        # Proceed with outlier filtering and averaging
        median = sorted(weights)[len(weights) // 2]
        filtered_weights = [w for w in weights if abs(w - median) < threshold]

        if len(filtered_weights) > 0:
            average = sum(filtered_weights) / len(filtered_weights)
            print(f"Averaged weight (with outlier filtering): {average}")
            return average
        else:
            print("No valid weight readings after filtering.")
            return 0
