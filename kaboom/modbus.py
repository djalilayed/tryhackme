# script by Claudi
# script for TryHackMe room Kaboom https://tryhackme.com/room/kaboom
# YouTube video walk through: https://youtu.be/C51Td99E8uk

from pymodbus.client import ModbusTcpClient

c = ModbusTcpClient('10.129.164.205', port=502)
c.connect()

# Sweep holding registers
rr = c.read_holding_registers(address=0, count=20, slave=1)
print(rr.registers)

# Sweep coils
rc = c.read_coils(address=0, count=20, slave=1)
print(rc.bits)

c.close()
