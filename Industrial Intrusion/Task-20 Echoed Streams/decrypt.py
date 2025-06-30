# script by Gemini Pro
# script for tyrhackme room Task-20 Echoed Streams | TryHackMe: Industrial Intrusion CTF https://tryhackme.com/room/industrial-intrusion
# YouTube video walk through: https://youtu.be/qm_mpEskURo

import sys

def xor_bytes(a, b):
  """Performs a bitwise XOR on two byte strings."""
  return bytes([x ^ y for x, y in zip(a, b)])

def main():
  # Known plaintext of the first message
  known_plaintext = b"BEGIN TELEMETRY VIRELIA;ID=ZTRX0110393939DC;PUMP1=OFF;VALVE1=CLOSED;PUMP2=ON;VALVE2=CLOSED;END;"

  try:
    # Read the contents of the binary files
    with open("cipher1(1).bin", "rb") as f1, open("cipher2(1).bin", "rb") as f2:
      cipher1_data = f1.read()
      cipher2_data = f2.read()
  except FileNotFoundError as e:
    print(f"Error: {e}. Make sure the binary files are in the same directory.")
    sys.exit(1)

  # Extract the ciphertext from both files
  # Nonce: 0-15, Ciphertext: 16-111, Tag: 112-127
  ciphertext1 = cipher1_data[16:112]
  ciphertext2 = cipher2_data[16:112]

  # XOR the two ciphertexts
  xor_of_ciphertexts = xor_bytes(ciphertext1, ciphertext2)

  # Recover the plaintext of the second message
  recovered_plaintext2 = xor_bytes(known_plaintext, xor_of_ciphertexts)

  print("Successfully recovered the plaintext of cipher2.bin:")
  try:
    print(recovered_plaintext2.decode('utf-8'))
  except UnicodeDecodeError:
    print("Could not decode the recovered plaintext as UTF-8. Here is the raw byte string:")
    print(recovered_plaintext2)

if __name__ == "__main__":
  main()
