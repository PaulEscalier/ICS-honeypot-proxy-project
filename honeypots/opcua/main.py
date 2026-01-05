import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from state import state
import asyncio
import uvicorn
from server import run as opcua_server
from simulation import thermal_simulation

app = FastAPI()

app.mount("/static", StaticFiles(directory="web_interface"), name="static")

@app.get("/")
async def index():
    return FileResponse("web_interface/index.html")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        await ws.send_json(state)
        await asyncio.sleep(1)

async def main():
    asyncio.create_task(thermal_simulation())

    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, opcua_server)

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8003,
        log_level="warning"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
