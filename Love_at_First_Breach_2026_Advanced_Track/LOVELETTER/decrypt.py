# script by Gemin
# script for tryhackme room LOVELETTER.exe  https://tryhackme.com/room/lafbctf2026-advanced
# YouTube video walk through: https://youtu.be/sRj3IAD-z0w


#!/usr/bin/env python3
from pathlib import Path

ks = Path("keystream.bin").read_bytes()
if not ks:
    raise SystemExit("keystream.bin is empty")

for p in Path(".").glob("*.enc"):
    ct = p.read_bytes()
    if len(ct) > len(ks):
        print(f"[!] {p.name}: ciphertext longer than keystream ({len(ct)} > {len(ks)})")
        continue
    pt = bytes(ct[i] ^ ks[i] for i in range(len(ct)))
    out = p.with_suffix(p.suffix + ".dec")
    out.write_bytes(pt)
    print(f"[+] {p.name} -> {out.name} ({len(pt)} bytes)")
