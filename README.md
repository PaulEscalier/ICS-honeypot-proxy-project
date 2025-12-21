# ICS Honeypot Proxy

## Modbus

### Activate the pump

```Bash
modpoll -m tcp -a 1 -r 1 -c 1 -t 0 127.0.0.1 1
```

### Deactivate the pump

```Bash
modpoll -m tcp -a 1 -r 1 -c 1 -t 0 127.0.0.1 0
```

### Activate the valve

```Bash
modpoll -m tcp -a 1 -r 2 -c 1 -t 0 127.0.0.1 1
```

### Deactivate the valve

```Bash
modpoll -m tcp -a 1 -r 2 -c 1 -t 0 127.0.0.1 0
```
