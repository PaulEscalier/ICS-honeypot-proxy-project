import time
import logging
from snap7.server import Server

logging.basicConfig(level=logging.INFO)

def main():
    srv = Server()

    srv.start(102)
    print("S7 server started")
    try:
        while True:
            event = srv.pick_event()
            if event:
                print("Event:", srv.event_text(event))
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Stopping server...")
        srv.stop()
        srv.destroy()

if __name__ == "__main__":
    main()
