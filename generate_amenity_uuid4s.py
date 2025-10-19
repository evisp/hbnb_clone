#!/usr/bin/env python3
import uuid
import sys

def gen_uuid4():
    u = uuid.uuid4()
    # Sanity checks: version 4 and canonical string with hyphens
    if u.version != 4:
        raise RuntimeError("Generated UUID is not v4")
    s = str(u)
    parts = s.split('-')
    if len(parts) != 5 or len(parts[0]) != 8 or len(parts[1]) != 4 or len(parts[2]) != 4 or len(parts[3]) != 4 or len(parts[4]) != 12:
        raise RuntimeError("Generated UUID not in canonical 8-4-4-4-12 format")
    if not parts[2].startswith('4'):
        raise RuntimeError("UUID middle section does not indicate version 4")
    if parts[3][0].lower() not in ('8','9','a','b'):
        raise RuntimeError("UUID variant nibble is not RFC 4122 (8,9,a,b)")
    return s

def main():
    # Generate exactly three UUID4s for amenities
    count = 3
    uuids = [gen_uuid4() for _ in range(count)]

    # Print plain list
    print("Generated UUID4s:")
    for i, u in enumerate(uuids, 1):
        print(f"{i}. {u}")

    # Print SQL INSERTs for amenities (replace names as needed)
    names = ["WiFi", "Swimming Pool", "Air Conditioning"]
    print("\n-- Copy-paste into seed.sql (adjust names if necessary):")
    for u, name in zip(uuids, names):
        # Escape any single quotes in name just in case
        safe_name = name.replace("'", "''")
        print(f"INSERT INTO amenities (id, name) VALUES ('{u}', '{safe_name}');")

    # Also print a compact CSV row set if you prefer spreadsheets
    print("\n-- CSV (id,name):")
    for u, name in zip(uuids, names):
        print(f"{u},{name}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
