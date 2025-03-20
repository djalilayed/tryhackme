# script for TryHackMe Hackfinity Battle Old Authentication https://tryhackme.com/room/HackfinityBattle
# script generate by Claudi AI, updated also by Grok AI
# script generate correct key send it to binary, then send the correct username and finally get the flag.

#!/usr/bin/env python3
import socket
import time
import sys

def create_valid_key():
    # Initialize a key to meet all constraints
    key = bytearray([65] * 16)  # Start with 'A's
    
    # Constraint: 3rd character must be 'Q' after XOR with 0x52
    key[2] = ord('Q') ^ 0x52  # This might be non-printable
    
    # Constraint: Character at position 13 must be '4' after XOR with 0x52
    key[13] = ord('4') ^ 0x52
    
    # Check 1: Sum of first 4 chars after XOR must be divisible by 3
    xored = [(b ^ 0x52) for b in key[0:4]]
    total = sum(xored)
    remainder = total % 3
    if remainder != 0:
        # Adjust first char to make sum divisible by 3
        key[0] = ((xored[0] + (3 - remainder)) ^ 0x52)
    
    # Check 2: Sum of next 5 chars after XOR must be divisible by 8
    xored = [(b ^ 0x52) for b in key[4:9]]
    total = sum(xored)
    remainder = total % 8
    if remainder != 0:
        # Adjust first char in this range to make sum divisible by 8
        key[4] = ((xored[0] + (8 - remainder)) ^ 0x52)
    
    # Check 3: Sum of next 4 chars after XOR must be divisible by 5
    xored = [(b ^ 0x52) for b in key[9:13]]
    total = sum(xored)
    remainder = total % 5
    if remainder != 0:
        # Adjust first char in this range to make sum divisible by 5
        key[9] = ((xored[0] + (5 - remainder)) ^ 0x52)
    
    # Check 4: Sum of last 4 chars after XOR must be divisible by 3
    xored = [(b ^ 0x52) for b in key[12:16]]
    total = sum(xored)
    remainder = total % 3
    if remainder != 0:
        # Adjust last char to make sum divisible by 3
        key[15] = ((xored[3] + (3 - remainder)) ^ 0x52)
    
    return bytes(key)

def create_valid_username():
    target = "elb4rt0pwn"
    # Each character minus 2
    return ''.join(chr(ord(c) - 2) for c in target)

def solve_remote_binary(host, port):
    # Create valid credentials
    key = create_valid_key()
    username = create_valid_username()
    
    # Print for debugging
    print(f"Using key (hex): {key.hex()}")
    print(f"Key length: {len(key)}")
    print(f"Using username: {username}")
    
    # Verify constraints (for debugging)
    xored_key = [b ^ 0x52 for b in key]
    print("\nVerification:")
    print(f"3rd char after XOR: {xored_key[2]} (should be {ord('Q')})")
    print(f"14th char after XOR: {xored_key[13]} (should be {ord('4')})")
    print(f"Sum of first 4 chars % 3: {sum(xored_key[0:4]) % 3} (should be 0)")
    print(f"Sum of next 5 chars % 8: {sum(xored_key[4:9]) % 8} (should be 0)")
    print(f"Sum of next 4 chars % 5: {sum(xored_key[9:13]) % 5} (should be 0)")
    print(f"Sum of last 4 chars % 3: {sum(xored_key[12:16]) % 3} (should be 0)")
    
    # Connect to the remote server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        print(f"\nConnected to {host}:{port}")
        
        # Wait for the key prompt
        data = b""
        while b"Enter the key:" not in data:
            chunk = s.recv(1024)
            if not chunk:
                raise ConnectionError("Connection closed by server before key prompt")
            data += chunk
            print(f"Received: {chunk.decode(errors='replace')}")
        
        # Send the key
        print(f"Sending key...")
        s.sendall(key + b'\n')
        
        # Wait for the username prompt
        data = b""
        while b"Enter the username:" not in data:
            chunk = s.recv(1024)
            if not chunk:
                raise ConnectionError("Connection closed by server before username prompt")
            data += chunk
            print(f"Received: {chunk.decode(errors='replace')}")
        
        # Send the username
        print(f"Sending username...")
        s.sendall(username.encode() + b'\n')
        
        # Receive the flag
        flag_data = b""
        try:
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                flag_data += chunk
                # Print received data for debugging
                print(f"Received: {chunk.decode(errors='replace')}")
                
                # Add a small delay to avoid busy waiting
                time.sleep(0.1)
        except socket.timeout:
            pass  # Expected when we're done receiving
        
        # Print the complete response
        print("\nFull response:")
        print(flag_data.decode(errors='replace'))
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        print(f"Example: {sys.argv[0]} 10.10.33.22 9002")
        sys.exit(1)
    
    # Get host and port from arguments
    host = sys.argv[1]
    port = sys.argv[2]
    
    # Run the solver with provided host and port
    solve_remote_binary(host, port)
