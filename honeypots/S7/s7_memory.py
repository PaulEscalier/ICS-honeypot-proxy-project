import threading

class PLCMemory:
    def __init__(self):
        self.lock = threading.Lock()
        self.db1 = {
            "pump": False,
            "valve": False,
            "temperature": 42.5,
            "pressure": 1.7,
        }

    def read(self):
        with self.lock:
            return self.db1.copy()

    def write(self, key, value):
        with self.lock:
            self.db1[key] = value

plc_memory = PLCMemory()
