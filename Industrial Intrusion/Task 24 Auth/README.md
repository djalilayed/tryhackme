TryHackMe room Auth  part of Industrial Intrusion CTF https://tryhackme.com/room/industrial-intrusion

ZeroTrace intercepts a stripped-down authentication module running on a remote industrial gateway. Assembly scrolls across glowing monitors as she unpacks the logic behind the plant’s digital checkpoint

The input must be exactly 8 characters long (sVar4 == 8)

The input is read into local_158.

Transformation:

    The input (local_158[0]) is passed to a function called transform along with the length (8).

    The transformed input is stored in local_168.
    
Comparison:

    The transformed input (local_168) is compared to the hardcoded value (local_160 = 0xefcdab8967452301) using memcmp.

    If they match, the flag is printed. flag.txt
    
transform Function

it takes each byte of your 8-byte input and performs a bitwise XOR operation with the hexadecimal value 0x55

If (INPUT_BYTE ^ 0x55) = TARGET_BYTE
Then (TARGET_BYTE ^ 0x55) = INPUT_BYTE

To find the correct unlock code, we simply need to take the target bytes from the main function and XOR each one with 0x55.

We apply the ^ 0x55 operation to each of these bytes to find the required input bytes.

local_160 = 0xefcdab8967452301

01 23 45 67 89 ab cd ef

0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef


0x01 ^ 0x55 = 0x54
0x23 ^ 0x55 = 0x76
0x45 ^ 0x55 = 0x10
0x67 ^ 0x55 = 0x32
0x89 ^ 0x55 = 0xdc
0xab ^ 0x55 = 0xfe
0xcd ^ 0x55 = 0x98
0xef ^ 0x55 = 0xba


python3 -c 'import sys; sys.stdout.buffer.write(b"\x54\x76\x10\x32\xdc\xfe\x98\xba\n")' | ./auth
 
echo -ne "\x54\x76\x10\x32\xdc\xfe\x98\xba\n" | ./auth

=======

python3 -c 'import sys; sys.stdout.buffer.write(b"\x54\x76\x10\x32\xdc\xfe\x98\xba\n")' | nc 10.10.110.85 9005
 
echo -ne "\x54\x76\x10\x32\xdc\xfe\x98\xba\n" | nc 10.10.110.85 9005
