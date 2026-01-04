import asyncio
from logger import logger
from iec104_asdu import handle_asdu

STARTDT_ACT = b"\x68\x04\x07\x00\x00\x00"
STARTDT_CON = b"\x68\x04\x0b\x00\x00\x00"

TESTFR_ACT = b"\x68\x04\x43\x00\x00\x00"
TESTFR_CON = b"\x68\x04\x83\x00\x00\x00"

class IEC104Server:
    async def handle_client(self, reader, writer):
        peer = writer.get_extra_info("peername")
        logger.info(f"Client connected: {peer}")

        while True:
            data = await reader.read(1024)
            if not data:
                break

            logger.info(f"RX {peer}: {data.hex()}")

            # STARTDT
            if data == STARTDT_ACT:
                logger.info("STARTDT ACT")
                writer.write(STARTDT_CON)

            # TESTFR
            elif data == TESTFR_ACT:
                logger.info("TESTFR ACT")
                writer.write(TESTFR_CON)

            # Interrogation (C_IC_NA_1)
            elif b"\x64\x01" in data:
                logger.info("Interrogation command received")
                writer.write(self.interrogation_response())
            elif len(data) > 6 and data[6] == 0x2D:
                logger.info("Single Command received")
                response = handle_asdu(data)
                if response:
                    writer.write(response)

            await writer.drain()

        logger.info(f"Client disconnected: {peer}")

    def interrogation_response(self):
        # ASDU very basic (cause: activation confirmation)
        return (
            b"\x68\x0e"          # APCI
            b"\x00\x00\x00\x00"
            b"\x64"              # Type: C_IC_NA_1
            b"\x01"              # SQ
            b"\x07\x00"          # Cause: activation confirmation
            b"\x01\x00"          # ASDU addr
            b"\x00\x00\x00"      # IOA
        )

async def start_iec104_server():
    server = IEC104Server()
    srv = await asyncio.start_server(
        server.handle_client,
        "0.0.0.0",
        2404
    )

    logger.info("IEC 60870-5-104 server listening on port 2404")

    async with srv:
        await srv.serve_forever()
