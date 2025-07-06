# script by ChatGPT and Gemini for tryhackme room https://tryhackme.com/room/hfb1cipherssecretmessage
# youtube video walk through: https://youtu.be/NZJB_1D8YbM
# how to use: python3 decrypt.py 'a_up4qr_kaiaf0_bujktaz_qm_su4ux_cpbq_ETZ_rhrudm'

#!/usr/bin/env python3
import sys

def dec(ciphertext: str) -> str:
    """
    Reverse of enc(): shift each letter backward by its index in the string.
    Non-alpha characters are left as-is (but still count toward the index).
    """
    plain = []
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            decoded_ord = (ord(c) - base - i) % 26 + base
            plain.append(chr(decoded_ord))
        else:
            plain.append(c)
    return "".join(plain)

def usage():
    print(f"Usage: {sys.argv[0]} 'ciphertext'")
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    cipher = sys.argv[1]
    flag = dec(cipher)
    print(flag)
