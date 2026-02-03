


```
cl /W4 /D_AMD64_ /D_WIN64 /D_KERNEL_MODE rootkit.c /I"C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\km" /I"C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared" /link /driver /entry:DriverEntry /subsystem:native /out:rootkit.sys "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\km\x64\ntoskrnl.lib"
```
