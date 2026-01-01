# SnakeEye Kiosk System

Target:
- Raspberry Pi 4
- Raspberry Pi OS Bullseye
- Qt5 + GStreamer

Install on fresh Pi:
```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/muji/snakeeye.git
cd snakeeye/scripts
sudo ./install_from_git.sh
sudo reboot
