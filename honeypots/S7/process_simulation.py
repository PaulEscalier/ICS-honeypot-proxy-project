import time
import random
from s7_memory import plc_memory

def process_loop():
    while True:
        state = plc_memory.read()

        # Simulation simple et crédible
        if state["pump"]:
            plc_memory.write("pressure", min(state["pressure"] + 0.05, 10.0))
            plc_memory.write("temperature", min(state["temperature"] + 0.1, 120.0))
        else:
            plc_memory.write("pressure", max(state["pressure"] - 0.03, 1.0))
            plc_memory.write("temperature", max(state["temperature"] - 0.05, 25.0))

        # Valve ouverte -> chute de pression
        if state["valve"]:
            plc_memory.write("pressure", max(state["pressure"] - 0.1, 0.5))

        time.sleep(1)
