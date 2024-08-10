# original script: https://medium.com/maverislabs/decrypting-smb3-traffic-with-just-a-pcap-absolutely-maybe-712ed23ff6a2
# updated with assistance from ChatGPT

import hmac
import argparse
from binascii import unhexlify, hexlify

# Importing cryptography modules
try:
    from Cryptodome.Cipher import ARC4
    from Cryptodome.Hash import MD4
except ImportError:
    print("Warning: You don't have any crypto installed. You need pycryptodomex")
    print("See https://pypi.org/project/pycryptodomex/")

def generateEncryptedSessionKey(keyExchangeKey, exportedSessionKey):
    cipher = ARC4.new(keyExchangeKey)
    sessionKey = cipher.encrypt(exportedSessionKey)
    return sessionKey

# Argument parser setup
parser = argparse.ArgumentParser(description="Calculate the Random Session Key based on data from a PCAP (maybe).")
parser.add_argument("-u", "--user", required=True, help="User name")
parser.add_argument("-d", "--domain", required=True, help="Domain name")
parser.add_argument("-p", "--password", required=True, help="Password of User")
parser.add_argument("-n", "--ntproofstr", required=True, help="NTProofStr. This can be found in PCAP (provide Hex Stream)")
parser.add_argument("-k", "--key", required=True, help="Encrypted Session Key. This can be found in PCAP (provide Hex Stream)")
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")

args = parser.parse_args()

# Upper Case User and Domain
user = str(args.user).upper().encode('utf-16le')
domain = str(args.domain).upper().encode('utf-16le')

# Create 'NTLM' Hash of password using Cryptodome's MD4
md4 = MD4.new()
md4.update(args.password.encode('utf-16le'))
password = md4.digest()

# Calculate the ResponseNTKey
h = hmac.new(password, digestmod='md5')
h.update(user + domain)
respNTKey = h.digest()

# Use NTProofSTR and ResponseNTKey to calculate Key Exchange Key
NTproofStr = unhexlify(args.ntproofstr)
h = hmac.new(respNTKey, digestmod='md5')
h.update(NTproofStr)
KeyExchKey = h.digest()

# Calculate the Random Session Key by decrypting Encrypted Session Key with Key Exchange Key via RC4
RsessKey = generateEncryptedSessionKey(KeyExchKey, unhexlify(args.key))

if args.verbose:
    print("USER WORK: " + user.decode('utf-16le') + " " + domain.decode('utf-16le'))
    print("PASS HASH: " + hexlify(password).decode())
    print("RESP NT:   " + hexlify(respNTKey).decode())
    print("NT PROOF:  " + hexlify(NTproofStr).decode())
    print("KeyExKey:  " + hexlify(KeyExchKey).decode())

print("Random SK: " + hexlify(RsessKey).decode())
