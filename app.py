# TODO: Import your module here
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

    def get_sensor_data(self):
        waste_water_level = self.waste_water_level_sensor.get_water_level()
        ntu_value = self.turbidity_sensor.get_turbidity()
        sensor_location = self.waste_water_level_sensor.sensor_location
        ntu_id = self.turbidity_sensor.id

        print(waste_water_level)
        print(f"Turbidity Level: {ntu_value}")
        self.mqtt_client.send_message(f"sensor/waterlevel/{sensor_location}", str(waste_water_level))
        self.mqtt_client.send_message(f"sensor/{ntu_id}", str(ntu_value))

    # def monitor_waste_water_level(self):
    #     while self.monitoring:
    #         waste_water_level = self.waste_water_level_sensor.get_water_level()
    #         sensor_location = self.waste_water_level_sensor.sensor_location
    #         print(f"Monitoring - Water Level: {waste_water_level}")
    #         self.mqtt_client.send_message(f"sensor/waterlevel/{sensor_location}", str(waste_water_level)) # The sensor code need to adjust before uncomment these codes
    #         time.sleep(5)
    def monitor_waste_water_level(self):
        self.waste_water_level_sensor.monitor_water_level()

    def monitor_turbidity_level(self):
        while self.monitoring:
            ntu_value = self.turbidity_sensor.get_turbidity()
            ntu_id = self.turbidity_sensor.id
            print(f"Monitoring - Turbidity Level: {ntu_value}")
            self.mqtt_client.send_message(f"sensor/{ntu_id}", str(ntu_value))
            time.sleep(1)

    def start_monitoring(self):
        # self.water_level_thread = threading.Thread(target=self.monitor_waste_water_level)
        # self.water_level_thread.daemon = True
        # self.water_level_thread.start()

        self.turbidity_thread = threading.Thread(target=self.monitor_turbidity_level)
        self.turbidity_thread.daemon = True
        self.turbidity_thread.start()

    def cleanup(self):
        self.monitoring = False
        if hasattr(self, 'water_level_thread') and self.water_level_thread.is_alive():
            self.water_level_thread.join()
        if hasattr(self, 'turbidity_thread') and self.turbidity_thread.is_alive():
            self.turbidity_thread.join()
        self.waste_water_level_sensor.cleanup()
        self.turbidity_sensor.cleanup()

if __name__ == "__main__":
    mqtt_client = mqttModule.MQTTModule(server="10.243.29.193", port=1883) # Connect to VM
    mqtt_client.connect()  # Initialize MQTT Client

    waste_water_level_sensor = WaterLevelModule(in_pin=17, mode_pin=27, sensor_location="waste")
    turbidity_sensor = TurbidityModule(id="TurbiditySensor_Bowl", sensor_pin=2, output_pin=13)

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
