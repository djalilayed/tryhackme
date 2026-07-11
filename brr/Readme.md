#Modbus has separate memory areas:
```
01  Read coils
02  Read discrete inputs
03  Read holding registers
04  Read input registers
```


```
0000  starting address 0
0014  read 20 registers
```
```
0x14 is decimal 20.
```
```
python3 - <<'PY'
import socket

target = "10.128.131.128"
port = 5020

request = bytes.fromhex(
    "000100000006010300000001"
)

with socket.create_connection((target, port), timeout=5) as sock:
    sock.sendall(request)
    response = sock.recv(1024)

print(response.hex())
PY
```

```
0001  Transaction ID
0000  Protocol ID
0005  Length
01    Unit ID
03    Function code
02    Byte count
0054  Register value
```
