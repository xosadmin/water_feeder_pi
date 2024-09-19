import requests

class HTTPModule:
    def __init__(self, server):
        self.server = server
    
    def uploadSensorData(self, topic, value):
        try:
            dataCompose = {
                "sensor": topic,
                "value": value
            }
            response = requests.post(f"http://{self.server}:5000/update_sensordata", json=dataCompose)
            if response.status_code == 200:
                print("Data sent successfully to the API")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending data to the API: {e}")

    def uploadDrinkData(self, petid, drinkamount):
        try:
            dataCompose = {
                "petID": petid,
                "drinkAmount": drinkamount
            }
            response = requests.post(f"http://{self.server}:5000/addpetdrink", json=dataCompose)
            if response.status_code == 200:
                print("Data sent successfully to the API")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending data to the API: {e}")
