import asyncio
import random
from energy_state import energy_state
from logger import logger

async def energy_simulation():
    while True:
        if energy_state["breaker_1"]:
            energy_state["current_a"] = 300 + random.uniform(-20, 20)
            energy_state["voltage_kv"] = 225 + random.uniform(-2, 2)
        else:
            energy_state["current_a"] = 0.0
            energy_state["voltage_kv"] = 210 + random.uniform(-1, 1)

        energy_state["frequency_hz"] = 50.0 + random.uniform(-0.05, 0.05)

        logger.info(
            f"STATE | B1={energy_state['breaker_1']} "
            f"U={energy_state['voltage_kv']:.1f}kV "
            f"I={energy_state['current_a']:.1f}A "
            f"F={energy_state['frequency_hz']:.2f}Hz"
        )

        await asyncio.sleep(2)
