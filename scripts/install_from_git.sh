#!/usr/bin/env bash
set -euo pipefail

LOG=/var/log/snakeeye_install.log
mkdir -p /var/log
touch "$LOG"
chmod 664 "$LOG"

exec > >(tee -a "$LOG") 2>&1

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DST_DIR="/opt/snakeeye"

echo "==> Installer source: $SRC_DIR"
echo "==> Install target  : $DST_DIR"
date

echo "==> Checking OS arch..."
uname -m
dpkg --print-architecture

echo "==> Installing base packages..."
sudo apt update
sudo apt install -y \
  git rsync curl ca-certificates \
  python3 python3-venv python3-pip \
  build-essential cmake pkg-config \
  qtbase5-dev qttools5-dev qttools5-dev-tools \
  qtmultimedia5-dev qtwebengine5-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
  gstreamer1.0-tools gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-ugly gstreamer1.0-libav

echo "==> Creating $DST_DIR ..."
sudo mkdir -p "$DST_DIR"
sudo chown -R pi:pi "$DST_DIR"

echo "==> Copying repo to $DST_DIR ..."
# Copy everything from repo to /opt/snakeeye
sudo rsync -a --delete \
  --exclude ".git" \
  "$SRC_DIR/" "$DST_DIR/"

sudo chown -R pi:pi "$DST_DIR"

echo "==> Ensuring Qt binary is executable..."
if [[ -f "$DST_DIR/bin/snakeye" ]]; then
  sudo chmod +x "$DST_DIR/bin/snakeye"
else
  echo "ERROR: $DST_DIR/bin/snakeye not found"
  ls -ლა "$DST_DIR/bin" || true
  exit 1
fi

echo "==> Creating venv (if missing) ..."
if [[ ! -d "$DST_DIR/venv" ]]; then
  sudo -u pi python3 -m venv "$DST_DIR/venv"
fi

echo "==> Upgrading pip tooling..."
sudo -u pi "$DST_DIR/venv/bin/python" -m pip install --upgrade pip wheel setuptools

echo "==> Installing API requirements..."
if [[ -f "$DST_DIR/utzo_camera_api/requirements.txt" ]]; then
  sudo -u pi "$DST_DIR/venv/bin/pip" install -r "$DST_DIR/utzo_camera_api/requirements.txt"
else
  echo "ERROR: requirements.txt missing"
  exit 1
fi

echo "==> Installing systemd services..."
sudo cp -f "$DST_DIR/services/"*.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable snakeeye-api.service snakeeye-web.service
sudo systemctl restart snakeeye-api.service snakeeye-web.service

echo "==> Setting LXDE autostart for kiosk..."
AUTOSTART="/etc/xdg/lxsession/LXDE-pi/autostart"
sudo cp -f "$AUTOSTART" "${AUTOSTART}.bak.$(date +%Y%m%d_%H%M%S)" || true

# Remove old lines if present, then add our line
sudo sed -i '/snakeeye\/bin\/snakeye/d' "$AUTOSTART"
sudo sed -i '/start_snakeye\.sh/d' "$AUTOSTART"

# Add our launcher
echo "@/opt/snakeeye/bin/start_snakeye.sh" | sudo tee -a "$AUTOSTART" >/dev/null

echo "==> Done."
echo "Web: http://localhost:8000/"
echo "API: http://localhost:8080/docs"
echo "Reboot recommended."
