#!/usr/bin/env bash
# Nach Yeastar: Anruf über den LIVE Cloud-Agenten (amina-soniox-v2).
# Fragt nach der Zielnummer. Schreibt Log + Error-Log.
set -euo pipefail

PROJECT="${LIVEKIT_PROJECT:-aai}"
AGENT_NAME="${LIVEKIT_AGENT_NAME:-amina-soniox-v2}"
TRUNK_ID="${LIVEKIT_SIP_TRUNK_ID:-ST_ity6jXX3KWMw}"
LOG_DIR="${LIVEKIT_CALL_LOG_DIR:-$HOME/.hermes/logs/livekit-calls}"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$LOG_DIR/call-$STAMP.log"
ERR="$LOG_DIR/call-$STAMP.err.log"

exec > >(tee -a "$LOG") 2> >(tee -a "$ERR" >&2)

echo "log: $LOG"
echo "err: $ERR"
echo "project=$PROJECT agent=$AGENT_NAME trunk=$TRUNK_ID"
echo "time=$(date -Iseconds)"

read -r -p "Zielnummer (E.164, z.B. +3876...): " DEST
DEST="${DEST// /}"
if [[ ! "$DEST" =~ ^\+[0-9]{8,15}$ ]]; then
  echo "Ungültige Nummer. Braucht + und Ziffern, z.B. +38763558550" >&2
  exit 2
fi

echo "Prüfe Agent..."
lk agent status --project "$PROJECT" --id CA_J8AZ7K6yJ5o3 || true
echo "Prüfe Trunk..."
lk sip outbound list --project "$PROJECT"

ROOM="amina-out-$STAMP"
echo "Dispatch $AGENT_NAME -> room $ROOM"
lk dispatch create --project "$PROJECT" --room "$ROOM" --agent-name "$AGENT_NAME"

echo "Wähle $DEST ..."
set +e
lk sip participant create --project "$PROJECT" \
  --trunk "$TRUNK_ID" \
  --call "$DEST" \
  --room "$ROOM" \
  --identity "sip-${DEST#+}" \
  --name "GSM" \
  --wait \
  --timeout 90s
RC=$?
set -e
echo "sip_exit=$RC room=$ROOM dest=$DEST"
echo "Fertig. Logs: $LOG  $ERR"
exit "$RC"
