#script by Gemini for tryhacme room Task 21 CRC Me If You Can Industrial Intrusion https://tryhackme.com/room/industrial-intrusion
# script for loal testing in case you wantn to test in your local machine.
# YouTube video walk through: https://youtu.be/-zylGSCC6cU

import socket
import struct
from gateway_proto import crc32 # Import the same CRC logic

HOST = '127.0.0.1' # Localhost
PORT = 1501

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    try:
        # 1. Receive the raw payload from the client
        command = conn.recv(1024).strip()
        if not command:
            print("[-] Received empty payload. Closing.")
            return

        # For this lab, we'll assume the command is always 4 bytes
        if len(command) != 4:
            print(f"[-] Oracle only handles 4-byte commands, got {len(command)} bytes.")
            conn.sendall(b'ERROR: ONLY 4-BYTE PAYLOADS SUPPORTED')
            return
            
        print(f"[i] Received command payload: {command.decode()}")

        # 2. Build the standard header
        header = b'\xca\xfe\x01\x04'

        # 3. Calculate the CRC of the command
        calculated_crc = crc32(command)
        print(f"[i] Calculated CRC: {hex(calculated_crc)}")
        
        # 4. Pack the CRC into 4 big-endian bytes
        crc_bytes = struct.pack('>I', calculated_crc)

        # 5. Assemble the full packet and send it back
        full_packet = header + command + crc_bytes
        print(f"[i] Sending full packet: {full_packet.hex()}")
        conn.sendall(full_packet)

    except Exception as e:
        print(f"[!] An error occurred: {e}")
    finally:
        conn.close()
        print(f"[-] Connection with {addr} closed.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] CRC-Oracle Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == '__main__':
    main()
