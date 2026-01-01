# script by ChatGPT
# python3 image_decode.py 5ed5961c6276df568891c3ea-1765955075920.png -v -o sq4_key.png
# script to reverse image encoding.
# script fot getting key for tryhackme room Carrotbane of My Existence Side Quest
# YouTube video: https://youtu.be/8OQX9d6igKA

#!/usr/bin/env python3
import argparse
import base64
import re
import zlib
from pathlib import Path
from PIL import Image

B32_ALLOWED = re.compile(rb'[^A-Z2-7=\n\r01a-z]')  # keep 0/1 just in case; we’ll map them if needed

def xor_repeat(data: bytes, key: bytes) -> bytes:
    out = bytearray(len(data))
    klen = len(key)
    for i, b in enumerate(data):
        out[i] = b ^ key[i % klen]
    return bytes(out)

def rot_letters_only(data: bytes, shift: int) -> bytes:
    """Rotate A-Z / a-z only. Digits unchanged (matches ROT13(..., rotateNumbers=false))."""
    s = shift % 26
    out = bytearray()
    for b in data:
        if 65 <= b <= 90:
            out.append((b - 65 + s) % 26 + 65)
        elif 97 <= b <= 122:
            out.append((b - 97 + s) % 26 + 97)
        else:
            out.append(b)
    return bytes(out)

def inflate_adaptive(blob: bytes) -> bytes:
    """CyberChef Inflate 'Adaptive' equivalent: try zlib wrapper, then raw deflate."""
    for wbits in (15, -15):
        try:
            return zlib.decompress(blob, wbits)
        except zlib.error:
            pass
    raise zlib.error("Could not inflate (zlib or raw deflate).")

def extract_pixel_bytes(image_path: Path) -> bytes:
    img = Image.open(image_path).convert("L")
    raw = bytes(img.getdata())
    return raw.rstrip(b"\x00")

def clean_text(raw: bytes) -> bytes:
    # Accept lowercase too, then normalize
    raw = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    raw = B32_ALLOWED.sub(b"", raw)
    return raw.strip()

def split_base32_chunks(b32_text: bytes) -> list[bytes]:
    """
    Split merged Base32 into decodable chunks.
    Prefer newline chunks if present; otherwise split at padding runs (={1,6}).
    """
    t = b32_text.strip()
    if b"\n" in t:
        chunks = [c.strip() for c in t.split(b"\n") if c.strip()]
        return chunks

    # No newlines: likely multiple Base32 strings concatenated, each with its own padding.
    # Split at padding runs: keep the padding with the chunk.
    chunks = []
    i = 0
    n = len(t)
    while i < n:
        # find next padding run
        m = re.search(rb'={1,6}', t[i:])
        if not m:
            chunks.append(t[i:])
            break
        end = i + m.end()  # include '=' padding
        chunks.append(t[i:end])
        i = end
        # skip any extra '=' (paranoia)
        while i < n and t[i:i+1] == b"=":
            i += 1
    return [c for c in chunks if c]

def b32_decode_one(chunk: bytes) -> bytes:
    c = chunk.strip().upper()

    # Some dumps accidentally include 0/1; allow RFC3548 mappings:
    # 0 -> O always; 1 -> I or L depending on map01.
    # Also: remove *internal* whitespace (shouldn't exist, but safe).
    c = b"".join(c.split())

    # Padding: ensure length multiple of 8 for base32 decoder
    pad = (8 - (len(c) % 8)) % 8
    if pad:
        c += b"=" * pad

    # Try strict first, then map01 options
    for map01 in (None, b"I", b"L"):
        try:
            return base64.b32decode(c, casefold=True, map01=map01)
        except Exception:
            continue
    raise ValueError("Base32 decode failed for a chunk (bad alphabet or padding).")

def reverse_loop(pre_fork: bytes, passes: int) -> bytes:
    """
    Invert the Jump loop correctly:
    Encoder per-pass: ROT(+7 letters-only) THEN Split('H0' -> 'H0\\n')
    Decoder per-pass: unsplit('H0\\n' -> 'H0') THEN ROT(-7)
    Repeat passes times.
    """
    data = pre_fork
    for _ in range(passes):
        data = data.replace(b"H0\n", b"H0")
        data = rot_letters_only(data, -7)
    return data

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=Path("out.bin"))
    ap.add_argument("--passes", type=int, default=9, help="Jump('encoder1',8) => 9 passes total")
    ap.add_argument("--key", default="h0pp3r")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    raw = extract_pixel_bytes(args.image)
    b32_text = clean_text(raw)

    if args.verbose:
        print(f"[+] Extracted {len(raw)} bytes from pixels")
        print(f"[+] Clean Base32-ish text length: {len(b32_text)}")
        print(f"[+] Newlines: {b32_text.count(b'\\n')}  '=' count: {b32_text.count(b'=')}")
        print(f"[+] Preview: {b32_text[:120]!r}")

    chunks = split_base32_chunks(b32_text)
    if args.verbose:
        print(f"[+] Chunks found: {len(chunks)}")
        for i, c in enumerate(chunks[:3], 1):
            print(f"    chunk{i}: len={len(c)} preview={c[:60]!r}")

    # Decode each fork/base32 chunk independently: Base32 -> XOR -> Inflate
    inflated = []
    key = args.key.encode("utf-8")
    for i, ch in enumerate(chunks, 1):
        try:
            dec = b32_decode_one(ch)
            dec = xor_repeat(dec, key)
            dec = inflate_adaptive(dec)
            inflated.append(dec)
        except Exception as e:
            if i <= 3 or args.verbose:
                print(f"[!] Chunk {i} failed: {e}")
            # If too many fail, something upstream is wrong:
            # keep going to see if at least some chunks decode.
            continue

    if not inflated:
        raise SystemExit("[!] No chunks inflated successfully. (Likely wrong chunk splitting or wrong key.)")

    # Reconstruct pre-fork stream (Fork split delimiter is '\n')
    pre_fork = b"\n".join(inflated)

    # Reverse the loop (Split+ROT repeated)
    post_loop = reverse_loop(pre_fork, args.passes)

    # Base64 decode
    b64 = b"".join(post_loop.split())
    out = base64.b64decode(b64, validate=False)

    args.out.write_bytes(out)
    print(f"[+] Wrote {len(out)} bytes to {args.out}")

    # quick signature hint
    if out.startswith(b"\x89PNG\r\n\x1a\n"):
        print("[+] Looks like PNG")
    elif out.startswith(b"\xff\xd8\xff"):
        print("[+] Looks like JPEG")
    elif out.startswith(b"GIF8"):
        print("[+] Looks like GIF")

if __name__ == "__main__":
    main()
