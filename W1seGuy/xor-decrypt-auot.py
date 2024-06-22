# usage: decrypt-xor.py -H Ip -P port
# this script with help of ChatGPT and Gemini
# TryHackMe room W1seGuy https://tryhackme.com/r/room/w1seguy

import socket
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
    encrypted_bytes = binascii.unhexlify(encrypted_text)
    num_iterations = min(len(encrypted_bytes), len(known_start))
    key_start = ""
    for i in range(num_iterations):
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

def interact_with_server(host, port):
    """
    Connects to the server, retrieves the XOR encoded text, decodes it, sends back the key,
    and retrieves the final flag.

    Args:
        host (str): The server host.
        port (int): The server port.

    Returns:
        str: The final flag received from the server.
    """
    known_start = "THM{"  # Known start of the flag format
    known_end = "}"  # Known end of the flag format

    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Receive the initial message with the XOR encoded text
        initial_message = s.recv(4096).decode()
        print(f"Server message: {initial_message}")

        # Extract the XOR encoded text from the message
        xor_encoded_text = initial_message.split(': ')[1].strip()

        # Find the initial key characters
        prefix = find_key_start(xor_encoded_text, known_start)
        print(f"Potential Key Start: {prefix}")

        # Find the key and flags using the determined prefix
        matching_flags = generate_and_test_keys_with_prefix(xor_encoded_text, known_start, known_end, prefix)
        if matching_flags:
            key, decoded_flag = matching_flags[0]
            print(f"Derived Key: {key}")
            print(f"Decoded Flag 1: {decoded_flag}")

            # Wait for the server to ask for the encryption key
            key_request_message = s.recv(4096).decode()
            print(f"Server message: {key_request_message}")

            # Send the key back to the server
            print("Sending key to server...")
            s.sendall((key + '\n').encode())

            # Wait for the final flag
            print("Waiting for server reply...")
            final_flag = s.recv(4096).decode().strip()
            print(f"Final Flag: {final_flag}")
            return final_flag
        else:
            print("No valid flag found.")
            return None

def main():
    parser = argparse.ArgumentParser(description='Find key and decode XOR encrypted data.')
    parser.add_argument('-e', '--encrypted', type=str, help='Hex-encoded encrypted data')
    parser.add_argument('-H', '--host', type=str, help='Server host', required=True)
    parser.add_argument('-P', '--port', type=int, help='Server port', required=True)

    args = parser.parse_args()

    if args.encrypted:
        known_start = "THM{"  # Known start of the flag format
        known_end = "}"  # Known end of the flag format

        # Find the initial key characters
        prefix = find_key_start(args.encrypted, known_start)
        print(f"Potential Key Start: {prefix}")

        # Find the key and flags using the determined prefix
        matching_flags = generate_and_test_keys_with_prefix(args.encrypted, known_start, known_end, prefix)
        if matching_flags:
            for key, flag in matching_flags:
                print(f"Derived Key: {key}")
                print(f"Decoded Flag: {flag}")
        else:
            print("No valid flag found.")
    else:
        interact_with_server(args.host, args.port)

if __name__ == "__main__":
    main()
