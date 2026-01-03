import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from logger import logger

from modbus_server import create_context, create_identity, start_modbus
from process import process_loop
from state import process_state

app = FastAPI()
app.mount("/static", StaticFiles(directory="web_interface"), name="static")

@app.get("/")
async def index():
    return FileResponse("web_interface/index.html")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host
    path = request.url.path
    method = request.method

    logger.info(f"{client_ip} {method} {path}")

    return await call_next(request)

@app.websocket("/ws")
async def websocket(ws: WebSocket):
    client_ip = ws.client.host
    logger.info(f"WebSocket connected from {client_ip}")

    await ws.accept()

    try:
        while True:
            await ws.send_json(process_state)
            await asyncio.sleep(1)
    except Exception as e:
        logger.warning(f"WebSocket disconnected ({client_ip})")

async def main():
    context = create_context()
    identity = create_identity()

    # Tâches background
    asyncio.create_task(process_loop(context))
    asyncio.create_task(start_modbus(context, identity))

    # Uvicorn ASYNC (IMPORTANT)
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
