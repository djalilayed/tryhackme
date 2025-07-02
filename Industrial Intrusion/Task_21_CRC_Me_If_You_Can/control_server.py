#script by Gemini for tryhacme room Task 21 CRC Me If You Can Industrial Intrusion https://tryhackme.com/room/industrial-intrusion
# script for loal testing in case you wantn to test in your local machine.
# YouTube video walk through: https://youtu.be/-zylGSCC6cU

import socket
import struct
from gateway_proto import crc32 # Import the same CRC logic

HOST = '127.0.0.1' # Localhost
PORT = 1500

# The header we discovered for 4-byte commands
EXPECTED_HEADER = b'\xca\xfe\x01\x04'
# The specific command that wins the prize
SUCCESS_COMMAND = b'KILL'

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    try:
        # Receive the packet from the client
        data = conn.recv(1024)
        if not data or len(data) < 12: # Basic length check
            print("[-] Received invalid or empty packet. Closing.")
            conn.sendall(b'FAIL')
            return

        print(f"[i] Received packet: {data.hex()}")

        # --- Packet Validation Logic ---
        header = data[:4]
        command = data[4:8]
        received_crc_bytes = data[8:12]

        # 1. Check if the header is correct
        if header != EXPECTED_HEADER:
            print(f"[-] FAIL: Invalid header. Expected {EXPECTED_HEADER.hex()}, got {header.hex()}")
            conn.sendall(b'FAIL')
            return

        # 2. Calculate the CRC of the received command
        calculated_crc = crc32(command)
        # Unpack the received CRC as a big-endian integer
        (received_crc, ) = struct.unpack('>I', received_crc_bytes)

        # 3. Compare the calculated CRC with the received one
        if calculated_crc != received_crc:
            print(f"[-] FAIL: CRC mismatch. Calculated {hex(calculated_crc)}, received {hex(received_crc)}")
            conn.sendall(b'FAIL')
            return

        # 4. Check if it's the winning command
        if command == SUCCESS_COMMAND:
            print("[!] SUCCESS! Correct KILL command received.")
            conn.sendall(b'local_flag{great_job_replicating_the_lab!}')
        else:
            print(f"[-] FAIL: Command '{command.decode()}' is not the kill switch.")
            conn.sendall(b'FAIL')

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
        print(f"[*] Control Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == '__main__':
    main()
