## TryHackMe room Pressed https://tryhackme.com/room/pressedroom

### TryHackMe Pressed YouTube Video Walk Through: 

[TryHackMe Pressed Full Walkthrough 2025](#)

**Below commands used on TryHackMe room Pressed YouTube video walk through: **

```
cat sheet.txt | base64 -d > sheet.ods
```
```
unzip sheet.ods
```

convert text to hex:

```
echo -n 'rhI1Yaz****Ivl8ps6MJj' | xxd -p
```

Using openssl to decrypt aes

```
openssl enc -aes-256-cbc -d -K 726849315961******149766c387073364d4a6a -iv 70457738****34736a -in cmd.bin -out cmd.txt
```

