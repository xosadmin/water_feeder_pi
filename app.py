# TODO: Import your module here
from modules import WaterLevelModule

class WaterFeeder:
    def __init__(self, waste_water_level_sensor):
        # Set your module as member here
        self.waste_water_level_sensor = waste_water_level_sensor
        # GET WATER FEEDER INITIAL DATA
        self.get_sensor_data()

    def get_sensor_data(self):
        waste_water_level = self.waste_water_level_sensor.get_water_level()
        print(waste_water_level)

    def monitor_waste_water_level(self):
        self.waste_water_level_sensor.monitor_water_level()

    def cleanup(self):
        self.waste_water_level_sensor.cleanup()

if __name__ == "__main__":
    waste_water_level_sensor = WaterLevelModule(in_pin=17, mode_pin=27)

    try:
        # Instantiate your module here by passing them as args
        water_feeder = WaterFeeder(
            waste_water_level_sensor = waste_water_level_sensor
        )
        # Start monitoring here
        water_feeder.monitor_waste_water_level()

    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        water_feeder.cleanup()