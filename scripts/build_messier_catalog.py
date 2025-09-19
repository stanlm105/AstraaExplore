
#!/usr/bin/env python3
"""
Builds data/messier_catalog.json from a public Messier dataset.

Source used:
- Messier API by Osric Dienda (raw JSON): https://osricdienda.com/messier-api/messier.json
  Fields: messierNumber, name, NGC, type, constellation, rightAscension (hh:mm:ss.ss),
          declination (±dd:mm:ss.ss), magnitude, size (e.g., "178x63"), distance, viewingSeason, viewingDifficulty

This script converts to the schema:
{
  "catalog": "M",
  "number": 31,
  "ngc": "224",
  "name": "Andromeda Galaxy",
  "type": "Spiral Galaxy",
  "constellation": "Andromeda",
  "magnitude": 3.4,
  "size_arcmin": 190.0,  # if size is "178x63", this uses the major axis (178)
  "ra_deg": 10.6847,     # from "00:42:44.3"
  "dec_deg": 41.2688,    # from "+41:16:09"
  "notes": ""
}

Usage:
    python build_messier_catalog.py
"""
import json, re, urllib.request, math, sys, os
from typing import Optional

RAW_URL = "https://osricdienda.com/messier-api/messier.json"
OUT_DIR = os.path.join(os.path.dirname(__file__) or ".", "data")
OUT_PATH = os.path.join(OUT_DIR, "messier_catalog.json")

def hms_to_deg(hms: str) -> Optional[float]:
    if not hms:
        return None
    m = re.match(r"^\s*(\d+):(\d+):(\d+(?:\.\d+)?)\s*$", hms)
    if not m:
        # Some sources might use just hh:mm
        m = re.match(r"^\s*(\d+):(\d+(?:\.\d+)?)\s*$", hms)
        if not m:
            return None
        h = float(m.group(1))
        m_ = float(m.group(2))
        s = 0.0
    else:
        h = float(m.group(1))
        m_ = float(m.group(2))
        s = float(m.group(3))
    return (h + m_/60.0 + s/3600.0) * 15.0  # 24h = 360°

def dms_to_deg(dms: str) -> Optional[float]:
    if not dms:
        return None
    m = re.match(r"^\s*([+\-]?)(\d+):(\d+):(\d+(?:\.\d+)?)\s*$", dms)
    if not m:
        # Fallback for dd:mm
        m = re.match(r"^\s*([+\-]?)(\d+):(\d+(?:\.\d+)?)\s*$", dms)
        if not m:
            return None
        sign = -1.0 if m.group(1) == "-" else 1.0
        d = float(m.group(2))
        m_ = float(m.group(3))
        s = 0.0
    else:
        sign = -1.0 if m.group(1) == "-" else 1.0
        d = float(m.group(2))
        m_ = float(m.group(3))
        s = float(m.group(4))
    return sign * (d + m_/60.0 + s/3600.0)

def parse_size_arcmin(size):
    if not size:
        return None
    s = str(size).lower()
    # normalize unicode and units
    s = (s.replace("×", "x")
           .replace("arcminutes", "")
           .replace("arcminute", "")
           .replace("arcmin", "")
           .replace("’", "")    # curly minute
           .replace("′", "")    # prime minute
           .replace("'", "")    # plain apostrophe minute
           .replace("″", "")    # double-prime seconds if present
           .replace('"', ""))
    s = s.strip()
    # remove spaces so "178 x 63" -> "178x63"
    s = s.replace(" ", "")
    try:
        if "x" in s:
            a, _ = s.split("x", 1)
            return float(a)
        return float(s)
    except Exception:
        return None

def fetch_json(url: str):
    with urllib.request.urlopen(url) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} for {url}")
        data = resp.read()
    return json.loads(data.decode("utf-8"))

def transform(mapi: dict) -> list:
    out = []
    # mapi format is expected as {"M1": {...}, "M2": {...}, ...} or similar per the API
    for key, obj in mapi.items():
        # Handle keys like "M45"
        try:
            num = int(re.sub(r"[^0-9]","", key))
        except Exception:
            # Some APIs might use arrays; skip weird keys
            continue
        ra_deg = hms_to_deg(obj.get("rightAscension"))
        dec_deg = dms_to_deg(obj.get("declination"))
        size_arcmin = parse_size_arcmin(obj.get("size"))
        mag = obj.get("magnitude")
        try:
            mag = float(mag) if mag is not None else None
        except Exception:
            mag = None
        out.append({
            "catalog": "M",
            "number": num,
            "ngc": obj.get("NGC"),
            "name": obj.get("name") or f"Messier {num}",
            "type": obj.get("type"),
            "constellation": obj.get("constellation"),
            "magnitude": mag,
            "size_arcmin": size_arcmin,
            "ra_deg": ra_deg,
            "dec_deg": dec_deg,
            "notes": ""
        })
    # Sort by number
    out.sort(key=lambda x: x["number"])
    return out

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Fetching {RAW_URL} ...")
    mapi = fetch_json(RAW_URL)
    dataset = transform(mapi.get("data", mapi))
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(dataset)} objects to {OUT_PATH}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
