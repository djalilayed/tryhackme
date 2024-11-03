# script with assistance of ChatGPT
# script for tryhackme room SeeTwo https://tryhackme.com/r/room/seetworoom
# this script read wireshark.txt the result from: tshark -r y capture.pcap -Y "tcp.port == 1337" -T fields -e data > wireshark.txt

import re
import base64

# Define the XOR key
key = "MySup3rXoRKeYForCommandandControl".encode("utf-8")

def xor_crypt(data, key):
    """XOR encryption/decryption."""
    key_length = len(key)
    encrypted_data = bytearray()
    for i, byte in enumerate(data):
        encrypted_data.append(byte ^ key[i % key_length])
    return bytes(encrypted_data)

# Load the data from the file containing hex payloads
file_path = 'wireshark.txt'
with open(file_path, 'r') as file:
    hex_data_lines = file.readlines()

# Process each line of hex data
for i, line in enumerate(hex_data_lines, start=1):
    try:
        # Convert hex string to bytes
        packet_data = bytes.fromhex(line.strip())
        
        # Decode packet data to UTF-8 to search for separator pattern
        packet_text = packet_data.decode("utf-8", errors="ignore")
        
        # Find the separator "AAAAAAAAAA" followed by base64 data
        matches = re.findall(r"AAAAAAAAAA([A-Za-z0-9+/]+={0,2})", packet_text)
        
        for j, encoded_command in enumerate(matches, start=1):
            try:
                # Base64 decode and XOR decrypt the command
                decoded_command = base64.b64decode(encoded_command.encode("utf-8"))
                decrypted_command = xor_crypt(decoded_command, key).decode("utf-8")
                
                print(f"Decoded Command {i}-{j}: {decrypted_command}")
                
            except Exception as e:
                print(f"Error decoding command in packet {i}, match {j}: {e}")
                
    except ValueError as e:
        print(f"Skipping line {i}: not valid hex data ({e})")
