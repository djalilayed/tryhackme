
##tryhackme room Kernel Blackout https://tryhackme.com/room/kernelblackout
##YouTube video walk through: https://youtu.be/yfMCQTyOmJ4

```
cl /W4 /D_AMD64_ /D_WIN64 /D_KERNEL_MODE rootkit.c /I"C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\km" /I"C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared" /link /driver /entry:DriverEntry /subsystem:native /out:rootkit.sys "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\km\x64\ntoskrnl.lib"
```



we just want to prove we can locate it in memory.

This is where the Offsets (0x2e8 and 0x450) come in. Windows uses a "Doubly Linked List" to track processes.

    0x450 (ImageFileName): The process name (e.g., "chrome.exe").

    0x2e8 (ActiveProcessLinks): The "handshake" that connects this process to the next one.
    
    
    
We use a for loop as a safety mechanism. If we used while(true) and got stuck, the whole OS would freeze.

We use the Flink (Forward Link) to jump to the next item in the chain.

The Ghost (Unlinking)

This is the final step you used. We found the process, now we "Unlink" it.

In a linked list, Process A points to B, and B points to C.

    Normal: A <-> B <-> C

    Hidden: A <-> C

We are not deleting "B" (Process B is still running on the CPU). We are just telling A to point directly to C, effectively removing B from the map.

self-pointing cleanup (Flink = CurrentListEntry / Blink = CurrentListEntry), which is actually one of the more interesting lines in the code.  "We point the hidden process's links back to itself so it doesn't hold dangling pointers — this prevents a crash if anything ever touches it."
