# script with assistance of ChatGPt and ClaudiAI
# for tryhackme root Extracted https://tryhackme.com/r/room/extractedroom
# dump_file_process.raw is extracted file from wireshark for keepass process dump
# dump_file_database.raw is extracted file from wireshark  for keepass database
# Youtube video walk through: https://youtu.be/q0XAEyirQzY

import base64

def xor_decrypt(data, key):
    # XOR each byte of the data with the given key
    return bytes([b ^ key for b in data])

def process_file(filename, xor_key):
    # Open the file containing the binary data (which is Base64-encoded)
    with open(filename, 'rb') as f:
        base64_encoded_data = f.read()
    
    # Base64 decode the data
    try:
        decoded_data = base64.b64decode(base64_encoded_data)
        print(f"{filename} was Base64 encoded. Decoded successfully.")
    except Exception as e:
        print(f"Error decoding Base64: {e}")
        return None
    
    # XOR decrypt the data
    decrypted_data = xor_decrypt(decoded_data, xor_key)
    
    return decrypted_data

# Process both files (using XOR key 0x41 for the process dump, 0x42 for the database dump)
files_to_process = [
    ('dump_file_process.raw', 0x41, 'decrypted_memory_dump.dmp'),  # Process dump
    ('dump_file_database.raw', 0x42, 'decrypted_database.kdbx')    # Database dump
]

# Iterate through the files and process each one
for filename, xor_key, output_file in files_to_process:
    data = process_file(filename, xor_key)
    if data:
        with open(output_file, 'wb') as f:
            f.write(data)
        print(f"Decrypted data from {filename} saved as '{output_file}'.")
