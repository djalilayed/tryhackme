# scsript with help of chatgpt for tryhackme room https://tryhackme.com/r/room/pyrat
import socket

# Define target IP and port
target_ip = "10.10.176.98"  # Replace with your target IP
target_port = 8000         # Replace with your target port
# Path to the endpoint file (list of possible endpoints)
endpoint_file = "/usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt"  # Replace with the path to your endpoint wordlist file

# Set a timeout value in seconds
timeout_value = 5

# Create a socket connection to the target with a timeout
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout_value)  # Set timeout for the connection
    client_socket.connect((target_ip, target_port))
    return client_socket

# Send data and get the response from the server
def send_command(client_socket, command):
    try:
        client_socket.sendall((command + "\n").encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8").strip()  # Strip any extra spaces or newlines
        return response
    except socket.timeout:
        return "No response from server (timeout)"

# Function to read endpoints from a file
def read_endpoints_from_file(file_path):
    with open(file_path, 'r', encoding='latin-1', errors='ignore') as file:
        endpoints = [line.strip() for line in file.readlines()]
    return endpoints




# Read the possible endpoints from the file
endpoint_list = read_endpoints_from_file(endpoint_file)

# Try each endpoint
for endpoint in endpoint_list:
    client_socket = connect_to_server()  # Connect to the server

    # Send the endpoint as a command and receive the server's response
    response = send_command(client_socket, endpoint)

    # Check if the response is empty or contains 'not defined', 'invalid syntax', or '<string>'
    if not response or "not defined" in response or "invalid syntax" in response or "<string>" in response:
        client_socket.close()
        continue  # Skip and try the next endpoint

    # If the response is valid (not empty, not 'not defined', 'invalid syntax', or '<string>'), print it and exit
    print(f"Valid response for endpoint '{endpoint}': {response}")
    client_socket.close()
    break  # Exit after finding a valid endpoint
