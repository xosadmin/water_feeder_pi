import paho.mqtt.client as mqtt

class MQTTModule:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.client = mqtt.Client()  # Initialize MQTT client
        self.client.on_message = self.on_message  # Set on_message callback function

    def connect(self):
        self.client.connect(self.server, self.port)  # Connect to MQTT server
        self.client.loop_start()  # Start the network loop

    def send_message(self, topic, value):
        self.client.publish(topic, value)  # Publish value to specific topic
        print(f"Message sent to topic {topic}: {value}")

    def receive_message(self, topic):
        self.client.subscribe(topic)  # Subscribe to a topic
        print(f"Subscribed to topic: {topic}")

    def on_message(self, client, userdata, msg):
        # Callback function when a message is received
        print(f"{msg.payload.decode('utf-8')}")

    def disconnect(self):
        self.client.loop_stop()  # Stop the network loop
        self.client.disconnect()  # Disconnect from MQTT


"""
Usage: mqtt_module.send_message(topic, value) 
Topic: The sensor related to your function. 
- The topic syntax: <sensor_name>
- For example: Turbity Sensor: turbiditysensor

All available sensor topics:
- Turbity Sensor: turbiditysensor
- Valve: valve
- Waste water level: waterlevelwaste

If you cannot find your sensor, please post on Teams so that be registered.

on_message = function to stand by and waiting for remote command from Cloud VM.

"""