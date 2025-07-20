List of command used on TryHackMe Directory YouTube Video walk through: https://youtu.be/sET2aPr2CIg
TryHackMe Directory room: https://tryhackme.com/room/directorydfirroom

tcp.flags.syn==1 and tcp.flags.ack==0

ip.src == 10.0.2.74 and tcp.flags.syn==1 and tcp.flags.ack==0


ip.src == 10.0.2.75 and tcp.flags.syn==1 and tcp.flags.ack==1 and ip.dst == 10.0.2.74

tcp.flags.syn==1 and tcp.flags.ack==0 and ip.src==10.0.2.75 and ip.dst==10.0.2.74


scan ports:

tshark -r capture.pcap -Y "tcp.flags.syn == 1 and tcp.flags.ack == 0 and ip.src == 10.0.2.74" -T fields -e tcp.dstport | sort
-n | uniq

open ports:

tshark -r capture.pcap -Y "ip.src == 10.0.2.75 && tcp.flags.syn == 1 && tcp.flags.ack == 1 && ip.dst == 10.0.2.74" -T fields -
e tcp.srcport | sort -n | uniq

===========


Kerberos AS‑REP Roast attack

AS‑REQ without pre‑auth
The attacker sends a Kerberos Authentication Service Request (AS‑REQ) for each guessed username without any pre‑authentication
 data.

KDC’s two possible replies

    Error 25 (KDC_ERR_PREAUTH_REQUIRED):
    The account exists and does require pre‑authentication → the KDC tells you “you need to pre-auth”

    Error 6 (KDC_ERR_C_PRINCIPAL_UNKNOWN):
    The account does not exist

2. Grabbing the AS‑REP Roast (no pre‑auth account)

Some accounts are misconfigured to not require pre‑authentication. When you ask for one of those:

    The KDC happily responds with a full AS‑REP (msg_type 11) including the user’s encrypted key material.
    That blob is effectively an encrypted version of the user’s long‑term key, derived directly from their password.


tshark -r capture.pcap -Y "kerberos.msg_type=10" -T fields -e kerberos.CNameString | sort -u | uniq

http.request.method == "POST" && http.request.uri contains "wsman"
kerberos.msg_type == 11

tshark -r capture.pcap -Y "kerberos.msg_type=10" -T fields -e kerberos.CNameString | sort -u | uniq

pip install pycryptodom
grep -oP '<rsp:Arguments>\K[^<]*' decrypted_output.txt | base64 -d


 grep -zoP '<S N="V">\K[\s\S]*?(?=<\/S>)' base64_decrypted.txt
grep -oP '<rsp:Arguments>\K[^<]*' decrypted_output.txt | base64 -d

echo '$krb5asrep$23$larry.doe@DIRECTORY.THM:f8716efbaa9[READACTED]a469f' > hash.txt


First 32 bytes (64 hex chars) after the colon:
    f8716efbaa984508ddde606756441480
    (This is the checksum/header)

Remaining ciphertext after the $:
    805ab8be8cfb018a282718f7c040cd43...ba469f
    (Full encrypted timestamp and data)

 hashcat -m 18200 hash.txt rockyou.txt



pip install pycryptodome pyshark cryptography

 python3 c.py -p 'userpassword' capture.pcap > decrypt_directory.txt

grep -oP 'AAAAAA[A-Za-z0-9+/]*={0,2}' decrypt_diretory.txt | base64 -d > attacker_commands.txt

grep -zoP '<S N="V">\K[\s\S]*?(?=<\/S>)' attacker_commands.txt

