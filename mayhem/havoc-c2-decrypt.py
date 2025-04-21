# original script: https://github.com/Immersive-Labs-Sec/HavocC2-Forensics/blob/main/PacketCapture/havoc-pcap-parser.py
# sript updated by Grok
# script for tryhackme room Mayhem: https://tryhackme.com/room/mayhemroom
# TryHackMe Mayhem walk through: https://youtu.be/vKBVDcqlJ-c

# Copyright (C) 2024 Kev Breen, Immersive Labs
# https://github.com/Immersive-Labs-Sec/HavocC2-Forensics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import argparse
import struct
import binascii
from binascii import unhexlify
from uuid import uuid4

try:
    import pyshark
except ImportError:
    print("[-] Pyshark not installed, please install with 'pip install pyshark'")
    exit(0)

try:
    from Crypto.Cipher import AES
    from Crypto.Util import Counter
except ImportError:
    print("[-] PyCryptodome not installed, please install with 'pip install pycryptodome'")
    exit(0)

# Store AES keys and IVs for each session
sessions = {}

def tsharkbody_to_bytes(hex_string):
    """
    Converts a TShark hex formatted string to a byte string.
    
    :param hex_string: The hex string from TShark.
    :return: The byte string.
    """
    if not hex_string:
        return b''
    hex_string = hex_string.replace(':', '')
    try:
        return unhexlify(hex_string)
    except Exception as e:
        print(f"[!] Error converting hex string to bytes: {e}")
        return b''

def aes_decrypt_ctr(aes_key, aes_iv, encrypted_payload):
    """
    Decrypts an AES-encrypted payload in CTR mode.

    :param aes_key: The AES key as a byte string.
    :param aes_iv: The AES IV (Initialization Vector) for the counter, as a byte string.
    :param encrypted_payload: The encrypted payload as a byte string.
    :return: The decrypted plaintext as a byte string.
    """
    try:
        ctr = Counter.new(128, initial_value=int.from_bytes(aes_iv, byteorder='big'))
        cipher = AES.new(aes_key, AES.MODE_CTR, counter=ctr)
        return cipher.decrypt(encrypted_payload)
    except Exception as e:
        print(f"[!] Error decrypting payload: {e}")
        return b''

def check_magic_bytes(header_bytes, magic_bytes):
    """
    Checks if the header contains the specified magic bytes.

    :param header_bytes: The header bytes to check.
    :param magic_bytes: The expected magic bytes (e.g., 'deadbeef').
    :return: Tuple of (bool, agent_id_str).
    """
    if len(header_bytes) < 20:
        return False, None
    try:
        _, magic, agent_id, _, _ = struct.unpack('>I4s4sI4s', header_bytes)
        magic_str = binascii.hexlify(magic).decode('ascii')
        agent_id_str = binascii.hexlify(agent_id).decode('ascii')
        return magic_str == magic_bytes, agent_id_str
    except Exception as e:
        print(f"[!] Error checking magic bytes: {e}")
        return False, None

def parse_request(http_pair, magic_bytes, save_path):
    """
    Parses and decrypts Havoc C2 request and response packets.
    
    :param http_pair: Dictionary containing request and response data.
    :param magic_bytes: Expected magic bytes (e.g., 'deadbeef').
    :param save_path: Directory to save decrypted payloads.
    """
    request = http_pair['request']
    response = http_pair['response']
    unique_id = uuid4()

    print("[+] Parsing Request")

    # Parse request body
    request_body = tsharkbody_to_bytes(request.get('file_data', ''))
    if not request_body:
        print("[!] No request body found")
        return

    # Check for magic bytes
    has_magic, agent_id = check_magic_bytes(request_body[:20], magic_bytes)
    if not has_magic and agent_id not in sessions:
        print(f"[!] No valid magic bytes or known agent ID")
        return

    # Handle DEMON_INIT packet (first packet with key and IV)
    if has_magic and len(request_body) >= 68:
        magic = request_body[4:8]  # Magic bytes position
        magic_str = binascii.hexlify(magic).decode('ascii')
        if magic_str == magic_bytes and agent_id not in sessions:
            print("[+] Found Havoc C2 Initial Packet")
            print(f"  [-] Agent ID: {agent_id}")
            print(f"  [-] Magic Bytes: {magic_str}")
            print(f"  [-] C2 Address: {request.get('uri')}")

            aes_key = request_body[20:52]  # 32 bytes
            aes_iv = request_body[52:68]   # 16 bytes

            print(f"  [+] Found AES Key")
            print(f"    [-] Key: {binascii.hexlify(aes_key).decode('ascii')}")
            print(f"    [-] IV: {binascii.hexlify(aes_iv).decode('ascii')}")

            sessions[agent_id] = {
                "aes_key": aes_key,
                "aes_iv": aes_iv
            }
            return  # No payload to decrypt in DEMON_INIT

    # Process client-to-server request
    aes_keys = sessions.get(agent_id, None)
    if not aes_keys:
        print(f"[!] No AES keys for Agent ID {agent_id}")
        return

    request_payload = request_body[20:] if has_magic else request_body
    if request_payload:
        print("  [+] Decrypting Client-to-Server Payload")
        decrypted_request = aes_decrypt_ctr(aes_keys['aes_key'], aes_keys['aes_iv'], request_payload)
        if decrypted_request:
            try:
                print(f"  [-] Decrypted Request Payload: {decrypted_request.decode('utf-8', errors='ignore')}")
            except UnicodeDecodeError:
                print(f"  [-] Decrypted Request Payload (hex): {binascii.hexlify(decrypted_request).decode('ascii')}")

            if save_path:
                if not os.path.exists(save_path):
                    print(f"[!] Save path {save_path} does not exist, creating")
                    os.makedirs(save_path)
                save_file = f'{save_path}/{unique_id}-request-{agent_id}.bin'
                with open(save_file, 'wb') as output_file:
                    output_file.write(decrypted_request)
                print(f"  [-] Saved decrypted request to {save_file}")

    # Process server-to-client response (HTTP OK)
    response_body = tsharkbody_to_bytes(response.get('file_data', ''))
    if response_body and len(response_body) > 12:
        print("  [+] Processing Server-to-Client Response")
        response_payload = response_body[12:]  # Remove first 12 bytes
        if response_payload:
            print("  [+] Decrypting Server-to-Client Payload")
            decrypted_response = aes_decrypt_ctr(aes_keys['aes_key'], aes_keys['aes_iv'], response_payload)
            if decrypted_response:
                try:
                    print(f"  [-] Decrypted Response Payload: {decrypted_response.decode('utf-8', errors='ignore')}")
                except UnicodeDecodeError:
                    print(f"  [-] Decrypted Response Payload (hex): {binascii.hexlify(decrypted_response).decode('ascii')}")

                if save_path:
                    if not os.path.exists(save_path):
                        print(f"[!] Save path {save_path} does not exist, creating")
                        os.makedirs(save_path)
                    save_file = f'{save_path}/{unique_id}-response-{agent_id}.bin'
                    with open(save_file, 'wb') as output_file:
                        output_file.write(decrypted_response)
                    print(f"  [-] Saved decrypted response to {save_file}")
    else:
        print("[!] No valid response body found")

