# script by Claudi
# script for TryHackMe room Injectus IX | Model Extraction | Model Leakage Event | Task 2 https://tryhackme.com/room/injectusix
# YouTube full video: https://youtu.be/7BgeZddzZ_w

#!/usr/bin/env python3
"""
cargomind_extract.py  —  decision-surface mapper for the CargoMind /predict API
(TryHaulMe / Injectus-style model-extraction exercise, authorised target only).

What it does:
  1. Field discovery   – dumps the FULL raw JSON keys so any hidden field
                         (confidence, score, debug, flag, ...) the frontend
                         ignores gets caught.
  2. Single-feature    – holds the other 5 inputs at a baseline and sweeps each
     sensitivity         feature 0->1, so you see which columns actually move
                         the classification / risk_band. Run from two baselines
                         (0.0 and 0.5) to expose feature interaction.
  3. Threshold finder  – binary-searches every band transition it sees in the
                         coarse sweep, to pin the exact boundary value.
  4. Band hunt         – random search to surface inputs that trigger each of
                         the four bands (low / medium / elevated / critical),
                         which the original write-up never did.

Rate limit: the API allows ~29 requests then returns 429; POST /reset clears
the counter. The script auto-resets before it gets close and recovers from a
429 automatically, so you can let it run.

Usage:
    python3 cargomind_extract.py http://10.129.152.245:8000
    python3 cargomind_extract.py http://10.129.152.245:8000 --step 0.05
Only stdlib — no pip install needed.
"""

import json
import sys
import argparse
import urllib.request
import urllib.error

FEATURES = ["CM", "SE", "RR", "OS", "CT", "MS"]
RESET_EVERY = 25          # stay safely under the ~29 limit
SEEN_KEYS = set()         # every JSON key ever returned by /predict


class Client:
    def __init__(self, base):
        self.base = base.rstrip("/")
        self.count = 0

    def _post(self, path, obj):
        url = f"{self.base}{path}"
        data = json.dumps(obj).encode()
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            try:
                body = json.loads(body)
            except Exception:
                pass
            return e.code, body
        except Exception as e:
            return None, {"_transport_error": str(e)}

    def reset(self):
        self._post("/reset", {})
        self.count = 0

    def predict(self, vec):
        if self.count >= RESET_EVERY:
            self.reset()
        status, data = self._post("/predict", {"features": vec})
        self.count += 1
        if status == 429:                       # hit the limit anyway -> reset & retry
            self.reset()
            status, data = self._post("/predict", {"features": vec})
            self.count += 1
        if isinstance(data, dict):
            SEEN_KEYS.update(data.keys())
        return data

    def band(self, vec):
        """Return (classification, risk_band) or None on error."""
        d = self.predict(vec)
        if isinstance(d, dict) and "classification" in d:
            return (d.get("classification"), d.get("risk_band"))
        return None


def field_discovery(c):
    print("\n=== 1. FIELD DISCOVERY (full raw responses) ===")
    probes = [
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    ]
    for v in probes:
        d = c.predict(v)
        print(f"  {v} -> {json.dumps(d)}")
    print(f"  >> keys ever seen from /predict: {sorted(SEEN_KEYS)}")
    extra = SEEN_KEYS - {"classification", "risk_band", "error"}
    if extra:
        print(f"  !! HIDDEN FIELD(S) the frontend ignores: {sorted(extra)}  <-- investigate")
    else:
        print("  (only classification / risk_band returned — no hidden channel)")


def single_feature_sweep(c, step, baseline):
    print(f"\n=== 2. SINGLE-FEATURE SWEEP (others held at {baseline}) ===")
    transitions = []   # (feature_index, low_value, high_value) around a band change
    n = int(round(1.0 / step))
    for i, name in enumerate(FEATURES):
        prev = None
        row = []
        for k in range(n + 1):
            v = round(k * step, 4)
            vec = [baseline] * 6
            vec[i] = v
            b = c.band(vec)
            row.append((v, b))
            if prev is not None and b != prev[1]:
                transitions.append((i, prev[0], v))
            prev = (v, b)
        changed = any(r[1] != row[0][1] for r in row)
        flag = "  <-- moves output" if changed else ""
        print(f"  {name}: {row[0][1]} ... {row[-1][1]}{flag}")
    return transitions


def binary_threshold(c, i, lo, hi, baseline, iters=18):
    """Find the precise transition point for feature i between lo and hi."""
    def band_at(v):
        vec = [baseline] * 6
        vec[i] = v
        return c.band(vec)

    b_lo = band_at(lo)
    for _ in range(iters):
        mid = (lo + hi) / 2
        if band_at(mid) == b_lo:
            lo = mid
        else:
            hi = mid
    return round(lo, 5), round(hi, 5), b_lo, band_at(hi)


def threshold_finder(c, transitions, baseline):
    print("\n=== 3. PRECISE THRESHOLDS (binary search) ===")
    if not transitions:
        print("  (no transitions seen in the coarse sweep at this baseline)")
        return
    seen = set()
    for i, lo, hi in transitions:
        key = (i, round(lo, 2), round(hi, 2))
        if key in seen:
            continue
        seen.add(key)
        a, b, ba, bb = binary_threshold(c, i, lo, hi, baseline)
        print(f"  {FEATURES[i]}: boundary in ({a}, {b})   {ba} -> {bb}")


def band_hunt(c, trials=120):
    print(f"\n=== 4. BAND HUNT ({trials} random vectors) ===")
    import random
    found = {}
    for _ in range(trials):
        vec = [round(random.random(), 3) for _ in range(6)]
        b = c.band(vec)
        if b and b not in found:
            found[b] = vec
    for (cls, band), vec in sorted(found.items(), key=lambda x: str(x[0])):
        print(f"  {band:>9} / {cls:<14} example input: {vec}")
    bands = {b[1] for b in found}
    print(f"  >> distinct risk_bands reached: {sorted(bands)}")
    missing = {"low", "medium", "elevated", "critical"} - bands
    if missing:
        print(f"  (not reached randomly: {sorted(missing)} — may need targeted inputs)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", help="target base URL, e.g. http://10.129.152.245:8000")
    ap.add_argument("--step", type=float, default=0.1, help="coarse sweep step (default 0.1)")
    args = ap.parse_args()

    c = Client(args.base)
    c.reset()

    field_discovery(c)
    for baseline in (0.0, 0.5):
        tr = single_feature_sweep(c, args.step, baseline)
        threshold_finder(c, tr, baseline)
    band_hunt(c)

    print("\nDone. If a hidden field showed up in section 1, that's your real leak channel.")


if __name__ == "__main__":
    main()
