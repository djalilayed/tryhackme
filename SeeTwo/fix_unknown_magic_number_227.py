# script with assistance from ChatGPT
# fixing Error: Unknown magic number 227
# you can also run command: (echo -ne '\x55\x0d\x0d\x0a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'; cat your_file.pyc) > fixed_file.pyc
# script based on solution provided here: https://book.hacktricks.xyz/generic-methodologies-and-resources/basic-forensic-methodology/specific-software-file-type-tricks/.pyc#error-unknown-magic-number-227

# Define the correct header for Python 3.8
header = bytes.fromhex("550d0d0a000000000000000000000000")

# Read the existing .pyc file
with open("client.pyc", "rb") as f:
    original_data = f.read()

# Write the new file with the correct header
with open("fixed_file.pyc", "wb") as f:
    f.write(header + original_data)
