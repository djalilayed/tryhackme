# script with assistance of ChatGPT
# script for tryhackme room SeeTwo https://tryhackme.com/r/room/seetworoom
# this script read directly capture.pcap provided.

import pyshark
import base64
import re

# Define the XOR key
key = "MySup3rXoRKeYForCommandandControl".encode("utf-8")

def xor_crypt(data, key):
    """XOR encryption/decryption."""
    key_length = len(key)
    encrypted_data = bytearray()
    for i, byte in enumerate(data):
        encrypted_data.append(byte ^ key[i % key_length])
    return bytes(encrypted_data)

# Path to the pcap file
pcap_path = 'capture.pcap'  # Replace with the path to your pcap file

# Load pcap and filter packets by port 1337
packets = pyshark.FileCapture(pcap_path, display_filter="tcp.port == 1337")

# Process each packet
for i, packet in enumerate(packets, start=1):
    try:
        # Ensure the packet has TCP layer and payload data
        if 'TCP' in packet and hasattr(packet.tcp, 'payload'):
            # Extract the hex payload and convert it to bytes
            hex_data = packet.tcp.payload.replace(':', '')
            packet_data = bytes.fromhex(hex_data)
            
            # Decode to UTF-8 to look for the pattern
            packet_text = packet_data.decode("utf-8", errors="ignore")
            
            # Find the separator "AAAAAAAAAA" followed by base64 data
            matches = re.findall(r"AAAAAAAAAA([A-Za-z0-9+/]+={0,2})", packet_text)
            
            for j, encoded_command in enumerate(matches, start=1):
                try:
                    # Decode and decrypt the command
                    decoded_command = base64.b64decode(encoded_command.encode("utf-8"))
                    decrypted_command = xor_crypt(decoded_command, key).decode("utf-8")
                    
                    print(f"Decoded Command {i}-{j}: {decrypted_command}")
                    
                except Exception as e:
                    print(f"Error decoding command in packet {i}, match {j}: {e}")
    except AttributeError:
        # Skip packets without the TCP layer or payload attribute
        print(f"Skipping packet {i} due to missing attributes.")

# Close the pcap file
packets.close()
