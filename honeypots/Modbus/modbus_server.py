from pymodbus.server.server import ModbusTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusDeviceContext
)
from logger import logger
from pymodbus.pdu.device import ModbusDeviceIdentification
from modbus_blocks import (
    LoggingCoilBlock,
    LoggingHoldingRegisterBlock,
)

def on_connect(connect: bool, peername=None):
    # trace_connect is called with connect=True when client connects
    if connect and peername:
        ip, port = peername
        logger.info(f"MODBUS CONNECT | ip={ip} port={port}")
    elif not connect and peername:
        ip, port = peername
        logger.info(f"MODBUS DISCONNECT | ip={ip} port={port}")

def create_context():
    device = ModbusDeviceContext(
        co=LoggingCoilBlock(0, [0]*100),
        hr=LoggingHoldingRegisterBlock(0, [0]*100),
    )
    return ModbusServerContext(devices={1: device}, single=False)

def create_identity():
    identity = ModbusDeviceIdentification()
    identity.VendorName = "Siemens"
    identity.ProductName = "SIMATIC S7-300"
    identity.ModelName = "CPU 315-2 PN/DP"
    identity.MajorMinorRevision = "3.3"
    return identity

async def start_modbus(context, identity):
    server = ModbusTcpServer(
        context=context,
        identity=identity,
        address=("0.0.0.0", 502),
        trace_connect=lambda status: on_connect(status, getattr(status, 'peername', None)),
    )
    await server.serve_forever()
