# script by Chatgpt
# script for tryhackme room LOVELETTER.exe  https://tryhackme.com/room/lafbctf2026-advanced
# YouTube video walk through: https://youtu.be/sRj3IAD-z0w

import base64

def decrypt(data, key):
    res = bytearray()
    for i in range(len(data)):
        res.append(data[i] ^ key[i % len(key)])
    return res

marker = b'<!--VALENTINE_PAYLOAD_START-->'
key = b'ROSES'

# Ensure roses.jpg is in the same directory
try:
    with open('roses.jpg', 'rb') as f:
        content = f.read()

    start_idx = content.find(marker)
    if start_idx != -1:
        # Extract payload after the marker, excluding the last 3 bytes as per cupid.ps1 logic
        payload = content[start_idx + len(marker):-3]
        decrypted_bytes = decrypt(payload, key)
        
        # The result is a Base64 encoded string
        b64_str = decrypted_bytes.decode('ascii').strip()
        
        # Add padding if necessary for base64 decoding
        missing_padding = len(b64_str) % 4
        if missing_padding:
            b64_str += '=' * (4 - missing_padding)
            
        # Decode Base64 to get the final VBScript
        final_payload = base64.b64decode(b64_str).decode('utf-8')
        print(final_payload)
    else:
        print('[-] Marker not found in roses.jpg')
except FileNotFoundError:
    print('[-] roses.jpg not found in the current directory')
except Exception as e:
    print(f'[-] An error occurred: {e}')
