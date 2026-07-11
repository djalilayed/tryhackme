# code by Chat GPT Sol 5.6
# code for TryHackMe room Brr https://tryhackme.com/room/brr
# Video Walk Through: https://youtu.be/DCNJqR8D9Do

import socket
import struct

TARGET = "10.128.131.128"
PORT = 5020

# Modbus TCP:
# transaction=1, protocol=0, length=6
# unit=1, function=3 (read holding registers)
# start address=0, count=20
request = bytes.fromhex(
    "000100000006010300000014"
)

with socket.create_connection((TARGET, PORT), timeout=5) as sock:
    sock.sendall(request)
    response = sock.recv(1024)

byte_count = response[8]
data = response[9:9 + byte_count]

registers = struct.unpack(
    ">" + "H" * (byte_count // 2),
    data
)

print("Registers:")
for address, value in enumerate(registers):
    print("{} ==> {:04x}".format(address, value))

decoded = "".join(
    chr(value)
    for value in registers
    if 32 <= value <= 126
)

print("Decoded:", decoded)
