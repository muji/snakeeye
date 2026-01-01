#!/usr/bin/env bash
set -euo pipefail

APP_NAME="snakeeye"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # repo root
DST_DIR="/opt/${APP_NAME}"
PI_USER="${SUDO_USER:-pi}"

log() { echo -e "\n==> $*"; }

if [[ $EUID -ne 0 ]]; then
  echo "ERROR: Run with sudo: sudo ./scripts/install_from_git.sh"
  exit 1
fi

log "Installer source: ${SRC_DIR}"
log "Install target  : ${DST_DIR}"
log "User            : ${PI_USER}"

# -------------------------------
# 1) APT packages (minimal set)
# -------------------------------
log "Installing base packages..."
apt update
apt install -y \
  git rsync curl \
  python3 python3-venv python3-pip

# (Optional) if you want Qt runtime deps from apt (usually not needed if binary already works)
# apt install -y libqt5core5a libqt5gui5 libqt5widgets5 libqt5webenginewidgets5

# -------------------------------
# 2) Create /opt/snakeeye + copy repo content
# -------------------------------
log "Creating install folder..."
mkdir -p "${DST_DIR}"

log "Syncing repo -> /opt (always overwrite changed files)..."
# Exclude .git to keep /opt clean
rsync -a --delete --exclude ".git" "${SRC_DIR}/" "${DST_DIR}/"

log "Fixing ownership..."
chown -R "${PI_USER}:${PI_USER}" "${DST_DIR}"

# -------------------------------
# 3) Validate required paths
# -------------------------------
BIN="${DST_DIR}/bin/snakeye"
API_DIR="${DST_DIR}/utzo_camera_api"
WWW_DIR="${DST_DIR}/www"
SERVICES_DIR="${DST_DIR}/services"
VENV_DIR="${DST_DIR}/venv"

log "Validating required files..."
[[ -f "${BIN}" ]] || { echo "ERROR: Missing ${BIN}"; exit 2; }
[[ -d "${API_DIR}" ]] || { echo "ERROR: Missing ${API_DIR}"; exit 2; }
[[ -f "${API_DIR}/requirements.txt" ]] || { echo "ERROR: Missing requirements.txt"; exit 2; }
[[ -f "${API_DIR}/run.py" ]] || { echo "ERROR: Missing ${API_DIR}/run.py"; exit 2; }
[[ -d "${WWW_DIR}" ]] || { echo "ERROR: Missing ${WWW_DIR}"; exit 2; }
[[ -d "${SERVICES_DIR}" ]] || { echo "ERROR: Missing ${SERVICES_DIR}"; exit 2; }
[[ -f "${SERVICES_DIR}/snakeeye-api.service" ]] || { echo "ERROR: Missing snakeeye-api.service"; exit 2; }
[[ -f "${SERVICES_DIR}/snakeeye-web.service" ]] || { echo "ERROR: Missing snakeeye-web.service"; exit 2; }

# -------------------------------
# 4) Ensure Qt binary executable
# -------------------------------
log "Ensuring Qt binary is executable..."
chmod +x "${BIN}"

# -------------------------------
# 5) Setup Python venv + requirements
# -------------------------------
log "Setting up Python venv..."
sudo -u "${PI_USER}" python3 -m venv "${VENV_DIR}"

log "Upgrading pip..."
sudo -u "${PI_USER}" "${VENV_DIR}/bin/pip" install --upgrade pip

log "Installing API requirements..."
sudo -u "${PI_USER}" "${VENV_DIR}/bin/pip" install -r "${API_DIR}/requirements.txt"

# -------------------------------
# 6) Install systemd services
# -------------------------------
log "Installing systemd service files..."
cp -f "${SERVICES_DIR}/snakeeye-api.service" /etc/systemd/system/
cp -f "${SERVICES_DIR}/snakeeye-web.service" /etc/systemd/system/

log "Reloading systemd..."
systemctl daemon-reload

log "Enabling services..."
systemctl enable snakeeye-api.service
systemctl enable snakeeye-web.service

log "Restarting services..."
systemctl restart snakeeye-api.service || true
systemctl restart snakeeye-web.service || true

# -------------------------------
# 7) Show status + quick checks
# -------------------------------
log "Service status:"
systemctl --no-pager --full status snakeeye-api.service || true
systemctl --no-pager --full status snakeeye-web.service || true

log "Port checks:"
ss -lntp | egrep ':8000|:8080|:5000|:7000' || true

log "HTTP check:"
curl -sS --max-time 2 http://127.0.0.1:8000 >/dev/null && echo "OK: http://localhost:8000 reachable" || echo "WARN: web not reachable"

log "Install complete."
echo "Next: reboot (recommended): sudo reboot"
