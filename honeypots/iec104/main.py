import asyncio
from iec104_server import start_iec104_server
from simulation import energy_simulation
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from energy_state import energy_state

import asyncio
import uvicorn
from iec104_server import start_iec104_server
from simulation import energy_simulation

app = FastAPI()
app.mount("/static", StaticFiles(directory="web_interface"), name="static")

@app.get("/")
async def index():
    return FileResponse("web_interface/index.html")

@app.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    while True:
        await ws.send_json(energy_state)
        await asyncio.sleep(1)

async def main():
    asyncio.create_task(energy_simulation())
    asyncio.create_task(start_iec104_server())

    config = uvicorn.Config(app, host="0.0.0.0", port=8002)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())