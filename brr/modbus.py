# code by Claudi AI
# code for TryHackMe room Brr https://tryhackme.com/room/brr
# Video Walk Through: https://youtu.be/DCNJqR8D9Do

from pymodbus.client import ModbusTcpClient

c = ModbusTcpClient('10.128.131.128', port=5020)
c.connect()

# Sweep holding registers
rr = c.read_holding_registers(address=0, count=20, slave=1)
print(rr.registers)

# Sweep coils
rc = c.read_coils(address=0, count=20, slave=1)
print(rc.bits)

c.close()
