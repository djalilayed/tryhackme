# script by Gemeni
# script for tryhackme room Pressed https://tryhackme.com/room/pressedroom
# script decrypt aes encrypted file exported from Wireshark
# you need to update below the key an div

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# --- Your Forensic Findings ---
KEY = b'rhI1Ya******s6MJj'
IV = b'pE****4sj'
FILENAME = 'cmd.bin' # Changed to your filename
OUTPUT_FILENAME = 'decrypted_output.bin'

# --------------------------------

try:
    with open(FILENAME, 'rb') as f:
        ciphertext = f.read()
    print(f"[*] Read {len(ciphertext)} bytes from {FILENAME}")

    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    
    decrypted_padded = cipher.decrypt(ciphertext)
    decrypted_data = unpad(decrypted_padded, AES.block_size)
    
    print("\n--- Decryption Successful --- 🔓")
    
    # --- CHANGE IS HERE ---
    # Instead of trying to print, write the raw bytes to a file.
    with open(OUTPUT_FILENAME, 'wb') as f:
        f.write(decrypted_data)
        
    print(f"[*] Decrypted binary data saved to: {OUTPUT_FILENAME}")

except FileNotFoundError:
    print(f"[!] Error: The file '{FILENAME}' was not found.")
except Exception as e:
    print(f"[!] An error occurred: {e}")
