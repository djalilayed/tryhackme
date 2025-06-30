tryhackme room Industrial Intrusion Task-19 No Salt, No Shame
youtube video walk through: https://youtu.be/5-U9fT4wm-s

o “secure” the maintenance logs, Virelia’s gateway vendor encrypted every critical entry with AES-CBC—using the plant’s code name as the passphrase and a fixed, all-zero IV. Of course, without any salt or integrity checks, it’s only obscurity, not true security. Somewhere in those encrypted records lies the actual shutdown command.

Passphrase: VIRELIA-WATER-FAC

Download the encrypted log file attached to this task and get the flag!

all-zero IV". For AES, the IV size is the same as the block size, which is 128 bits (16 bytes). So your IV will be 16 bytes of 0x00. (AES operates on 128-bit blocks regardless of the key size.)


pip3 install pycryptodome

echo -n "VIRELIA-WATER-FAC" | sha256sum


9cfa5c575052bee2ac406f82dbbcae08a18edf6bba396b9be46231347cf8f959
00000000000000000000000000000000

For proper AES-256-CBC, you should have:

   Key: 32 bytes (256 bits)
   IV: 16 bytes (128 bits)

youtube video walk through: https://youtu.be/5-U9fT4wm-s
