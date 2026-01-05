import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from state import process_state
from logger import logger
from s7_server import S7Honeypot
from process import conveyor_loop
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="web_interface"), name="static")

@app.get("/")
async def index():
    return FileResponse("web_interface/index.html")

clients = []

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            await ws.send_json(process_state)
            await asyncio.sleep(1)
    finally:
        clients.remove(ws)

honeypot = S7Honeypot()

async def fake_s7_network():
    while True:
        await asyncio.sleep(5)

async def main():
    asyncio.create_task(conveyor_loop())
    asyncio.create_task(fake_s7_network())
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

    print("[+] Siemens S7 Conveyor Honeypot running")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())