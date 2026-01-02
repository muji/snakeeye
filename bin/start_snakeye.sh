#!/usr/bin/env bash
set -euo pipefail

LOG=/var/log/snakeeye_gui.log
mkdir -p /var/log
touch "$LOG"
chmod 664 "$LOG"

echo "=== start_snakeye.sh $(date) ===" >> "$LOG"

# LXDE starts X on :0
export DISPLAY=:0
export XAUTHORITY=/home/pi/.Xauthority

# Give X / network time
sleep 2

# Optional: reduce Qt noise. Set to 1 for debugging.
export QT_DEBUG_PLUGINS=0

exec /opt/snakeeye/bin/snakeye >>"$LOG" 2>&1
