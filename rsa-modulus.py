# script with help from Chatgpt to generate modules from RSA pubclic key
import base64
import struct

def decode_pub_key(file_path):
    with open(file_path, 'r') as f:
        key_data = f.read().strip().split(None, 2)[1]
    key_bytes = base64.b64decode(key_data)

    parts = []
    while key_bytes:
        # Read the length of the data
        dlen = struct.unpack('>I', key_bytes[:4])[0]

        # Extract the data chunk
        data, key_bytes = key_bytes[4:4+dlen], key_bytes[4+dlen:]
        parts.append(data)

    # The modulus is in the third part for RSA (ssh-rsa)
    # Convert from bytes to a number
    modulus = int.from_bytes(parts[2], byteorder='big')
    return modulus

# Replace 'path/to/your/id_rsa.pub' with the actual path to your id_rsa.pub file
modulus = decode_pub_key('id_rsa.pub')
print(f"Modulus: {modulus}")
