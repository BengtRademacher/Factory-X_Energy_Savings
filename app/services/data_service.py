import random
import time
import threading
from datetime import datetime
from collections import deque
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
            "pm10_rise_rate": 0.05,
            "pm10_fall_rate": 0.15,
            "timestamp": ""
        }
        
        # Simulation parameters
        self._state_lock = threading.RLock()
        self.pm10_value = 0.0
        self.mist_active = False
        self.pm10_rise_rate = 0.05
        self.pm10_fall_rate = 0.15
        self._tasks_started = False
        
        self._initialized = True
        self.api_app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        @self.api_app.get("/data")
        def get_data():
            return self.get_server_data_snapshot()

    def run_api(self):
        uvicorn.run(self.api_app, host="127.0.0.1", port=8000, log_level="error")

    def data_generator(self):
        last_tick = time.monotonic()
        while True:
            now = time.monotonic()
            elapsed_seconds = max(0.0, min(now - last_tick, 2.0))
            last_tick = now

            with self._state_lock:
                rise_rate = self.pm10_rise_rate
                fall_rate = self.pm10_fall_rate

                # Two-point controller logic. The slider values are maximum
                # rates per second, so the random factor never exceeds 1.0.
                if not self.mist_active:
                    # Phase: Pollution (Extraction OFF)
                    self.pm10_value += rise_rate * elapsed_seconds * random.uniform(0.9, 1.0)
                    if self.pm10_value >= 3.0:
                        self.pm10_value = 3.0
                        self.mist_active = True
                else:
                    # Phase: Cleaning (Extraction ON)
                    self.pm10_value -= fall_rate * elapsed_seconds * random.uniform(0.9, 1.0)
                    if self.pm10_value <= 2.0:
                        self.pm10_value = 2.0
                        self.mist_active = False

                self.pm10_value = max(0.0, round(self.pm10_value, 4))

                snapshot = {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "Main supply": 4200 + random.randint(-50, 50),
                    "Mist extractor": (385 + random.randint(-5, 5)) if self.mist_active else 0,
                    "Chip conveyor": 260 + random.randint(-10, 10),
                    "PM10": self.pm10_value,
                    "mist_extractor_active": self.mist_active,
                    "pm10_rise_rate": rise_rate,
                    "pm10_fall_rate": fall_rate,
                }
                self.server_data.update(snapshot)
                self.history.append(snapshot.copy())
            
            time.sleep(1)

    def set_pm10_rates(self, rise_rate, fall_rate):
        with self._state_lock:
            self.pm10_rise_rate = float(rise_rate)
            self.pm10_fall_rate = float(fall_rate)
            self.server_data["pm10_rise_rate"] = self.pm10_rise_rate
            self.server_data["pm10_fall_rate"] = self.pm10_fall_rate

    def get_server_data_snapshot(self):
        with self._state_lock:
            return self.server_data.copy()

    def get_history_snapshot(self):
        with self._state_lock:
            return list(self.history)

    def reset_all_data(self):
        with self._state_lock:
            self.history.clear()
            self.pm10_value = 0.0
            self.mist_active = False
            self.server_data["PM10"] = 0.0
            self.server_data["mist_extractor_active"] = False

    def start_background_tasks(self):
        with self._lock:
            if self._tasks_started:
                return
            self._tasks_started = True
        threading.Thread(target=self.run_api, daemon=True).start()
        threading.Thread(target=self.data_generator, daemon=True).start()

# Global instance
data_service = DataService()
