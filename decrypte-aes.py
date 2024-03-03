# help from chat gpt
# decrypt file encrypted using aes symetric encryption
# tryhackme room chrome

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def decrypt_file(key, iv, input_file_path, output_file_path):
    # Read the encrypted data from the file
    with open(input_file_path, "rb") as file:
        encrypted_data = file.read()

    # Create a Cipher object to manage the decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data and write it to the output file
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    with open(output_file_path, "wb") as file:
        file.write(decrypted_data)

    print("File decrypted and saved successfully.")

if __name__ == "__main__":
    # The AES key and IV must be bytes, so we convert the provided strings
    key = b"PjoM95MpBdz85Kk7ewcXSLWCoAr7mRj1"
    iv = b"lR3soZqkaWZ9ojTX"

    # Specify the paths to your encrypted file and the output decrypted file
    input_file_path = "encrypted_files"
    output_file_path = "decrypted_files.zip"

    # Ensure the paths are correct and accessible
    decrypt_file(key, iv, input_file_path, output_file_path)
