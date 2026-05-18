## Video walk through https://youtu.be/LXtyzyHZx6Y
## code used on the video

```
python3 -c "
import hmac, hashlib, json
from datetime import datetime, timezone
secret='shopflow-internal-2024-xK9#mP2@nL5'
ts=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
p={'amount':1337,'risk_score':1,'status':'CLEARED','timestamp':ts,'user_id':'3'}
meta=json.dumps(p,sort_keys=True,separators=(',',':'))
sig=hmac.new(secret.encode(),meta.encode(),hashlib.sha256).hexdigest()
payload=json.dumps({'user_id':'3','item_id':'33','amount':'1337','currency':'USD','x_risk_meta':meta,'x_risk_sig':sig})
print(payload)
" | curl -s -i -X POST http://10.112.138.51/checkout \
  -H 'Content-Type: application/json' \
  --data @-
```
