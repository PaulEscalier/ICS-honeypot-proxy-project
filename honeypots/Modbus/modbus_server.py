from pymodbus.server.server import ModbusTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusDeviceContext
)
from pymodbus.pdu.device import ModbusDeviceIdentification

def create_context():
    device = ModbusDeviceContext(
        co=ModbusSequentialDataBlock(0, [0]*10),
        hr=ModbusSequentialDataBlock(0, [25, 10] + [0]*8)
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
        address=("0.0.0.0", 502)
    )
    await server.serve_forever()
