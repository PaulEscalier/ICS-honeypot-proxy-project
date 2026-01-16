from logger import logger
from energy_state import energy_state

C_SC_NA_1 = 0x2D

def handle_asdu(data: bytes, client_ip: str):
    asdu_type = data[6]

    if asdu_type != C_SC_NA_1:
        return None

    ioa = int.from_bytes(data[12:15], "little")
    sco = data[15]

    command_on = bool(sco & 0x01)

    if ioa == 100:
        energy_state["breaker_1"] = command_on
        logger.warning(
            f"ATTACK | {client_ip} | Breaker_1 set to {'ON' if command_on else 'OFF'}"
        )

    elif ioa == 101:
        energy_state["breaker_2"] = command_on
        logger.warning(
            f"ATTACK | {client_ip} | Breaker_2 set to {'ON' if command_on else 'OFF'}"
        )

    return activation_confirmation(data)

def activation_confirmation(rx: bytes):
    tx = bytearray(rx)
    tx[8] = 0x07
    return bytes(tx)
