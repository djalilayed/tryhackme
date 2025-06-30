# script by Gemini Pro
# script for tryhackme room Industrial Intrusion Task-19 No Salt, No Shame
# youtube video walk through: https://youtu.be/5-U9fT4wm-s

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# --- Configuration ---
# The passphrase provided in the challenge
PASSPHRASE = 'VIRELIA-WATER-FAC'

# The name of the encrypted file to read
ENCRYPTED_FILE = 'shutdown.log-1750934543756.enc'

# The name of the file to write the decrypted content to
DECRYPTED_FILE = 'decrypted.log'

def derive_key_and_iv():
    """Derives the AES key and IV from the passphrase."""
    # 1. Derive the key by hashing the passphrase with SHA-256.
    #    The crypto library needs the raw bytes of the hash, not the hex string.
    key = hashlib.sha256(PASSPHRASE.encode('utf-8')).digest()

    # 2. The IV is 16 bytes of zeros (128 bits).
    iv = bytes(16)

    print(f"[*] Derived Key (bytes): {key.hex()}")
    print(f"[*] IV (bytes):          {iv.hex()}")
    
    return key, iv

def decrypt_file(key, iv):
    """Decrypts the file using the derived key and IV."""
    try:
        # Read the encrypted file content as binary data
        with open(ENCRYPTED_FILE, 'rb') as f_in:
            encrypted_data = f_in.read()
        
        print(f"[+] Read {len(encrypted_data)} bytes from {ENCRYPTED_FILE}")

        # Create a new AES cipher object in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt the data
        decrypted_padded_data = cipher.decrypt(encrypted_data)

        # Remove the PKCS7 padding from the decrypted data
        # This step will fail if the key is wrong, as the padding will be invalid.
        plaintext = unpad(decrypted_padded_data, AES.block_size)
        
        # Write the decrypted plaintext to the output file
        with open(DECRYPTED_FILE, 'wb') as f_out:
            f_out.write(plaintext)
            
        print(f"\n[SUCCESS] Decryption successful!")
        print(f"[*] Plaintext saved to {DECRYPTED_FILE}")
        print("[*] Now search that file for the flag!")

    except FileNotFoundError:
        print(f"[ERROR] The file '{ENCRYPTED_FILE}' was not found. Make sure it's in the same directory.")
    except ValueError as e:
        # This error is almost always caused by an incorrect key or IV,
        # which results in garbage data that can't be unpadded correctly.
        print(f"\n[ERROR] Decryption failed! This is likely due to an incorrect key or IV.")
        print(f"        The padding is invalid, which is a classic sign of a decryption error.")
        print(f"        Underlying error: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")


if __name__ == '__main__':
    derived_key, derived_iv = derive_key_and_iv()
    decrypt_file(derived_key, derived_iv)
