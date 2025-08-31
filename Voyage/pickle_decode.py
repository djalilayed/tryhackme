# for tryhackme room Voyage https://tryhackme.com/room/voyage
# run below on terminal

python3 - <<'PY'
import binascii, pickle
hexval = "80049526000000000000007d94288c0475736572948c0561646d696e948c07726576656e7565948c05383530303094752e"
data = binascii.unhexlify(hexval)
print("Decoded dict:", pickle.loads(data))
PY
