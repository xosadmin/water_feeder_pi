import subprocess
import threading
import time
from datetime import datetime
import re
import requests

class WiFiConn:
    def __init__(self, update_interval=5, api_url="http://203.29.240.135:5000/update_wificonn"):
        self.wificonn = {
            'ipaddr': None,
            'rssi': 100,
            'lastseen': None
        }
        self.update_interval = update_interval
        self.api_url = api_url
        self.stop_event = threading.Event()

    def get_ip_address(self):
        try:
            result = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE, text=True)
            ip_address = result.stdout.strip().split()[0]
            return ip_address
        except Exception as e:
            print(f"Error retrieving IP address: {e}")
            return None

    def get_rssi(self):
        try:
            result = subprocess.run(['iwconfig'], stdout=subprocess.PIPE, text=True)
            output = result.stdout
            rssi_match = re.search(r'Signal level=(-\d+)', output)
            if rssi_match:
                rssi = int(rssi_match.group(1)) * -1
                return rssi
            else:
                print("RSSI not found")
                return None
        except Exception as e:
            print(f"Error retrieving RSSI: {e}")
            return None

    def update(self):
        ipaddr = self.get_ip_address()
        rssi = self.get_rssi()
        if ipaddr:
            self.wificonn['ipaddr'] = ipaddr
        if rssi is not None:
            self.wificonn['rssi'] = rssi
        self.wificonn['lastseen'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"WiFi connection updated: {self.wificonn}")
        self.send_to_api()

    def send_to_api(self):
        try:
            response = requests.post(self.api_url, json=self.wificonn)
            if response.status_code == 200:
                print("Data sent successfully to the API")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending data to the API: {e}")

    def start_real_time_update(self):
        self.stop_event.clear()
        thread = threading.Thread(target=self._run_update_loop)
        thread.start()

    def stop_real_time_update(self):
        self.stop_event.set()

    def _run_update_loop(self):
        while not self.stop_event.is_set():
            self.update()
            time.sleep(self.update_interval)

