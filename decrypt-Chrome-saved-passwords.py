# original https://www.hackthebox.com/blog/seized-ca-ctf-2022-forensics-writeup
# small changes replacing action_url to origin_url and just check ciphertext is not empty
# run on windows machine
import os
import re
import sys
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv

def get_secret_key():
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
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""

def get_db_connection(chrome_path_login_db):
    try:
        return sqlite3.connect(chrome_path_login_db)
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome database cannot be found")
        return None

if __name__ == '__main__':
    secret_key = get_secret_key()
    chrome_path_login_db = r"AppData\Local\Google\Chrome\User Data\Default\Login Data"
    conn = get_db_connection(chrome_path_login_db)
    if(secret_key and conn):
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        for index,login in enumerate(cursor.fetchall()):
            url = login[0]
            username = login[1]
            ciphertext = login[2]
            if(ciphertext!=""):
                decrypted_password = decrypt_password(ciphertext, secret_key)
                print("Sequence: %d"%(index))
                print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password))
                print("*"*50)
        cursor.close()
        conn.close()
