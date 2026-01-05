import asyncio
from state import process_state

async def conveyor_loop():
    while True:
        if process_state["belt_running"] and not process_state["emergency_stop"]:
            process_state["load_weight"] += process_state["motor_speed"] * 0.05
            process_state["temperature"] += process_state["motor_speed"] * 0.01
        else:
            process_state["load_weight"] = max(0, process_state["load_weight"] - 5)
            process_state["temperature"] -= 0.5

        if process_state["load_weight"] > 300:
            process_state["jam_detected"] = True

        if process_state["temperature"] > 80:
            process_state["emergency_stop"] = True

        process_state["temperature"] = max(20, process_state["temperature"])

        await asyncio.sleep(1)
