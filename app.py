import os
from time import sleep, time
import threading
from modules import WaterLevelModule, TurbidityModule, mqttModule, ValveModule, RFIDModule, readWeight, PumpModule
from modules import wificonn, httpModule

class WaterFeeder:
    def __init__(self, waste_water_level_sensor_arg, turbidity_sensor, reservoir_valve, rfid_module, mqtt_client, wifi_conn, httpmodule, readWeight, pump_arg, bowl_valve_arg, reservoir_water_level_sensor_arg):
        self.waste_water_level_sensor = waste_water_level_sensor_arg
        self.turbidity_sensor = turbidity_sensor
        self.reservoir_valve = reservoir_valve
        self.rfid_module = rfid_module
        self.mqtt_client = mqtt_client
        self.wifi_conn = wifi_conn
        self.httpmodule = httpmodule
        self.readWeight = readWeight
        self.monitoring = True
        self.pump = pump_arg
        self.bowl_valve = bowl_valve_arg
        self.reservoir_water_level_sensor = reservoir_water_level_sensor_arg

        # Stop event for controlling the pump flow
        self.stop_event = threading.Event()

        # Subscribe to remote command via MQTT
        self.mqtt_client.client.subscribe("remotecommand")
        self.mqtt_client.client.on_message = self.on_message

        # Uncomment this to test bowl drain 
        # self.start_drain_bowl_thread() 

    def get_sensor_data(self):
        waste_water_level = self.waste_water_level_sensor.is_low()
        reservoir_water_level = self.reservoir_water_level_sensor.is_low()
        turbidity_value = self.turbidity_sensor.read_turbidity()
        weight_value = self.readWeight.average_weight()

        if weight_value is not None:
            # Console logs
            print(f"Reservoir water level: {self.reservoir_water_level_sensor.get_water_level()}")
            print(f"Turbidity Level: {turbidity_value}")
            print(f"Waste water level: {waste_water_level}")
            print(f"Water bowl weight: {weight_value}")
        else:
            print("Weight sensor returned invalid data.")

    def monitor_waste_water_level(self):
        while self.monitoring and not self.stop_event.is_set():
            try:
                print("Checking waste water sensor...")
                waste_water_level = self.waste_water_level_sensor.is_low()
                print(f"Monitoring - Waste water level: {self.waste_water_level_sensor.get_water_level()}")
                waste_tank_sensor_location = self.waste_water_level_sensor.sensor_location
                print(f"Uploading waste water level: {waste_water_level}")
                self.httpmodule.uploadSensorData(f"{waste_tank_sensor_location}", str(waste_water_level))
                sleep(5)
            except Exception as e:
                print(f"Error in monitor_waste_water_level: {e}")

    def monitor_reservoir_water_level(self):
        while self.monitoring and not self.stop_event.is_set():
            try:
                print("Checking reservoir water sensor...")
                reservoir_water_level = self.reservoir_water_level_sensor.is_low()
                print(f"Monitoring - Reservoir water level: {self.reservoir_water_level_sensor.get_water_level()}")
                reservoir_sensor_location = self.reservoir_water_level_sensor.sensor_location
                print(f"Uploading reservoir water level: {reservoir_water_level}")
                self.httpmodule.uploadSensorData(f"{reservoir_sensor_location}", str(reservoir_water_level))
                sleep(5)
            except Exception as e:
                print(f"Error in monitor_reservoir_water_level: {e}")

    def monitor_turbidity_level(self):
        while self.monitoring and not self.stop_event.is_set():
            try:
                turbidity_value = self.turbidity_sensor.read_turbidity()
                print(f"Monitoring - Turbidity Level: {turbidity_value}")
                ntu_id = self.turbidity_sensor.id
                weight_value = self.readWeight.average_weight()

                if weight_value is not None:
                    print(f"Uploading water bowl weight: {weight_value}")
                    self.httpmodule.uploadSensorData("weightBowl", weight_value)
                    self.httpmodule.uploadSensorData(ntu_id, turbidity_value)
                else:
                    print("Weight sensor returned invalid data.")

                sleep(5)
            except Exception as e:
                print(f"Error in monitor_turbidity_level: {e}")

    def monitor_bowl_weight(self):
        while self.monitoring and not self.stop_event.is_set():
            try:
                weight_value = self.readWeight.average_weight()
                if weight_value is not None:
                    print(f"Current bowl weight: {weight_value} grams")
                else:
                    print("Weight sensor returned invalid data.")
                sleep(5)
            except Exception as e:
                print(f"Error in monitor_bowl_weight: {e}")

    def start_monitoring(self):
        print("Starting monitoring threads...")

        self.wifi_conn.start_real_time_update()

        print("Starting turbidity monitoring...")
        self.turbidity_thread = threading.Thread(target=self.monitor_turbidity_level)
        self.turbidity_thread.daemon = True
        self.turbidity_thread.start()

        print("Starting RFID monitoring...")
        self.rfid_thread = threading.Thread(target=self.rfid_module.read_rfid)
        self.rfid_thread.daemon = True
        self.rfid_thread.start()

        print("Starting weight monitoring...")
        self.weight_thread = threading.Thread(target=self.monitor_bowl_weight)
        self.weight_thread.daemon = True
        self.weight_thread.start()

        print("Starting waste water monitoring...")
        self.waste_water_thread = threading.Thread(target=self.monitor_waste_water_level)
        self.waste_water_thread.daemon = True
        self.waste_water_thread.start()

        print("Starting reservoir water monitoring...")
        self.reservoir_thread = threading.Thread(target=self.monitor_reservoir_water_level)
        self.reservoir_thread.daemon = True
        self.reservoir_thread.start()

        if float(self.turbidity_sensor.read_turbidity()) >= 6.5:
            print("Turbidity too high, starting bowl drain...")
            self.start_drain_bowl_thread()

    def start_drain_bowl_thread(self):
        self.drain_bowl_thread = threading.Thread(target=self.drain_bowl)
        self.drain_bowl_thread.daemon = True
        self.drain_bowl_thread.start()

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode('utf-8')

        if topic == "remotecommand":
            if payload == "0":
                print("No command specified.")
            elif payload == "changewater":
                self.start_drain_bowl_thread()
                sleep(2)
                self.mqtt_client.send_message("remotecommand", "0")
            elif payload == "refillwater":
                sleep(2)
                self.mqtt_client.send_message("remotecommand", "0")
            elif payload == "restartfeeder":
                self.mqtt_client.send_message("remotecommand", "0")
                os.system("reboot")
            else:
                print(f"Unknown command received: {payload}")

    def drain_bowl(self):
        print("Draining water...")
        start_time = time()

        self.pump.start()
        self.bowl_valve.open()

        while time() - start_time < 40:
            if self.stop_event.is_set():
                print("Stopping pump and closing valve due to interruption...")
                self.pump.stop()
                self.bowl_valve.close()
                return

            if not self.waste_water_level_sensor.is_low():
                print("Waste tank is full! Please empty the tank.")
                print("Stopping pump and closing valve...")
                self.pump.stop()
                self.bowl_valve.close()
                return

            sleep(1)

        print("Stopping pump and closing valve...")
        self.pump.stop()
        self.bowl_valve.close()

    def cleanup(self):
        self.monitoring = False
        self.stop_event.set()

        if hasattr(self, 'turbidity_thread') and self.turbidity_thread.is_alive():
            self.turbidity_thread.join()
        if hasattr(self, 'weight_thread') and self.weight_thread.is_alive():
            self.weight_thread.join()
        if hasattr(self, 'rfid_thread') and self.rfid_thread.is_alive():
            self.rfid_thread.join()
        if hasattr(self, 'waste_water_thread') and self.waste_water_thread.is_alive():
            self.waste_water_thread.join()
        if hasattr(self, 'reservoir_thread') and self.reservoir_thread.is_alive():
            self.reservoir_thread.join()
        if hasattr(self, 'drain_bowl_thread') and self.drain_bowl_thread.is_alive():
            self.drain_bowl_thread.join()

        self.waste_water_level_sensor.cleanup()
        self.rfid_module.cleanup()
        self.pump.cleanup()
        self.wifi_conn.stop_real_time_update()

