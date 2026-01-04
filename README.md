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
