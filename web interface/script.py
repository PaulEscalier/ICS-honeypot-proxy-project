from flask import Flask, jsonify, send_from_directory
import random
import asyncio
from pymodbus.client import AsyncModbusTcpClient

MODBUS_HOST = "modbus"
MODBUS_PORT = 5020

app = Flask(__name__)

async def modbus_activity():
    client = AsyncModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    await client.connect()

    if not client.connected:
        return {
            "action": "error",
            "address": -1,
            "value": None,
            "result": "unable to connect to Modbus server"
        }

    action = random.choice(["read_holding", "write_single"])
    address = random.randint(0, 10)

    if action == "read_holding":
        rr = await client.read_holding_registers(address, count=1, device_id=1)
        if rr.isError():
            value = None
            result = f"error: {rr}"
        else:
            value = rr.registers[0]
            result = str(value)

    else:  # write
        value = random.randint(0, 100)
        rr = await client.write_register(address, value, device_id=1)
        result = "ok" if not rr.isError() else f"error: {rr}"

    client.close()

    return {
        "action": action,
        "address": address,
        "value": value,
        "result": result
    }


@app.route("/modbusActivity")
def route_activity():
    result = asyncio.run(modbus_activity())
    return jsonify(result)


# Route pour servir index.html
@app.route('/')
def serve_index():
    return send_from_directory('html', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('html', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
