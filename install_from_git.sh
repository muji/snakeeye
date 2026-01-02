#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
exec sudo "$DIR/scripts/install_from_git.sh"
