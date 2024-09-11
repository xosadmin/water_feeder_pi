"""
File: TurbidityModule
Author: Hanxun

This is to use digital method to get turbidty. For backup purposes only.

Description:
"""
import RPi.GPIO as GPIO

class TurbidityModule_dig:
    def __init__(self, id, sensor_pin, output_pin):
        self.id = id
        self.sensor_pin = sensor_pin
        self.output_pin = output_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)
        GPIO.setup(self.output_pin, GPIO.OUT)

    def get_turbidity(self):
        turbidity_state = GPIO.input(self.sensor_pin)
        if turbidity_state == GPIO.LOW:
            print(f"Turbidity Sensor {self.id}: High turbidity detected.")
            GPIO.output(self.output_pin, GPIO.HIGH)
            return 1 # High
        else:
            print(f"Turbidity Sensor {self.id}: Low turbidity detected.")
            GPIO.output(self.output_pin, GPIO.LOW)
            return 0 # Low

    def cleanup(self):
        GPIO.cleanup()
