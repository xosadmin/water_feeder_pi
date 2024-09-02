from modules import ValveModule, WaterLevelModule, TurbidityModule, RFIDModule, PumpModule, NotificationModule

class WaterFeeder:
  def __init__(self):
    # INITIALIZE MODULES
    # Valves
    self.reservoir_valve = ValveModule(pin=17) #(Jias)
    self.bowl_valve= ValveModule(pin=18) #(Hanxun)

    # Reservoir sensors (Jias)
    self.reservoir_level_sensor = WaterLevelModule(pin=19)
    self.reservoir_turbidity_sensor = TurbidityModule(pin=20)

    # Water bowl sensors (Hanxun)
    self.bowl_level_sensor = WaterLevelModule(pin=21)
    self.bowl_turbidity_sensor = TurbidityModule(pin=22)
    
    # RFID (Jean)
    self.rfid_reader = RFIDModule(pin=24)

    # Drainage system pump
    self.pump = PumpModule(pin=23) # (Zongqi)
    self.waste_level_sensor = WaterLevelModule(pin=23) #(Mike) 

    # Notification (All)
    self.notification = NotificationModule()

    # GET WATER FEEDER INITIAL DATA
    # Water levels
    self.reservoir_level_status = self.reservoir_level_sensor.get_water_level()
    self.bowl_level_sensor.get_water_level()
    self.waste_level_sensor.get_water_level()

    # Turbidity
    self.reservoir_turbidity_sensor.get_turbidity()
    self.bowl_turbidity_sensor.get_turbidity()

    # Water pump status
    self.pump.get_status()

  """
  TODO: Jiashuai
  1. Calculate amount of water to be replenished
  2. Open valve
  3. Close valve
  4. Update reservoir status
  5. Send notification
  """
  def refill_bowl(self):
    pass


  """
  TODO: Everyone
    1. Shape data in JSON format and send to Cloud API
  """
  def get_sensor_data(self):
    reservoir_level = self.reservoir_level_sensor.get_water_level()
    reservoir_turbidity = self.reservoir_turbidity_sensor.get_turbidity()

    bowl_level= self.bowl_level_sensor.get_water_level()
    bowl_turbidity = self.bowl_turbidity_sensor.get_turbidity()

    pump_status = self.pump.get_status()
    waste_level = self.waste_level_sensor.get_water_level()
    # Work here


  def cleanup(self):
    self.reservoir_valve.cleanup()
    self.bowl_valve.cleanup()

    self.reservoir_turbidity_sensor.cleanup()
    self.reservoir_level_sensor.cleanup()

    self.bowl_level_sensor.cleanup()
    self.bowl_turbidity_sensor.cleanup()

    self.pump.cleanup()
    self.waste_level_sensor.cleanup()

    self.rfid_reader.cleanup()

if __name__ == "__main__":
  try:
    water_feeder = WaterFeeder()
    # Write code here
    pass
  finally:
    water_feeder.cleanup()
