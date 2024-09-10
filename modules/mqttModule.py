import paho.mqtt.client as mqtt
import requests

class MQTTModule:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.client = mqtt.Client()  # Initialize MQTT client

    def connect(self):
        self.client.connect(self.server, self.port)  # Connect to MQTT server

    def send_message(self, topic, value):
        self.client.publish(topic, value)  # Public Value to specific Topic

    def disconnect(self):
        self.client.disconnect()  # Disconnect from MQTT

"""
Usage: mqtt_module.send_message(topic, value) 
Topic: The sensor related to your function. 
- The topic syntax: sensor/<sensor_name>/<location(optional)>
- For example: Turbity Sensor in Bowl: sensor/TurbiditySensor_Bowl
- For example: Valve: sensor/valve

All available sensor topics:
- Turbity Sensor in bowl: sensor/TurbiditySensor_Bowl
- Valve: sensor/valve
- Waste water level: sensor/waterlevel/waste
- Turbity Sensor in water tank: sensor/TurbiditySensor_WaterTank

If you cannot find your sensor, please post on Teams so that be registered.

"""