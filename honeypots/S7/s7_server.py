import socket
from logger import logger

COTP_CC = bytes.fromhex(
    "03 00 00 16"
    "11 D0 00 00 00 01 00"
    "C1 02 01 00"
    "C2 02 01 02"
    "C0 01 0A"
)

def start_s7_server(host="0.0.0.0", port=102):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    logger.info(f"S7 honeypot listening on {host}:{port}")

    while True:
        conn, addr = sock.accept()
        ip, src_port = addr
        logger.info(f"S7 connection from {ip}:{src_port}")

        try:
            data = conn.recv(1024)
            logger.info(f"RX {ip}: {data.hex()}")

            conn.sendall(COTP_CC)
            logger.info(f"TX {ip}: COTP CC")

            while True:
                payload = conn.recv(1024)
                if not payload:
                    break
                logger.info(f"S7 DATA {ip}: {payload.hex()}")

        except Exception as e:
            logger.warning(f"Error with {ip}: {e}")
        finally:
            conn.close()
            logger.info(f"Connection closed {ip}")
