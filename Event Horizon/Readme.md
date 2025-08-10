below from Tryhackme room Event Horizon https://tryhackme.com/room/eventhorizonroom
YouTube video walk through: https://youtu.be/xUifweCxp8E

grep -Po '^i=.*|(?<=// Hello World! ).*' newtraffic.txt > extracted_data.txt


grep -zoP '{"status"\s*:\s*"2"\s*,\s*"output"\s*:\s*"\K[^"]*(?=")' cmd.txt | tr -d '\0'


python3 decrypt_covenant_traffic.py modulus -i extracted_data.txt  -k "l86Tf[redacted]+aYy3/s8=" -t base64

python3 extract_privatekey.py -i evidence-1724741326043/powershell.DMP  -m 406673971344452247271166682949[REDACTED]437631716767966582109 -o ./mykeys/

python3 decrypt_covenant_traffic.py key -i extracted_data.txt  -k "l86TfRDvv[REDUCTED]+aYy3/s8=" -t base64 -r mykeys/privkey1.pem -s 1
