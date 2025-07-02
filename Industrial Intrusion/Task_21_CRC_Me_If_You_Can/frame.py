#script by ChatGPT for tryhacme room Task 21 CRC Me If You Can Industrial Intrusion https://tryhackme.com/room/industrial-intrusion
# YouTube video walk through: https://youtu.be/-zylGSCC6cU

#!/usr/bin/env python3
import sys
from gateway_proto import crc32

MAGIC   = b"\xCA\xFE"
VERSION = b"\x01"   # single-layer

def make_frame(payload: bytes) -> bytes:
    # support piping in text or bytes
    if not isinstance(payload, (bytes, bytearray)):
        payload = payload.encode()

    if len(payload) > 0xFF:
        raise ValueError("payload too big for 1-byte length")

    length = len(payload).to_bytes(1, "big")
    # CRC must be packed big-endian
    trailer = crc32(payload).to_bytes(4, "big")

    return MAGIC + VERSION + length + payload + trailer

if __name__ == "__main__":
    data = sys.stdin.buffer.read()
    sys.stdout.buffer.write(make_frame(data))
