```
nc 10.130.154.134 29536
```
```
< open can0 >
< rawmode >
```
```
< frame 23F 1789296988.818642 93ae0507846c9191 >

93 ae 05 07 84 6c 91 91

< frame CAN_ID TIMESTAMP PAYLOAD >
```
```
nc 10.130.154.134 29536 > baseline.raw

baseline.raw
repeated-lock.raw
repeated-horn.raw
repeated-arm.raw
repeated-disarm.raw
repeated-concurrently.raw
```
```

curl -sS -X POST http://10.130.154.134:8080/press \
    -H 'Content-Type: application/json' \
    -d '{"button":"LOCK"}' &

curl -sS -X POST http://10.130.154.134:8080/press \
    -H 'Content-Type: application/json' \
    -d '{"button":"HORN"}' &

curl -sS -X POST http://10.130.154.134:8080/press \
    -H 'Content-Type: application/json' \
    -d '{"button":"IMMOB_ARM"}' &

curl -sS -X POST http://10.130.154.134:8080/press \
    -H 'Content-Type: application/json' \
    -d '{"button":"IMMOB_DISARM"}' &

wait
```

## Count the frames belonging to each ID:
```
for file in baseline repeated-concurrently repeated-lock repeated-horn repeated-arm repeated-disarm; do
   echo "$file"

   tr '<' '\n' < "$file.raw" |
   awk 'toupper($1)=="FRAME" {
       count[toupper($2)]++
   }
   END {
       for (id in count)
           print count[id], id
   }' |
    sort -n
done
```
## look like constant 504 id related to buttons clicking


## each time you restart the machine you get different results!!!

## Split the payload into individual bytes:
```
for file in baseline repeated-concurrently repeated-lock repeated-horn repeated-arm repeated-disarm; do
   echo "$file"

   tr '<' '\n' < "$file.raw" |
   awk 'toupper($1)=="FRAME" &&
        toupper($2)=="504" {
        print toupper($4)
   }' |
   sed -E 's/(..)/\1 /g'
done
```
```
b0  B1
b1  checksum
b2  8A
b3  D7
b4  button 
b5  challenge related
b6 counter, id + 1 etc
b7 challenge related
```
```    
B1 EB 8A D7 27 84 B9 BD disarm
B1 F0 8A D7 3F 84 BA BD arm
B1 43 8A D7 8D 84 BB BD lock
B1 15 8A D7 DC 84 BC BD Horn
```

## confirm challenge:
```
for id in 318 1ED; do
  echo "== $id =="
  tr '<' '\n' < repeated-lock.raw |
  awk -v ID=$id 'toupper($1)=="FRAME" && toupper($2)==ID {print toupper($4)}' |
  sed -E 's/(..)/\1 /g' | head
done
```

## XOR checksum
```
byte_k ⊕ (XOR of the other 7) if that's the same on every frame
```
## additive checksum
```
byte_k - (sum of the other 7) mod 256 if that's the same

0x69+0xF5+0x01+0x09+0x53+0x76+0x4A = 0x27B

0x27B & 0xFF = 0x7B

K = (b4 − Σrest) & 0xFF
  = (0x20 − 0x7B) & 0xFF
  = (−0x5B) & 0xFF
  = 0x100 − 0x5B
  = 0xA5
```
In modular arithmetic, -x and (256 - x) are the same value mod 256

00 01 02 03 aa 

69 4F 10 09 1E 33 76 C0

< send 57C 8  69 4F 10 09 DF 33 76 FF >
