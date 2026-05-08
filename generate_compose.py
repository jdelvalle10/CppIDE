#!/usr/bin/env python3
"""
generate_compose.py
Reads students.csv and generates docker-compose.yml for the C++ IDE deployment.
Usage: python3 generate_compose.py
Output: docker-compose.yml
"""

import csv
import sys
import os

INPUT_FILE  = "students.csv"
OUTPUT_FILE = "docker-compose.yml"
IMAGE_NAME  = "cpp-ide:latest"       # must match what you built with docker build
NETWORK     = "ide_net"
BASE_PORT   = 8100                   # first student gets 8100, next 8101, etc.
                                     # Caddy handles routing so these stay internal

def sanitize(username: str) -> str:
    """Make username safe for Docker service names."""
    return username.strip().lower().replace(" ", "_").replace("-", "_")

def generate_compose(students: list[dict]) -> str:
    lines = []
    lines.append("# AUTO-GENERATED — do not edit by hand.")
    lines.append("# Re-run generate_compose.py to update.")
    lines.append("")
    lines.append("services:")

    volume_names = []

    for i, student in enumerate(students):
        username = sanitize(student["username"])
        password = student["password"].strip()
        port     = BASE_PORT + i
        volume   = f"{username}_workspace"
        volume_names.append(volume)

        lines.append("")
        lines.append(f"  {username}:")
        lines.append(f"    image: {IMAGE_NAME}")
        lines.append(f"    container_name: ide_{username}")
        lines.append(f"    restart: unless-stopped")
        lines.append(f"    environment:")
        lines.append(f"      - PASSWORD={password}")
        lines.append(f"      - DOCKER_USER=coder")
        lines.append(f"    volumes:")
        lines.append(f"      - {volume}:/home/coder/project")
        lines.append(f"    networks:")
        lines.append(f"      - {NETWORK}")
        lines.append(f"    # Internal port only — Caddy proxies externally")
        lines.append(f"    expose:")
        lines.append(f"      - \"8080\"")

    lines.append("")
    lines.append("volumes:")
    for v in volume_names:
        lines.append(f"  {v}:")

    lines.append("")
    lines.append("networks:")
    lines.append(f"  {NETWORK}:")
    lines.append(f"    driver: bridge")

    return "\n".join(lines) + "\n"

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found. Create it first.")
        sys.exit(1)

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        students = [row for row in reader if row.get("username", "").strip()]

    if not students:
        print("ERROR: No students found in CSV.")
        sys.exit(1)

    compose_content = generate_compose(students)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(compose_content)

    print(f"Generated {OUTPUT_FILE} for {len(students)} students.")
    print("Next step: docker compose up -d")

if __name__ == "__main__":
    main()
