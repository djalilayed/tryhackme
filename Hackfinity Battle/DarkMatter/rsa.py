# script by Gemeni for tryhackme room DarkMatter https://tryhackme.com/room/hfb1darkmatter
# script update of https://github.com/murtaza-u/zet/tree/main/20220808171808 on tryhackme room https://tryhackme.com/room/breakrsa

#!/usr/bin/python3
from gmpy2 import isqrt
from math import lcm

def factorize(n):
    if (n & 1) == 0:
        return (n // 2, 2)
    a = isqrt(n)
    if a * a == n:
        return a, a
    while True:
        a = a + 1
        bsq = a * a - n
        b = isqrt(bsq)
        if b * b == bsq:
            break
    return a + b, a - b

# --- RSA Values ---
n = 340282366920938460843936948965011886881
e = 65537

# --- Encrypted AES key ---
# The hexdump "6d64 52c1 5ca3 33a4 429a 5e45 1901 b6d7" converted to an integer
encrypted_aes_key_int = 0x6d6452c15ca333a4429a5e451901b6d7

# 1. Factor n to get p and q
p, q = factorize(n)

# 2. Calculate Lambda(n)
lambda_n = lcm(p - 1, q - 1)

# 3. Calculate the private exponent d
d = pow(e, -1, lambda_n)

print("\n")
print(f"[*] Found Prime Factors:")
print(f"p = {p}")
print(f"q = {q}\n")

# 2. Calculate Lambda(n)
# This is needed to find the private exponent.
# λ(n) = lcm(p-1, q-1)
lambda_n = lcm(p - 1, q - 1)
print(f"[*] Calculated Lambda(n):")
print(f"λ(n) = {lambda_n}\n")

print(f"[*] Private Exponent (d): {d}\n")

# --- Decryption Step ---
# 4. Decrypt the AES key using: m = c^d mod n
decrypted_key_int = pow(encrypted_aes_key_int, d, n)

print(f"[*] Decrypted AES Key (as an Integer):")
print(f"{decrypted_key_int}\n")

# 5. Convert the decrypted integer back to hex
# The format(number, 'x') converts an integer to a lowercase hex string
decrypted_key_hex = format(decrypted_key_int, 'x')

print(f"✅ Decrypted AES Key (in Hex):")
print(f"{decrypted_key_hex}")
print("\n")
