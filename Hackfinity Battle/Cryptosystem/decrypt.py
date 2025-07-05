# script by Gemini for tryhackme room https://tryhackme.com/room/hfb1cryptosystem
# youtube walk through: https://youtu.be/ItK9XFx5x7k

from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
import math

def solve():
    """
    Solves the RSA challenge by factoring n, which was generated with two
    primes p and q that are very close to each other.
    """
    # The public values from the 'order.py' file
    n = 15956250162063169819282947443743274370048643274416742655348817823973383829364700573954709256391245826513107784713930378963551647706777479778285473302665664446406061485616884195924631582130633137574953293367927991283669562895956699807156958071540818023122362163066253240925121801013767660074748021238790391454429710804497432783852601549399523002968004989537717283440868312648042676103745061431799927120153523260328285953425136675794192604406865878795209326998767174918642599709728617452705492122243853548109914399185369813289827342294084203933615645390728890698153490318636544474714700796569746488209438597446475170891
    c = 3591116664311986976882299385598135447435246460706500887241769555088416359682787844532414943573794993699976035504884662834956846849863199643104254423886040489307177240200877443325036469020737734735252009890203860703565467027494906178455257487560902599823364571072627673274663460167258994444999732164163413069705603918912918029341906731249618390560631294516460072060282096338188363218018310558256333502075481132593474784272529318141983016684762611853350058135420177436511646593703541994904632405891675848987355444490338162636360806437862679321612136147437578799696630631933277767263530526354532898655937702383789647510
    e = 0x10001

    # 1. Calculate the integer square root of n
    s = math.isqrt(n)
    print(f"[*] Approximate square root of n: {s}")

    # 2. Search for p. Since p is a large prime, it must be odd.
    # We start our search from the first odd number less than or equal to s.
    if s % 2 == 0:
        s -= 1

    print("[*] Starting search for p...")
    while True:
        # 3. Check if s is a factor of n
        if n % s == 0:
            p = s
            q = n // p
            print(f"[+] Found p: {p}")
            print(f"[+] Found q: {q}")
            
            # Verify that p * q is indeed n
            if p * q == n:
                print("[+] Factorization successful!")
                break
            else:
                 print("[-] Factorization failed, continuing search...")
        
        # Move to the next odd number
        s -= 2

    # 4. Decrypt the message
    # Calculate phi(n) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)
    
    # Calculate the private exponent d, which is the modular inverse of e mod phi
    # d = e^(-1) mod phi
    d = pow(e, -1, phi)
    print(f"[+] Calculated private key d (first 20 digits): {str(d)[:20]}...")

    # Decrypt the ciphertext c: m = c^d mod n
    m = pow(c, d, n)

    # 5. Convert the decrypted number back to bytes to get the flag
    flag = long_to_bytes(m)
    print(f"\n[!] The secret key is: {flag.decode()}")


    key_components = (n, e, d, p, q)
    rsa_key = RSA.construct(key_components)

    # 2. Export the key in PEM format
    # The export_key() method handles the complex ASN.1 and Base64 encoding.
    private_key_pem = rsa_key.export_key(format='PEM')

    # 3. Save the PEM key to a file
    with open('private.pem', 'wb') as f:
        f.write(private_key_pem)

    print("[+] Private key successfully saved to private.pem")
    print("\n--- Key Content ---")
    print(private_key_pem.decode('utf-8'))

solve()
