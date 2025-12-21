import asyncio
from state import process_state

SLAVE_ID = 1

async def process_loop(context):
    device = context[SLAVE_ID]

    while True:
        pump = device.getValues(1, 0, count=1)[0]
        valve = device.getValues(1, 1, count=1)[0]

        process_state["pump"] = bool(pump)
        process_state["valve"] = bool(valve)

        if process_state["pump"]:
            process_state["pressure"] += 0.1
        else:
            process_state["pressure"] -= 0.05

        if process_state["valve"]:
            process_state["temperature"] -= 0.2
        else:
            process_state["temperature"] += 0.1

        process_state["temperature"] = max(10, min(100, process_state["temperature"]))
        process_state["pressure"] = max(0, min(10, process_state["pressure"]))

        device.setValues(3, 0, [int(process_state["temperature"])])
        device.setValues(3, 1, [int(process_state["pressure"] * 10)])

        await asyncio.sleep(1)
