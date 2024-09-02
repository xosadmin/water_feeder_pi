"""
File: NotificationsModule
Author: To be done by all
Description: Sends notification to the client application with the following events:

1. Reservoir low water level - Notifies when reservoir needs refill.
2. Bowl water quality - Notifies user when high level of contamination is detected.
3. Bowl low water level - Notifies when water level needs refilling. 
4. Pump on/off - Notifies user pumps power state
5. Full Waste tank - Notifies user if water waste tank cannot accept anymore water. 
"""

class NotificationModule:
    def __init__(self):
      # Work here
      pass

    def send(self, message):
       print(f"Message: {message}")
