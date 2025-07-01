Access Granted for TryHackMe Industrial Intrusion CTF https://tryhackme.com/room/industrial-intrusion


(gdb) break main
(gdb) run
(gdb) break *0x5555555550e0
(gdb) continue

(gdb)  x/s $rdi # First arg (real password)
(gdb)  x/s $rsi  # Second arg (your input)

x/s stands for "eXamine as String".
$rdi is the register holding the first argument in x86_64.
So, x/s $rdi prints the memory at $rdi as a null-terminated string.

x/s $rsi	Print string at $rsi (2nd arg)

info registers
