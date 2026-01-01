#!/bin/bash
SPLASH="/opt/snakeeye/splash/seye_new.gif"
LOG="/var/log/snakeeye_splash.log"

echo "Splash start: $(date)" >> "$LOG"

export DISPLAY=:0
export XAUTHORITY=/home/pi/.Xauthority

# show splash fullscreen
feh --fullscreen --hide-pointer --auto-zoom "$SPLASH" &
FEH_PID=$!

sleep 10

kill "$FEH_PID" 2>/dev/null || true

# start app
exec /opt/snakeeye/bin/snakeye
