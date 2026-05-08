#!/usr/bin/env python3
"""
generate_caddyfile.py
Reads students.csv and generates Caddyfile routing blocks.
Usage: python3 generate_caddyfile.py
Output: Caddyfile
"""

import csv
import os
import sys

INPUT_FILE   = "students.csv"
OUTPUT_FILE  = "Caddyfile"
SERVER_HOST  = "your-server.school.local"   # ← change this to your hostname

def sanitize(username: str) -> str:
    return username.strip().lower().replace(" ", "_").replace("-", "_")

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found.")
        sys.exit(1)

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        students = [row for row in csv.DictReader(f) if row.get("username", "").strip()]

    lines = []
    lines.append(f"# AUTO-GENERATED — do not edit by hand.")
    lines.append(f"")
    lines.append(f"{SERVER_HOST} {{")
    lines.append(f"")

    for student in students:
        username = sanitize(student["username"])
        lines.append(f"    handle /ide/{username}/* {{")
        lines.append(f"        uri strip_prefix /ide/{username}")
        lines.append(f"        reverse_proxy ide_{username}:8080")
        lines.append(f"    }}")
        lines.append(f"")

    lines.append(f"    handle {{")
    lines.append(f'        respond "C++ IDE — please use your assigned URL." 200')
    lines.append(f"    }}")
    lines.append(f"")
    lines.append(f"    tls internal")
    lines.append(f"}}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Generated {OUTPUT_FILE} for {len(students)} students.")

if __name__ == "__main__":
    main()
