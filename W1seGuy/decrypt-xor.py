# usage: decrypt-xor.py -e 'xor encoded text'
# this script with help of ChatGPT and Gemini
# TryHackMe room W1seGuy https://tryhackme.com/r/room/w1seguy

import binascii
import string
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

def find_key_start(encrypted_text, known_start):
    """
    Attempts to find the first few characters of the key using XOR and a known decrypted text start.

    Args:
        encrypted_text (str): The encrypted text in hex format.
        known_start (str): The known start of the decrypted text (e.g., "THM{").

    Returns:
        str: The potential key start (first few characters) derived from XOR.
    """

    # Convert the encrypted text from hex to bytes
    encrypted_bytes = binascii.unhexlify(encrypted_text)

    # Determine the length to iterate over
    num_iterations = min(len(encrypted_bytes), len(known_start))

    # Initialize an empty string to store the derived key start
    key_start = ""

    # Loop through the encrypted text and corresponding expected decrypted characters
    for i in range(num_iterations):
        # Perform XOR operation to get the key character at this position
        key_char = chr(encrypted_bytes[i] ^ ord(known_start[i]))
        key_start += key_char

    return key_start

def xor_decode(hex_encoded, key):
    """
    Decodes a hex-encoded string using a provided key with XOR.

    Args:
        hex_encoded (str): The hex-encoded string.
        key (str): The key for XOR decryption.

    Returns:
        str: The decoded string.
    """
    xored = binascii.unhexlify(hex_encoded)
    decoded = ''.join(chr(xored[i] ^ ord(key[i % len(key)])) for i in range(len(xored)))
    return decoded

def test_key(key, hex_encoded, known_start, known_end):
    """
    Tests a given key by attempting to decode the hex-encoded string and checking if it starts and ends with the known values.

    Args:
        key (str): The key to test.
        hex_encoded (str): The hex-encoded string.
        known_start (str): The known start of the decoded flag.
        known_end (str): The known end of the decoded flag.

    Returns:
        tuple: The key and decoded flag if valid, otherwise None.
    """
    decoded_flag = xor_decode(hex_encoded, key)
    if decoded_flag.startswith(known_start) and decoded_flag.endswith(known_end):
        return key, decoded_flag
    return None

def generate_and_test_keys_with_prefix(hex_encoded, known_start, known_end, prefix):
    """
    Generates and tests all possible keys with the given prefix to find valid flags.

    Args:
        hex_encoded (str): The hex-encoded string.
        known_start (str): The known start of the decoded flag.
        known_end (str): The known end of the decoded flag.
        prefix (str): The prefix of the key.

    Returns:
        list: A list of tuples containing the valid keys and decoded flags.
    """
    key_length = 5  # Total key length is 5
    remaining_length = key_length - len(prefix)
    valid_chars = string.ascii_letters + string.digits
    matching_flags = []

    with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
        futures = []
        key_iterator = (prefix + ''.join(key_tuple) for key_tuple in itertools.product(valid_chars, repeat=remaining_length))

        for key in key_iterator:
            futures.append(executor.submit(test_key, key, hex_encoded, known_start, known_end))

        for future in as_completed(futures):
            result = future.result()
            if result:
                matching_flags.append(result)
                # Continue processing to find all valid flags

    return matching_flags

def main():
    parser = argparse.ArgumentParser(description='Find key and decode XOR encrypted data.')
    parser.add_argument('-e', '--encrypted', type=str, help='Hex-encoded encrypted data', required=True)

    args = parser.parse_args()

    known_start = "THM{"  # Known start of the flag format
    known_end = "}"  # Known end of the flag format

    # Find the initial key characters
    prefix = find_key_start(args.encrypted, known_start)
    print(f"Potential Key Start: {prefix}")

    # Find the key and flags using the determined prefix
    try:
        matching_flags = generate_and_test_keys_with_prefix(args.encrypted, known_start, known_end, prefix)
        if matching_flags:
            for key, flag in matching_flags:
                print(f"Derived Key: {key}")
                print(f"Decoded Flag: {flag}")
        else:
            print("No valid flag found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
