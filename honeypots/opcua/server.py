from opcua import Server
from state import state
from logger import logger
import socket
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/")
server.set_server_name("Industrial Furnace OPC UA Server")

idx = server.register_namespace("http://furnace.demo")

objects = server.get_objects_node()
furnace = objects.add_object(idx, "FurnaceSystem")

heater = furnace.add_variable(idx, "HeaterPower", state["heater_power"])
temp   = furnace.add_variable(idx, "ChamberTemperature", state["temperature"])
mass   = furnace.add_variable(idx, "LoadMass", state["load_mass"])
cool   = furnace.add_variable(idx, "CoolingEnabled", state["cooling"])
alarm  = furnace.add_variable(idx, "HighTempAlarm", state["alarm"])

heater.set_writable()
mass.set_writable()
cool.set_writable()

_original_accept = socket.socket.accept


def logging_accept(self):
    conn, addr = _original_accept(self)
    logger.info(f"OPC UA client connected from {addr[0]}:{addr[1]}")
    return conn, addr
socket.socket.accept = logging_accept

def run():
    server.start()
    logger.info("OPC UA server running on port 4840")

    try:
        while True:
            heater.set_value(state["heater_power"])
            temp.set_value(state["temperature"])
            mass.set_value(state["load_mass"])
            cool.set_value(state["cooling"])
            alarm.set_value(state["alarm"])
    finally:
        server.stop()
