# script from https://www.hackthebox.com/blog/seized-ca-ctf-2022-forensics-writeup
# used on tryhackme chrome room
import json
import base64

fh = open('AppData/Local/Google/Chrome/User Data/Local State', 'rb')
encrypted_key = json.load(fh)

encrypted_key = encrypted_key['os_crypt']['encrypted_key']

decrypted_key = base64.b64decode(encrypted_key)

open("dec_data",'wb').write(decrypted_key[5:])
