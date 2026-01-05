import struct
from state import process_state
from db_layout import DB1_LAYOUT, DB1_SIZE
from logger import logger

class S7Honeypot:
    def __init__(self):
        self.db = bytearray(DB1_SIZE)
        self.sync_state_to_db()

    def sync_state_to_db(self):
        for offset, (name, dtype) in DB1_LAYOUT.items():
            value = process_state[name]

            if dtype == "REAL":
                self.db[offset:offset+4] = struct.pack(">f", float(value))
            elif dtype == "BOOL":
                self.db[offset] = 1 if value else 0

    def sync_db_to_state(self):
        for offset, (name, dtype) in DB1_LAYOUT.items():
            if dtype == "REAL":
                process_state[name] = struct.unpack(">f", self.db[offset:offset+4])[0]
            elif dtype == "BOOL":
                process_state[name] = bool(self.db[offset])


    def read_db(self, start, size, client_ip="unknown"):
        logger.info(
            f"READ_DB | ip={client_ip} | start={start} | size={size}"
        )
        self.sync_state_to_db()
        return self.db[start:start+size]

    def write_db(self, start, data, client_ip="unknown"):
        logger.warning(
            f"WRITE_DB | ip={client_ip} | start={start} | bytes={len(data)}"
        )
        self.db[start:start+len(data)] = data
        self.sync_db_to_state()
        self.detect_attack(start, data, client_ip)
    
    def detect_attack(self, start, data, ip):
        if start == 0 and len(data) >= 4:
            speed = struct.unpack(">f", data[:4])[0]
            if speed > 90:
                logger.critical(
                    f"ATTACK | High motor speed | ip={ip} | value={speed}"
                )
            if start == 9:
                if data[0] == 0:
                    logger.critical(
                        f"ATTACK | Jam detection disabled | ip={ip}"
                    )
            if start == 10 and data[0] == 0:
                logger.critical(
                    f"ATTACK | Emergency stop released | ip={ip}"
                )




