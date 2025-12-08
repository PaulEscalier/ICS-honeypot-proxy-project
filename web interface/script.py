from flask import Flask, jsonify, send_from_directory
import random
import asyncio
from pymodbus.client import AsyncModbusTcpClient
from opcua import Client, ua
import snap7
from snap7.util import *
from snap7.type import Areas


MODBUS_HOST = "modbus"
MODBUS_PORT = 5020


OPC_UA_SERVER_URL = "opc.tcp://opcua:4840"
NODE_ID = "ns=2;i=1"  # ID de la variable à lire/écrire sur le serveur

app = Flask(__name__)

client = Client(OPC_UA_SERVER_URL)
connected = False


PLC_IP = "s7"
PLC_RACK = 0
PLC_SLOT = 1

def random_s7_activity():
    client = snap7.client.Client()
    client.connect(PLC_IP, PLC_RACK, PLC_SLOT)

    actions = []

    # Choix aléatoire : read / write
    for i in range(5):
        action_type = random.choice(["READ", "WRITE"])
        db_number = 1
        start = random.randint(0, 10)
        size = random.randint(1, 4)

        if action_type == "READ":
            data = client.read_area(Areas.DB, db_number, start, size)
            actions.append({
                "action": "READ",
                "db": db_number,
                "start": start,
                "size": size,
                "returned_bytes": list(data)
            })

        else:
            random_bytes = bytes([random.randint(0, 255) for _ in range(size)])
            client.write_area(Areas.DB, db_number, start, random_bytes)
            actions.append({
                "action": "WRITE",
                "db": db_number,
                "start": start,
                "size": size,
                "written_bytes": list(random_bytes)
            })

    client.disconnect()
    return actions

@app.get("/s7Activity")
def s7_activity():
    activity = random_s7_activity()
    return jsonify({
        "status": "OK",
        "performed_operations": activity
    })


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

@app.route("/opcUaActivity", methods=["GET"])
def opcua_activity():
    global connected
    if not connected:
        client.connect()
        connected = True
        print("Connected to OPC-UA server")
    root = client.get_root_node()
    objects = root.get_child(["0:Objects"])  # Node i=85
    children = objects.get_children()
    for child in children:
        print(child, child.get_browse_name())
    if(len(children)==0):
        print("no children")


    node = client.get_node(NODE_ID)
    print("Browse name of node:", node.get_browse_name())
    print("Access level:", node.get_access_level())
    print("Variant type:", node.get_data_type_as_variant_type())

    action = random.choice(["read", "write"])
    
    if action == "read":
        value = node.get_value()
        return jsonify({"action": "read", "node": NODE_ID, "value": value})
    else:
        new_value = random.randint(0, 100)
        node.set_value(ua.Variant(new_value, ua.VariantType.Int32))
        return jsonify({"action": "write", "node": NODE_ID, "new_value": new_value})

@app.teardown_appcontext
def shutdown(exception):
    global connected
    if connected:
        client.disconnect()
        connected = False
        print("Disconnected from OPC-UA server")

@app.route('/')
def serve_index():
    return send_from_directory('html', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('html', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
