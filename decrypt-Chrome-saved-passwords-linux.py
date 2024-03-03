# original https://www.hackthebox.com/blog/seized-ca-ctf-2022-forensics-writeup
# small changes replacing action_url to origin_url and just check ciphertext is not empty
# updated with help of chatgpt
# run on linux
import os
import sqlite3
from Crypto.Cipher import AES
import csv

def get_secret_key():
    # Reads the AES key directly from the 'aes.dec' file
    secret_key = open('aes.dec', 'rb').read()
    return secret_key

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  # Ensure decoding to string
        return decrypted_pass
    except Exception as e:
        print(f"{e}")
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""

def get_db_connection(chrome_path_login_db):
    try:
        return sqlite3.connect(chrome_path_login_db)
    except Exception as e:
        print(f"{e}")
        print("[ERR] Chrome database cannot be found")
        return None

if __name__ == '__main__':
    secret_key = get_secret_key()
    # Ensure you update this path to where your Chrome 'Login Data' database is located
    chrome_path_login_db = "logindata"
    conn = get_db_connection(chrome_path_login_db)
    if secret_key and conn:
        cursor = conn.cursor()
        # Adjust the SQL query to use the correct column names from the schema
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        for index, login in enumerate(cursor.fetchall()):
            origin_url, username, ciphertext = login
            # Check if there's an encrypted password (ciphertext) to decrypt
            if ciphertext:
                decrypted_password = decrypt_password(ciphertext, secret_key)
                # Print out the login information if decryption was successful
                if decrypted_password:
                    print(f"Sequence: {index}")
                    print(f"Origin URL: {origin_url}\nUser Name: {username}\nPassword: {decrypted_password}\n")
                    print("*" * 50)
        cursor.close()
        conn.close()

