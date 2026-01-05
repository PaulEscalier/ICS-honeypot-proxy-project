import asyncio
from state import state

async def thermal_simulation():
    while True:
        state["temperature"] += state["heater_power"] * 0.05

        state["temperature"] -= state["load_mass"] * 0.001

        if state["cooling"]:
            state["temperature"] -= 15

        state["alarm"] = state["temperature"] > 850

        await asyncio.sleep(2)
