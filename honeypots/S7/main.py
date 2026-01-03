import asyncio
import threading
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from process_simulation import process_loop
import threading

from s7_server import start_s7_server
from s7_memory import plc_memory
from logger import logger

app = FastAPI()
app.mount("/static", StaticFiles(directory="web_interface"), name="static")


@app.get("/")
async def index():
    return FileResponse("web_interface/index.html")


@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    ip = ws.client.host
    logger.info(f"HMI WebSocket connected from {ip}")

    try:
        while True:
            await ws.send_json(plc_memory.read())
            await asyncio.sleep(1)
    except Exception:
        logger.info(f"HMI WebSocket disconnected {ip}")


def start_web():
    uvicorn.run(app, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    threading.Thread(target=start_s7_server, daemon=True).start()
    threading.Thread(target=process_loop, daemon=True).start()
    start_web()
