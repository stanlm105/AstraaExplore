"""
Messier catalog type normalization utilities.

Provides functions and mappings to clean up, canonicalize, and override object types and constellation names
for Messier catalog entries.
"""

import re

# Known special cases in the Messier list (Messier number → type label)
TYPE_OVERRIDES = {
    24: "Star Cloud",     # Sagittarius Star Cloud
    40: "Double Star",    # Winnecke 4
    73: "Asterism",       # Not a physical cluster
}

# Canonicalization map (lowercase → nice label)
CANON = {
    "open cluster": "Open Cluster",
    "open star cluster": "Open Cluster",
    "globular cluster": "Globular Cluster",
    "globular": "Globular Cluster",
    "planetary nebula": "Planetary Nebula",
    "supernova remnant": "Supernova Remnant",
    "emission nebula": "Emission Nebula",
    "reflection nebula": "Reflection Nebula",
    "dark nebula": "Dark Nebula",
    "diffuse nebula": "Emission Nebula",
    "hii region": "Emission Nebula",
    "nebula": "Nebula",
    "galaxy": "Galaxy",
    "spiral galaxy": "Galaxy",
    "elliptical galaxy": "Galaxy",
    "lenticular galaxy": "Galaxy",
    "double star": "Double Star",
    "asterism": "Asterism",
    "star cloud": "Star Cloud",
}

def _canon_type(t: str) -> str:
    """
    Canonicalize a Messier object type string to a standard label.

    Args:
        t (str): Raw type string.

    Returns:
        str: Canonicalized type label.
    """
    t = (t or "").strip()
    if not t:
        return ""
    key = t.lower()
    # Try exact match
    if key in CANON:
        return CANON[key]
    # Normalize whitespace and try again
    key = re.sub(r"\s+", " ", key)
    for k, v in CANON.items():
        if key == k:
            return v
    # Last resort: title case the original
    return t.title()

def normalize_catalog_types(catalog: list[dict]) -> list[dict]:
    """
    Return a new list of Messier objects with clean .type and .constellation fields,
    and Messier number-based type overrides applied.

    Args:
        catalog (list[dict]): List of Messier object dictionaries.

    Returns:
        list[dict]: List of normalized Messier object dictionaries.
    """
    out = []
    for o in catalog:
        o2 = dict(o)  # Copy to avoid mutating input
        # Ensure Messier number is int when possible
        try:
            if str(o2.get("catalog", "")).upper() == "M":
                o2["number"] = int(o2["number"])
        except Exception:
            pass

        # Apply type overrides by Messier number
        num = o2.get("number")
        if isinstance(num, int) and num in TYPE_OVERRIDES:
            o2["type"] = TYPE_OVERRIDES[num]
        else:
            o2["type"] = _canon_type(o2.get("type"))

        # Clean constellation name
        const = (o2.get("constellation") or "").strip()
        if const:
            o2["constellation"] = const.title()
        else:
            o2["constellation"] = "—"

        out.append(o2)
    return out