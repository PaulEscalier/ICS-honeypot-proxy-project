import c104
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

c104.set_debug_mode(
        c104.Debug.Server |
        c104.Debug.Connection |
        c104.Debug.Point |
        c104.Debug.Callback
    )

async def main():
    server = c104.Server()
    print(server.ip, server.port)
    station = server.add_station(common_address=47)
    server.start()
    print("Server started and listening on 2404")

    # Keep the server running forever
    forever = asyncio.Event()
    await forever.wait()

if __name__ == "__main__":
    asyncio.run(main())
