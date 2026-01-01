#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"


APP_USER=pi
BASE=/opt/snakeeye
VENV=$BASE/venv

apt update
apt install -y git python3 python3-pip python3-venv

mkdir -p $BASE
cp -r "$ROOT_DIR/"* "$BASE/"
chown -R $APP_USER:$APP_USER $BASE
chmod +x $BASE/bin/snakeye

sudo -u $APP_USER python3 -m venv $VENV
sudo -u $APP_USER $VENV/bin/pip install -r $BASE/utzo_camera_api/requirements.txt
cp -f "${SERVICES_DIR}/snakeeye-gui.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable snakeeye-gui.service
systemctl restart snakeeye-gui.service || true

cp services/*.service /etc/systemd/system/
cp "$ROOT_DIR/services/"*.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable snakeeye-api snakeeye-web
systemctl restart snakeeye-api snakeeye-web

AUTOSTART=/etc/xdg/lxsession/LXDE-pi/autostart
mkdir -p /etc/xdg/lxsession/LXDE-pi
grep -qxF "@/opt/snakeeye/bin/snakeye" $AUTOSTART || echo "@/opt/snakeeye/bin/snakeye" >> $AUTOSTART
