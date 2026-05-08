#!/bin/bash
# =============================================================================
# deploy.sh — Full C++ IDE Deployment
# Run as a user with Docker permissions (add yourself to docker group first).
# Professor Del Valle — Doral Academy / Miami Dade College
# =============================================================================

set -e  # Exit immediately on any error

echo "========================================"
echo " C++ IDE Deployment — Starting"
echo "========================================"

# ── Step 1: Install Docker if not present ────────────────────────────────────
if ! command -v docker &> /dev/null; then
    echo "[1/6] Installing Docker..."
    curl -fsSL https://get.docker.com | bash
    sudo usermod -aG docker $USER
    echo "Docker installed. You may need to log out and back in."
else
    echo "[1/6] Docker already installed. Skipping."
fi

# ── Step 2: Install Docker Compose plugin ────────────────────────────────────
if ! docker compose version &> /dev/null; then
    echo "[2/6] Installing Docker Compose plugin..."
    sudo apt-get update && sudo apt-get install -y docker-compose-plugin
else
    echo "[2/6] Docker Compose already installed. Skipping."
fi

# ── Step 3: Install Caddy ─────────────────────────────────────────────────────
if ! command -v caddy &> /dev/null; then
    echo "[3/6] Installing Caddy..."
    sudo apt-get install -y debian-keyring debian-archive-keyring apt-transport-https
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
        | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
        | sudo tee /etc/apt/sources.list.d/caddy-stable.list
    sudo apt-get update && sudo apt-get install -y caddy
else
    echo "[3/6] Caddy already installed. Skipping."
fi

# ── Step 4: Build the Docker image ───────────────────────────────────────────
echo "[4/6] Building C++ IDE Docker image..."
docker build -t cpp-ide:latest .

# ── Step 5: Generate docker-compose.yml and Caddyfile from roster ─────────────
echo "[5/6] Generating docker-compose.yml and Caddyfile from students.csv..."
python3 generate_compose.py
python3 generate_caddyfile.py

# ── Step 6: Start all containers ─────────────────────────────────────────────
echo "[6/6] Starting all student containers..."
docker compose up -d

# ── Step 7: Start Caddy ───────────────────────────────────────────────────────
echo "Starting Caddy reverse proxy..."
sudo cp Caddyfile /etc/caddy/Caddyfile
sudo systemctl reload caddy || sudo systemctl start caddy

echo ""
echo "========================================"
echo " Deployment Complete"
echo "========================================"
echo " Student URL pattern:"
echo "   https://your-server.school.local/ide/USERNAME"
echo ""
echo " To check running containers:"
echo "   docker compose ps"
echo ""
echo " To view logs for a student container:"
echo "   docker compose logs ide_jdoe"
echo "========================================"
