#!/usr/bin/env bash
set -e

APP_USER=pi
BASE=/opt/snakeeye
VENV=$BASE/venv

apt update
apt install -y git python3 python3-pip python3-venv

mkdir -p $BASE
cp -r ./* $BASE
chown -R $APP_USER:$APP_USER $BASE
chmod +x $BASE/bin/snakeye

sudo -u $APP_USER python3 -m venv $VENV
sudo -u $APP_USER $VENV/bin/pip install -r $BASE/utzo_camera_api/requirements.txt

cp services/*.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable snakeeye-api snakeeye-web
systemctl restart snakeeye-api snakeeye-web

AUTOSTART=/etc/xdg/lxsession/LXDE-pi/autostart
mkdir -p /etc/xdg/lxsession/LXDE-pi
grep -qxF "@/opt/snakeeye/bin/snakeye" $AUTOSTART || echo "@/opt/snakeeye/bin/snakeye" >> $AUTOSTART
