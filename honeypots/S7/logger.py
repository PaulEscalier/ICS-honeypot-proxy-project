import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("s7-honeypot")
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

console = logging.StreamHandler()
console.setFormatter(fmt)

file_handler = RotatingFileHandler(
    "./S7.log",
    maxBytes=5_000_000,
    backupCount=5
)


file_handler.setFormatter(fmt)

if not logger.handlers:
    logger.addHandler(console)
    logger.addHandler(file_handler)
