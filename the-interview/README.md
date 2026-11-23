## TryHackMe room The Interview https://tryhackme.com/room/theinterview
## YouTube video walk through: https://youtu.be/Q2yB7liLIqQ


```
net user Administrator *
```
```
xfreerdp /v:10.112.188.17 /u:Administrator /p:'$Admin123Strator' /cert:ignore +clipboard /dynamic-resolution /drive:windows,/linux
```
### Key used for RC4 defender dump
```
1e87781b8dbaa844ce69702c0c78b786a3f623b738f5edf9af83530fb3fc54faa21eb9cf1331fd0f0da954f687cb9e18279697900e53fb317c9cbce48e23d05371ecc15951b8f3649d7ca33ed68dc9047e82c9baad9799d0d458cb847ca9ffbe3c8a775233557dde13a8b14087cc1bc8f10f6ecdd083a959cff84a9d1d50755e3e191818af23e2293558766d2c07e25712b2ca0b535ed8f6c56ce73d24bdd0291771861a54b4c285a9a3db7aca6d224aeacd621db9f2a22ed1e9e11d75bed7dc0ecb0a8e68a2ff1263408dc808dffd164b116774cd0b9b8d05411ed6262e429ba495676b8398db2f35d3c1b9ced52636f2765e1a95cb7ca4c3ddabddbff38253
```
```
Q="root/ProgramData/Microsoft/Windows Defender/Quarantine"
mkdir -p "$Q/Entries" "$Q/ResourceData"
```
```
cp '{80066DB4-0000-0000-214F-920CD72389D6}' "$Q/Entries/"
cp -r B3 "$Q/ResourceData/"
```
```
python3 defender-dump.py root/          # lists entries
python3 defender-dump.py root/ --dump   # writes quarantine.tar
tar -xvf quarantine.tar
sha256sum <extracted file>
```