if __name__ == "__main__":
    backendAddr = "203.29.240.135"

    mqtt_client = mqttModule.MQTTModule(server=backendAddr, port=1883)
    mqtt_client.connect()
    turbidity_sensor = TurbidityModule(id="turbiditysensor", sensor_channel=0)
    reservoir_valve = ValveModule(pin=20)
    httpmodule = httpModule.HTTPModule(server=backendAddr)
    wifi_conn = wificonn.WiFiConn(update_interval=5, api_url=f'http://{backendAddr}:5000/update_wificonn')
    waste_water_level_sensor = WaterLevelModule(in_pin=22, mode_pin=27, sensor_location="waterlevelwaste")
    weight_bowl = readWeight(iic_mode=0x03, iic_address=0x64, calibration_value=223.7383270263672)
    print("Getting 10 weight readings, please wait...")
    weight_bowl.begin()
    rfid_module = RFIDModule(server=backendAddr, water_weight=weight_bowl)
    pump = PumpModule(pin=16)
    bowl_valve = ValveModule(pin=21)
    reservoir_water_level_sensor = WaterLevelModule(in_pin=6, mode_pin=5, sensor_location="waterlevelreservoir")
    
    try:
        water_feeder = WaterFeeder(
            pump_arg=pump,
            mqtt_client=mqtt_client,
            waste_water_level_sensor_arg=waste_water_level_sensor,
            turbidity_sensor=turbidity_sensor,
            reservoir_valve=reservoir_valve,
            rfid_module=rfid_module,
            wifi_conn=wifi_conn,
            httpmodule=httpmodule,
            readWeight=weight_bowl,
            bowl_valve_arg=bowl_valve,
            reservoir_water_level_sensor_arg=reservoir_water_level_sensor
        )
        water_feeder.start_monitoring()
        while True:
            sleep(1)

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        water_feeder.cleanup()
        mqtt_client.disconnect()