def read_pcap_and_get_http_pairs(pcap_file, magic_bytes, save_path):
    """
    Reads a PCAP file and extracts HTTP request-response pairs.
    
    :param pcap_file: Path to the PCAP file.
    :param magic_bytes: Expected magic bytes (e.g., 'deadbeef').
    :param save_path: Directory to save decrypted payloads.
    """
    try:
        capture = pyshark.FileCapture(pcap_file, display_filter='http')
    except Exception as e:
        print(f"[!] Error reading PCAP file: {e}")
        return

    http_pairs = {}
    current_stream = None
    request_data = None

    print("[+] Parsing Packets")

    for packet in capture:
        try:
            if 'HTTP' in packet:
                if current_stream != packet.tcp.stream:
                    current_stream = packet.tcp.stream
                    request_data = None

                if hasattr(packet.http, 'request_method'):
                    request_data = {
                        'method': packet.http.request_method,
                        'uri': packet.http.request_full_uri,
                        'headers': packet.http.get_field_value('request_line'),
                        'file_data': packet.http.file_data if hasattr(packet.http, 'file_data') else None
                    }
                elif hasattr(packet.http, 'response_code') and request_data:
                    response_data = {
                        'code': packet.http.response_code,
                        'phrase': packet.http.response_phrase,
                        'headers': packet.http.get_field_value('response_line'),
                        'file_data': packet.http.file_data if hasattr(packet.http, 'file_data') else None
                    }
                    pair_key = f"{current_stream}_{packet.http.request_in}"
                    http_pairs[pair_key] = {
                        'request': request_data,
                        'response': response_data
                    }
                    parse_request(http_pairs[pair_key], magic_bytes, save_path)
                    request_data = None
        except AttributeError:
            pass

    capture.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decrypt Havoc C2 Traffic from a PCAP')
    parser.add_argument('--pcap', help='Path to pcap file', required=True)
    parser.add_argument('--aes-key', help='AES key (hex)', required=False)
    parser.add_argument('--aes-iv', help='AES initialization vector (hex)', required=False)
    parser.add_argument('--agent-id', help='Agent ID (hex)', required=False)
    parser.add_argument('--save', help='Directory to save decrypted payloads', required=False)
    parser.add_argument('--magic', help='Magic bytes marker for Havoc C2 traffic', default='deadbeef', required=False)

    args = parser.parse_args()

    if any([args.aes_key, args.aes_iv, args.agent_id]) and not all([args.aes_key, args.aes_iv, args.agent_id]):
        parser.error("[!] If you provide one of 'aes-key', 'aes-iv', or 'agent-id', you must provide all three.")

    if args.agent_id and args.aes_key and args.aes_iv:
        try:
            sessions[args.agent_id] = {
                "aes_key": unhexlify(args.aes_key),
                "aes_iv": unhexlify(args.aes_iv)
            }
            print(f"[+] Added session keys for Agent ID {args.agent_id}")
        except Exception as e:
            print(f"[!] Error processing provided AES key/IV: {e}")
            exit(1)

    read_pcap_and_get_http_pairs(args.pcap, args.magic, args.save)
