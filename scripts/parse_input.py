#!/usr/bin/env python3
"""
parse_input.py - Normalize a topic list (Excel/CSV) into the skill's config rows.

Usage:
    python parse_input.py <path-to-.xlsx-or-.csv>

Prints a JSON array of normalized topic configs to stdout. Missing fields are
filled with skill defaults. Column headers are matched loosely and bilingually
(TR/EN), so a sheet with "Konu" or "Topic" both work.

Defaults: language=tr, location_code=2792, video_count=5, mode=brief,
include_comments=false.

Requires pandas + openpyxl:
    pip install pandas openpyxl --break-system-packages
"""

import json
import sys

DEFAULTS = {
    "language": "tr",
    "location_code": 2792,
    "video_count": 5,
    "mode": "brief",
    "include_comments": False,
}

# Loose header matching: normalized header substring -> canonical field.
HEADER_MAP = {
    "topic": "topic", "konu": "topic", "keyword": "topic",
    "anahtar": "topic", "kelime": "topic", "baslik": "topic",
    "lang": "language", "dil": "language", "language": "language",
    "location": "location_code", "lokasyon": "location_code", "loc": "location_code",
    "video": "video_count", "adet": "video_count", "count": "video_count", "sayi": "video_count",
    "mode": "mode", "mod": "mode",
    "comment": "include_comments", "yorum": "include_comments",
}

TRUE_VALUES = {"true", "1", "yes", "evet", "var", "x", "y"}


def normalize_header(h):
    h = str(h).strip().lower()
    for a, b in (("ı", "i"), ("ş", "s"), ("ç", "c"), ("ğ", "g"), ("ö", "o"), ("ü", "u"), ("İ", "i")):
        h = h.replace(a, b)
    return h


def map_columns(columns):
    """Return {original_col: canonical_field}."""
    mapping = {}
    for col in columns:
        nh = normalize_header(col)
        for key, field in HEADER_MAP.items():
            if key in nh:
                mapping[col] = field
                break
    return mapping


def coerce(field, value):
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "none"}:
        return None
    if field == "video_count":
        try:
            return int(float(s))
        except ValueError:
            return None
    if field == "location_code":
        try:
            return int(float(s))
        except ValueError:
            return s  # could be a location_name string
    if field == "include_comments":
        return s.lower() in TRUE_VALUES
    if field == "mode":
        return "draft" if "draft" in s.lower() or "taslak" in s.lower() else "brief"
    return s  # topic, language


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_input.py <path>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    try:
        import pandas as pd
    except ImportError:
        print("pandas not installed. Run: pip install pandas openpyxl --break-system-packages", file=sys.stderr)
        sys.exit(2)

    if path.lower().endswith(".csv"):
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
    else:
        df = pd.read_excel(path, dtype=str, engine="openpyxl")

    df = df.fillna("")
    colmap = map_columns(df.columns)

    if "topic" not in colmap.values():
        # No recognized topic column: treat the first column as topics.
        first = df.columns[0]
        colmap[first] = "topic"

    rows = []
    for _, r in df.iterrows():
        cfg = dict(DEFAULTS)
        for col, field in colmap.items():
            val = coerce(field, r.get(col))
            if val is not None:
                cfg[field] = val
        topic = str(cfg.get("topic", "")).strip()
        if not topic:
            continue  # skip blank rows
        cfg["topic"] = topic
        rows.append(cfg)

    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
