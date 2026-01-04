import logging

logger = logging.getLogger("iec104-honeypot")
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

console = logging.StreamHandler()
console.setFormatter(fmt)

file_handler = logging.FileHandler("./iec104.log")
file_handler.setFormatter(fmt)

if not logger.handlers:
    logger.addHandler(console)
    logger.addHandler(file_handler)
