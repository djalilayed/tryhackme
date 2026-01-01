# script by ChatGPT
# sript for tryhackme room BreachBlocker Unlocker https://tryhackme.com/room/sq4-aoc2025-32LoZ4zePK
# YouTube video walk through: https://youtu.be/xINJWj8zcrQ

#!/usr/bin/env python3
import sqlite3
import hashlib
import string

DB_PATH = "hopflix-874297.db"
TARGET_EMAIL = "sbreachblocker@easterbunnies.thm"  # change if needed

def hopper_hash(s: str) -> str:
    res = s
    for _ in range(1000):
        res = hashlib.sha1(res.encode()).hexdigest()
    return res

def build_lookup(charset: str) -> dict[str, str]:
    # hash -> character
    lookup = {}
    for ch in charset:
        lookup[hopper_hash(ch)] = ch
    return lookup

def main():
    # Likely enough: all printable ASCII except whitespace controls
    charset = "".join(chr(i) for i in range(32, 127))
    lookup = build_lookup(charset)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    row = cur.execute("SELECT * FROM users WHERE email = ?", (TARGET_EMAIL,)).fetchone()
    if not row:
        raise SystemExit("Email not found in DB.")

    phash = row[2]  # matches rows[0][2] in main.py
    if len(phash) % 40 != 0:
        print(f"[!] Hash length {len(phash)} not divisible by 40; still trying chunking...")

    chunks = [phash[i:i+40] for i in range(0, len(phash), 40)]

    out = []
    unknown = 0
    for idx, chunk in enumerate(chunks):
        ch = lookup.get(chunk)
        if ch is None:
            out.append("?")
            unknown += 1
        else:
            out.append(ch)

    password = "".join(out)
    print("[+] Recovered password (best effort):", password)
    if unknown:
        print(f"[!] {unknown} characters unknown. Expand charset (e.g., unicode) if needed.")

if __name__ == "__main__":
    main()
