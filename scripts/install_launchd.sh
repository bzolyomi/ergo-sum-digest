#!/bin/bash
# Installs (or reinstalls) the launchd agent. Run once: bash scripts/install_launchd.sh
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/Library/LaunchAgents/com.ergosum.digest.plist"
mkdir -p "$HOME/.ergo-sum"
[ -f "$HOME/.ergo-sum/env" ] || { echo "Create ~/.ergo-sum/env first (see README)"; exit 1; }
sed -e "s#__REPO__#$REPO#g" -e "s#__HOME__#$HOME#g" "$REPO/scripts/com.ergosum.digest.plist" > "$DEST"
launchctl bootout "gui/$(id -u)/com.ergosum.digest" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"
echo "Installed. Log: ~/.ergo-sum/run.log"
