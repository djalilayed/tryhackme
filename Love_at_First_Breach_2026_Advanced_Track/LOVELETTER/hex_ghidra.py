# script by Gemin
# script for tryhackme room LOVELETTER.exe  https://tryhackme.com/room/lafbctf2026-advanced
# YouTube video walk through: https://youtu.be/sRj3IAD-z0w

def decrypt(hex_string):
    # Convert hex string to a list of integers
    encrypted_bytes = bytes.fromhex(hex_string)
    
    decrypted_chars = []
    
    for i, byte in enumerate(encrypted_bytes):
        # The logic from Ghidra: (index * 41) ^ byte ^ 0x4C
        # We use & 0xFF to ensure the multiplication stays within byte limits
        key_part = (i * 0x29) & 0xFF 
        decrypted_char = key_part ^ byte ^ 0x4C
        
        decrypted_chars.append(chr(decrypted_char))
    
    return "".join(decrypted_chars)

# --- PUT YOUR HEX HERE ---
# Example: If Ghidra shows "12 4A F3..." put it here
# First string (local_28, len 10) from 0x2b9da9020
hex_data = "24 11 6a 47 d2 ae 95 3f 6b 5c b2 ea d2 77 01 5c b9 90 da 2f 1d" 

print(f"Decrypted: {decrypt(hex_data)}")
