tryhacme room Task 21 CRC Me If You Can Industrial Intrusion https://tryhackme.com/room/industrial-intrusion

YouTube video walk through: https://youtu.be/-zylGSCC6cU

List of commands used on the video:


root@ip-10-10-104-234:~# python3
Python 3.8.10 (default, Sep 11 2024, 16:02:53) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from gateway_proto import crc32
>>> crc32(b"OPEN")
2464509456
>>> 

=========
python3 crc_oracle.py
[*] CRC-Oracle Server listening on 127.0.0.1:1501

 echo -n "TEST" | nc 127.0.0.1 1501 | xxd
 
==========

 python3 control_server.py
[*] Control Server listening on 127.0.0.1:1500


========

hexdump -C open_frame.bin
00000000  ca fe 01 04 4f 50 45 4e  92 e5 6e 10              |....OPEN..n.|
0000000c

AA BB is a fixed header (two‐byte magic),

00 04 is the big-endian payload length,

4F 50 45 4E is ASCII “OPEN”,

12 34 56 78 is a 4-byte CRC-32 over the payload.

cat open_frame.bin | nc 10.10.158.144 1501 | hexdump -C 


>>> from gateway_proto import crc32
>>> crc32("OPEN")
>>> crc32(b"OPEN")
2464509456
>>> crc = crc32(b"OPEN")
>>> hex(crc)
'0x92e56e10'
>>>


manually:

printf '\xca\xfe\x01\x04' > header.bin
cat header.bin kill_switch.bin > packet_data.bin

hexedit packet_data.bin

cat packet_data.bin | nc 127.0.0.1 1500 | xxd

cat kill_switch.bin | python3 frame.py | nc 127.0.0.1 1500

cat kill_switch.bin | python3 frame.py | nc 127.0.0.1 1500 | xxd
