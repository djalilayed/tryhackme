# get opt for tryhackme room TryHack3M: TriCipher Summit https://tryhackme.com/r/room/tryhack3mencryptionchallenge
# script with help of ChatGPT

import requests
from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import urllib.parse
import os

# Suppress SSL warnings (not recommended for production)
import urllib3
urllib3.disable_warnings()

# Configuration
otp_url = "https://cdn.tryhackm3.loc:5000/supersecretotp"
private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCuL9Yb8xsvKimy
lR/MJB2Z2oBXuIvIidHIVxf7+Sl3Y35sU53Vd+D1QOuJByvpLmpczYsQkUMJmKha
36ibC2gjBMlTlZJ0OwnjG+Na0libW9fnWZVKq0JuAhyJd9OUyO0Up1hk2W6/1abU
OuEcYn1CTdYrTq7pdRhKLp2kYfVo64oV+NPDgQWvaIyR9vdEA+tGa4bgm5BQENaw
0Uh6qrtBh8pFKDX9EMEizauhRAsOUVlZ6ZYWCiT+A+IGZHpzFIXWh0gRbIANDZAd
g+CATLT/jee9wi0Vvg7L4o/Xn293SIAXYK7NYEHwMZP/SSmtcasYSFfgFvZ3BX+j
OLNynG5lAgMBAAECggEABXwFGlEvwG7r7C8M1sEmW3NJSjnJ0PEh9VRksW7ZcuRj
lSaW2CNTpnU6VVCv/cIT4EMqh0WDnlg7qMzVAri7uSqL6kFR4K4BNDDrGi94Ub/1
Dtg/vp+g0lTnsB5hP5SJ/nX8bwR3m7uu6ozGDL4/ImjP/wIVuM0SjDdmiEf7UafX
iWE12Lq5RbsHnvcXte2wl09keRszatRk/ODrqMPxzjS1NSt6KBfxtiRPNB+GZt1y
DhYKaHEO0riDsUiXurMwt7bAlupiiIS0pDAfNDEnvc2gWaiir8pIFGezowd+sIOd
XSW3aJU2Y5ByroelgkovRNIpF2QPXfFSsHyzx5uQawKBgQDsnwAuzp07CaHrXyaJ
HBno149LOaGYzRucxdKFFndizY/Le7ONl4PujRV+dwATAnuo8WIz7Upitd1uuh+H
0n37G4gaKIPK0o/pNYgIpMAoWSRI9zkPyId8yBEcpMJiUYXhXziQHhYhJ3shzn/2
Rh5RDS31tCxykpe5AHATw+R60wKBgQC8c9bPRNakEftP4IkC5wriHXpwEXYWRmCf
rRmeJmfApUgGfnAWzWBu1D5eHZU5z+6iojSSyxZSGJfKedON6loySWww/ZF/1QqQ
xkS+E3S86jp1PeJVYu2DuYhfcb8AXjt4ed48DNEMR5XZeWIKCYLsACHmag1IR9cW
XmCgovO+5wKBgQDJaVp1fUfW3g8m07pwkSv4x6vgg3DrKQPtAXJ9+K6sun9A3M3s
o2EY6Jy4JkE47S8nkjheLQjZVybiPqniKik0Wq4SXhQ4y9zVzMw7V0l9zssVFONM
bQvvCjmOoSwZFn2YZj42ZnW9yOaF00mW7v6VTVumvrPq3p8pSZcdK+zLIwKBgQCm
qiwIEvFhGSYRdpq1nm/Zmgh2pHqzKHq7vPMzEvQfRA128Mtg3zGx0rN1uOQIxQRf
gOTODh4nbOiRgTy//crXPmgYy6iqTVeSwkZ5c+uCSAR7O8e3jE5SePtKreYmBTDD
U8Rfh1Y6bfTw6JD0H4VSAqv4g0JL8n0eo0kByBuZcQKBgGdaG1XJZbK4a1fQ3scR
sv8Z+HgkaKS1FY0nXShNwFaE4Tfk6f/gsTgNqbyhk+HsFelmxKoFgf0Sa7313TPR
ibFr+wDYJVOApLm9P/dg5AecXRylUKv/gbbVwBDnkCWrm48H3MY+uLqVBUZ+2jfi
c7A3LDsSigmnDbODU4muEM0Z
-----END RSA PRIVATE KEY-----'''

# You can then use this key string in your cryptographic operations as shown before.


def rot13(text):
    return text.translate(str.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"))

def encrypt_message(key, data):
    iv = b'0000000000000000'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data.encode(), AES.block_size))

def decrypt_message(key, data):
    iv = b'0000000000000000'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data), AES.block_size)

def sign_message(private_key, data):
    rsa_key = RSA.import_key(private_key)
    signer = pkcs1_15.new(rsa_key)
    h = SHA256.new(data)
    return signer.sign(h)

# Generate AES key
aes_key = os.urandom(16)

def submit_otp(otp):
    raw_data = f"otp={otp}"
    encrypted_data = b64encode(encrypt_message(aes_key, raw_data)).decode()
    signature = b64encode(sign_message(private_key, raw_data.encode())).decode()
    mac = rot13(b64encode(aes_key).decode())
    
    payload = {
        "data": encrypted_data,
        "mac": mac,
        "sign": signature
    }
    
    response = requests.post(otp_url, data=payload, verify=False)
    if response.ok:
        result = urllib.parse.unquote(response.text.split("=")[1].rstrip())
        decrypted_result = decrypt_message(aes_key, b64decode(result)).decode()
        return decrypted_result
    else:
        return response.text

# Testing OTPs from 1000 to 5000
for otp in range(1000, 5001):
    print(f"Testing OTP {otp}")
    result = submit_otp(otp)
    print(f"Response for OTP {otp}: {result}")
    if "flag" in result.lower():  # Adjust this condition based on how the correct response is worded
        print(f"Correct OTP found: {otp}")
        break
