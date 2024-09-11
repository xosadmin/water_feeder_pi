# TODO: Import your module here
import os
from modules import WaterLevelModule, TurbidityModule
from modules import mqttModule
import time
import threading

class WaterFeeder:
    def __init__(self, waste_water_level_sensor, turbidity_sensor, mqtt_client):
        # Set your module as member here
        self.waste_water_level_sensor = waste_water_level_sensor
        self.turbidity_sensor = turbidity_sensor
        self.mqtt_client = mqtt_client
        # GET WATER FEEDER INITIAL DATA
        self.monitoring = True
        self.get_sensor_data()

        self.mqtt_client.client.subscribe("remotecommand")
        self.mqtt_client.client.on_message = self.on_message

    def get_sensor_data(self):
        waste_water_level = self.waste_water_level_sensor.get_water_level()
        turbidity_value = turbidity_sensor.read_turbidity()
        sensor_location = self.waste_water_level_sensor.sensor_location
        ntu_id = self.turbidity_sensor.id

        print(waste_water_level)
        print(f"Turbidity Level: {turbidity_value}")
        self.mqtt_client.send_message(f"sensor/waterlevel/{sensor_location}", str(waste_water_level))
        self.mqtt_client.send_message(f"sensor/{ntu_id}", str(turbidity_value))

    # def monitor_waste_water_level(self):
    #     while self.monitoring:
    #         waste_water_level = self.waste_water_level_sensor.get_water_level()
    #         sensor_location = self.waste_water_level_sensor.sensor_location
    #         print(f"Monitoring - Water Level: {waste_water_level}") # The sensor code need to adjust before uncomment these codes
    #         time.sleep(5)

    def monitor_waste_water_level(self):
        self.waste_water_level_sensor.monitor_water_level()

    def monitor_turbidity_level(self):
        while self.monitoring:
            turbidity_value = turbidity_sensor.read_turbidity()
            print(f"Monitoring - Turbidity Level: {turbidity_value}")
            time.sleep(1)

    def start_monitoring(self):
        # self.water_level_thread = threading.Thread(target=self.monitor_waste_water_level)
        # self.water_level_thread.daemon = True
        # self.water_level_thread.start()

        self.turbidity_thread = threading.Thread(target=self.monitor_turbidity_level)
        self.turbidity_thread.daemon = True
        self.turbidity_thread.start()

    def on_message(self, client, userdata, message):
        # Callback function for handling MQTT messages.
        topic = message.topic
        payload = message.payload.decode('utf-8')

        if topic == "remotecommand":
            if payload == "0":
                print("No command specified.")
            elif payload == "changewater":
                pass
                self.mqtt_client.send_message("remotecommand", "0") # Clear the status of remotecommand
            elif payload == "refillwater":
                pass
                self.mqtt_client.send_message("remotecommand", "0") # Clear the status of remotecommand
            elif payload == "restartfeeder":
                self.mqtt_client.send_message("remotecommand", "0") # Clear the status of remotecommand
                os.system("reboot")
            else:
                print(f"Unknown command received: {payload}")

    def cleanup(self):
        self.monitoring = False
        if hasattr(self, 'water_level_thread') and self.water_level_thread.is_alive():
            self.water_level_thread.join()
        if hasattr(self, 'turbidity_thread') and self.turbidity_thread.is_alive():
            self.turbidity_thread.join()
        self.waste_water_level_sensor.cleanup()
        self.turbidity_sensor.cleanup()

if __name__ == "__main__":
    mqtt_client = mqttModule.MQTTModule(server="203.29.240.135", port=1883) # Connect to VM
    mqtt_client.connect()  # Initialize MQTT Client

    waste_water_level_sensor = WaterLevelModule(in_pin=17, mode_pin=27, sensor_location="waste")
    turbidity_sensor = TurbidityModule(id="TurbiditySensor_Bowl", sensor_pin=18)

    try:
        water_feeder = WaterFeeder(
            mqtt_client=mqtt_client,
            waste_water_level_sensor=waste_water_level_sensor,
            turbidity_sensor=turbidity_sensor
        )
        water_feeder.start_monitoring()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        water_feeder.cleanup()
        mqtt_client.disconnect()  # Disconnect MQTT Client
