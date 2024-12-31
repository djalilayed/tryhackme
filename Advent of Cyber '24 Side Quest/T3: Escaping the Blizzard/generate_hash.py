# script usedon tryhackme room Advent of Cyber '24 Side Quest
# https://tryhackme.com/r/room/adventofcyber24sidequest
# T3: Escaping the Blizzard

import subprocess

password_list = "recommended-passwords.txt"
output_file = "hashed-passwords2.txt"
enc_binary = "./enc"

with open(password_list, "r") as f_in, open(output_file, "w") as f_out:
    for password in f_in:
        password = password.strip()  # Remove leading/trailing whitespace
        try:
            # Execute the enc binary with the password as input
            result = subprocess.run([enc_binary, password], capture_output=True, text=True)
            hashed_password = result.stdout.strip()  # Get the output and remove any extra whitespace
            f_out.write(hashed_password + "\n")  # Write the hashed password to the output file
        except FileNotFoundError:
            print(f"Error: Could not find the binary file '{enc_binary}'")
            break
        except Exception as e:
            print(f"Error hashing password '{password}': {e}")
