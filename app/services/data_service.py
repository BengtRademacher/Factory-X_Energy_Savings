import random
import time
import threading
from datetime import datetime
from collections import deque
import requests
from fastapi import FastAPI
import uvicorn

class DataService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DataService, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.history = deque(maxlen=300)  # 5 minutes
        self.server_data = {
            "Main supply": 0,
            "Mist extractor": 0,
            "Chip conveyor": 0,
            "PM10": 0.0,
            "mist_extractor_active": False,
            "timestamp": ""
        }
        
        # Simulation parameters
        self.pm10_value = 0.0
        self.mist_active = False
        self.pm10_rise_rate = 0.05
        self.pm10_fall_rate = 0.15
        
        self._initialized = True
        self.api_app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        @self.api_app.get("/data")
        def get_data():
            return self.server_data

    def run_api(self):
        uvicorn.run(self.api_app, host="127.0.0.1", port=8000, log_level="error")

    def data_generator(self):
        while True:
            # Two-point controller logic
            if not self.mist_active:
                # Phase: Pollution (Extraction OFF)
                self.pm10_value += self.pm10_rise_rate + random.uniform(-0.005, 0.005)
                if self.pm10_value >= 3.0:
                    self.mist_active = True
            else:
                # Phase: Cleaning (Extraction ON)
                self.pm10_value -= self.pm10_fall_rate + random.uniform(-0.01, 0.01)
                if self.pm10_value <= 2.0:
                    self.mist_active = False
            
            # Clamp value
            self.pm10_value = max(0.0, round(self.pm10_value, 4))

            # Base loads with minimal noise
            self.server_data["Main supply"] = 4200 + random.randint(-50, 50)
            # Mist extractor only consumes power when active
            self.server_data["Mist extractor"] = (385 + random.randint(-5, 5)) if self.mist_active else 0
            self.server_data["Chip conveyor"] = 260 + random.randint(-10, 10)
            
            self.server_data["PM10"] = self.pm10_value
            self.server_data["mist_extractor_active"] = self.mist_active
            self.server_data["timestamp"] = datetime.now().strftime("%H:%M:%S")
            
            time.sleep(1)

    def api_poller(self):
        while True:
            try:
                response = requests.get("http://127.0.0.1:8000/data", timeout=0.5)
                if response.status_code == 200:
                    api_json = response.json()
                    normalized = {
                        "timestamp": api_json.get("timestamp", datetime.now().strftime("%H:%M:%S")),
                        "Main supply": api_json.get("Main supply", 0),
                        "Mist extractor": api_json.get("Mist extractor", 0),
                        "Chip conveyor": api_json.get("Chip conveyor", 0),
                        "PM10": api_json.get("PM10", 0.0),
                        "mist_extractor_active": api_json.get("mist_extractor_active", False)
                    }
                    self.history.append(normalized)
            except Exception:
                pass
            time.sleep(1)

    def reset_all_data(self):
        self.history.clear()
        self.pm10_value = 0.0
        self.mist_active = False
        self.server_data["PM10"] = 0.0
        self.server_data["mist_extractor_active"] = False

    def start_background_tasks(self):
        threading.Thread(target=self.run_api, daemon=True).start()
        threading.Thread(target=self.data_generator, daemon=True).start()
        threading.Thread(target=self.api_poller, daemon=True).start()

# Global instance
data_service = DataService()
