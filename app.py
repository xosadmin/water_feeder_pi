# TODO: Import your module here
# from modules import WaterLevelModule
from modules import PumpModule
from time import sleep

class WaterFeeder:
    def __init__(self, pumpArg):
        # Set your module as member here
        # self.waste_water_level_sensor = waste_water_level_sensor
        self.pump = pumpArg
        # GET WATER FEEDER INITIAL DATA
        self.get_sensor_data()

    def get_sensor_data(self):
        # waste_water_level = self.waste_water_level_sensor.get_water_level()
        # print(waste_water_level)
        # print(pump.get_status())
        pass

    def monitor_waste_water_level(self):
        self.waste_water_level_sensor.monitor_water_level()

    def cleanup(self):
        # self.waste_water_level_sensor.cleanup()
        self.pump.cleanup()

if __name__ == "__main__":
    # waste_water_level_sensor = WaterLevelModule(in_pin=17, mode_pin=27, sensor_location="waste")
    pump = PumpModule(pin=14)

    try:
        # Instantiate your module here by passing them as args
        water_feeder = WaterFeeder(
            # waste_water_level_sensor = waste_water_level_sensor,
            pumpArg = pump
        )
        # Start monitoring here
        # water_feeder.monitor_waste_water_level()
        pump.start()
        # pump.monitor_status()
        sleep(3)
        pump.stop()

    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        water_feeder.cleanup()