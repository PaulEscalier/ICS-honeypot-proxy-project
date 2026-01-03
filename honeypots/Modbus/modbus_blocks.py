from pymodbus.datastore import ModbusSequentialDataBlock
from logger import logger

class LoggingCoilBlock(ModbusSequentialDataBlock):
    def setValues(self, address, values):
        for i, value in enumerate(values):
            logger.info(
                f"MODBUS WRITE COIL | address={address + i} value={value}"
            )
        super().setValues(address, values)


class LoggingHoldingRegisterBlock(ModbusSequentialDataBlock):
    def setValues(self, address, values):
        for i, value in enumerate(values):
            logger.info(
                f"MODBUS WRITE REGISTER | address={address + i} value={value}"
            )
        super().setValues(address, values)
