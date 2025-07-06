# script by ChatGPT and Gemini for tryhackme room https://tryhackme.com/room/hfb1cipherssecretmessage
# youtube video walk through: https://youtu.be/NZJB_1D8YbM
# how to use: python3 encrypt_debug_g.py 'tryhackme'

#!/usr/bin/env python3
import sys

def enc_debug(plaintext: str) -> str:
    """
    Same as enc(), but prints each step of the shift for learning.
    """
    result = []
    for i, c in enumerate(plaintext):
        print("-" * 70) # Adds a separator for clarity
        if c.isalpha():
            # Decide whether we're in A–Z or a–z
            base = ord('A') if c.isupper() else ord('a')
            ord_c = ord(c)
            alpha_index = ord_c - base
            shifted = (alpha_index + i) % 26
            final_ascii = shifted + base
            encoded_char = chr(final_ascii)

            # Updated, more detailed debug output
            print(
                f"[{i:>2}] Character: '{c}' (ASCII: {ord_c}) | Base: '{chr(base)}' ({base})\n"
                f"    ► Alpha Index: (ASCII - Base) → ({ord_c} - {base}) = {alpha_index}\n"
                f"    ► Shifted Index: (Alpha Index + Index) % 26 → ({alpha_index} + {i}) % 26 = {shifted}\n"
                f"    ► New ASCII: (Shifted Index + Base) → ({shifted} + {base}) = {final_ascii}\n"
                f"    ► Result: chr({final_ascii}) → '{encoded_char}'"
            )

            result.append(encoded_char)
        else:
            # Non‐letters stay the same (but still count in the index)
            print(f"[{i:>2}] Character: '{c}' is not a letter. Leaving unchanged.")
            result.append(c)
    return "".join(result)

def usage():
    print(f"Usage: {sys.argv[0]} 'your plaintext here'")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    pt = sys.argv[1]
    print("\n--- Encoding Steps ---")
    cipher = enc_debug(pt)
    print("\n" + "="*28 + " RESULT " + "="*28)
    print(f"Plaintext:  {pt}")
    print(f"Ciphertext: {cipher}")
    print("=" * 64)
