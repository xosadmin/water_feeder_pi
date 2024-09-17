import os
import time
import threading
from modules import WaterLevelModule, TurbidityModule, mqttModule, ValveModule
from modules import wificonn

class WaterFeeder:
    def __init__(self, waste_water_level_sensor, turbidity_sensor, reservoir_valve, mqtt_client, wifi_conn):
        self.waste_water_level_sensor = waste_water_level_sensor
        self.turbidity_sensor = turbidity_sensor
        self.reservoir_valve = reservoir_valve
        self.mqtt_client = mqtt_client
        self.wifi_conn = wifi_conn
        self.monitoring = True
        self.get_sensor_data()

        self.mqtt_client.client.subscribe("remotecommand")
        self.mqtt_client.client.on_message = self.on_message

    def get_sensor_data(self):
        waste_water_level = self.waste_water_level_sensor.get_water_level()
        turbidity_value = self.turbidity_sensor.read_turbidity()
        sensor_location = self.waste_water_level_sensor.sensor_location
        ntu_id = self.turbidity_sensor.id

        print(waste_water_level)
        print(f"Turbidity Level: {turbidity_value}")
        self.mqtt_client.send_message(f"sensor/waterlevel/{sensor_location}", str(waste_water_level))
        self.mqtt_client.send_message(f"sensor/{ntu_id}", str(turbidity_value))

    def monitor_waste_water_level(self):
        self.waste_water_level_sensor.monitor_water_level()

    def monitor_turbidity_level(self):
        while self.monitoring:
            turbidity_value = self.turbidity_sensor.read_turbidity()
            print(f"Monitoring - Turbidity Level: {turbidity_value}")
            ntu_id = self.turbidity_sensor.id
            self.mqtt_client.send_message(f"sensor/{ntu_id}", str(turbidity_value))
            time.sleep(1)

    def start_monitoring(self):
        self.wifi_conn.start_real_time_update()

        self.turbidity_thread = threading.Thread(target=self.monitor_turbidity_level)
        self.turbidity_thread.daemon = True
        self.turbidity_thread.start()

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode('utf-8')

        if topic == "remotecommand":
            if payload == "0":
                print("No command specified.")
            elif payload == "changewater":
                self.mqtt_client.send_message("remotecommand", "0")
            elif payload == "refillwater":
                self.mqtt_client.send_message("remotecommand", "0")
            elif payload == "restartfeeder":
                self.mqtt_client.send_message("remotecommand", "0")
                os.system("reboot")
            else:
                print(f"Unknown command received: {payload}")

    def cleanup(self):
        self.monitoring = False
        if hasattr(self, 'turbidity_thread') and self.turbidity_thread.is_alive():
            self.turbidity_thread.join()
        self.waste_water_level_sensor.cleanup()
        self.turbidity_sensor.cleanup()
        self.wifi_conn.stop_real_time_update()

if __name__ == "__main__":
    backendAddr = "203.29.240.135"

    mqtt_client = mqttModule.MQTTModule(server=backendAddr, port=1883)
    mqtt_client.connect()

    waste_water_level_sensor = WaterLevelModule(in_pin=17, mode_pin=27, sensor_location="waste")
    turbidity_sensor = TurbidityModule(id="TurbiditySensor_Bowl", sensor_channel=0) # Install sensor on A0 on ADS115
    reservoir_valve = ValveModule(pin=20)
    wifi_conn = wificonn.WiFiConn(update_interval=5, api_url=f'http://{backendAddr}:5000/update_wificonn')
    
    try:
        water_feeder = WaterFeeder(
            mqtt_client=mqtt_client,
            waste_water_level_sensor=waste_water_level_sensor,
            turbidity_sensor=turbidity_sensor,
            reservoir_valve=reservoir_valve,
            wifi_conn=wifi_conn
        )
        water_feeder.start_monitoring()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        water_feeder.cleanup()
        mqtt_client.disconnect()
