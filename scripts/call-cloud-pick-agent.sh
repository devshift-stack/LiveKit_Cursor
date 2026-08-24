#!/usr/bin/env bash
# Interaktiv: LiveKit Cloud → Agent wählen → Nummer → Anruf.
# Logs: <repo>/logs/calls/<timestamp>/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PROJECT="${LIVEKIT_PROJECT:-aai}"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG_DIR="$ROOT/logs/calls/$STAMP"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/run.log"
ERR="$LOG_DIR/error.log"
META="$LOG_DIR/meta.txt"
DIAG="$LOG_DIR/diagnose.txt"

# Alles mitloggen, Terminal bleibt lesbar
exec > >(tee -a "$LOG") 2> >(tee -a "$ERR" >&2)

confirm() {
  local q="$1"
  local a
  read -r -p "$q [j/N]: " a
  [[ "$a" == "j" || "$a" == "J" || "$a" == "y" || "$a" == "Y" ]]
}

echo "========================================"
echo " LiveKit Cloud — Anruf"
echo " Zeit:  $(date -Iseconds)"
echo " Log:   $LOG"
echo " Fehler:$ERR"
echo "========================================"

if ! command -v lk >/dev/null 2>&1; then
  echo "lk fehlt. LiveKit CLI installieren." | tee "$DIAG"
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 fehlt." | tee "$DIAG"
  exit 1
fi

echo
echo "1) Verbinde Projekt: $PROJECT"
if ! lk agent list --project "$PROJECT" --json >"$LOG_DIR/agents.json" 2>"$LOG_DIR/agents.err"; then
  echo "Cloud-Liste fehlgeschlagen. Siehe agents.err" | tee "$DIAG"
  cat "$LOG_DIR/agents.err" || true
  exit 1
fi

python3 - "$LOG_DIR/agents.json" "$LOG_DIR/agents.tsv" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
data = json.load(open(src))
rows = []
for a in data.get("agents") or []:
    name = (a.get("agentName") or "").strip()
    aid = a.get("agentId") or ""
    deps = a.get("agentDeployments") or []
    dep = deps[0] if deps else {}
    status = dep.get("status") or "?"
    region = dep.get("region") or "?"
    repl = dep.get("replicas")
    pick = "1" if name and status == "Running" else "0"
    rows.append((pick, name or "(ohne Namen)", aid, status, region, str(repl if repl is not None else "-")))
with open(dst, "w") as f:
    for i, r in enumerate(rows, 1):
        f.write("\t".join([str(i), *r]) + "\n")
print(f"{len(rows)} Agenten in der Cloud")
PY

echo
echo "Verfügbare Agenten:"
printf "  %-4s %-22s %-8s %-12s %s\n" "#" "Name" "Status" "Region" "ID"
while IFS=$'\t' read -r n pick name aid status region repl; do
  mark=""
  [[ "$pick" == "1" ]] || mark="  (nicht wählbar)"
  printf "  %-4s %-22s %-8s %-12s %s%s\n" "$n" "$name" "$status" "$region" "$aid" "$mark"
done <"$LOG_DIR/agents.tsv"
echo

read -r -p "Nummer des Agenten: " CHOICE
[[ "$CHOICE" =~ ^[0-9]+$ ]] || { echo "Keine gültige Auswahl." | tee "$DIAG"; exit 2; }

IFS=$'\t' read -r n pick AGENT_NAME AGENT_ID STATUS REGION REPL < <(awk -F'\t' -v c="$CHOICE" '$1==c{print; exit}' "$LOG_DIR/agents.tsv")
if [[ -z "${AGENT_NAME:-}" ]]; then
  echo "Auswahl $CHOICE nicht gefunden." | tee "$DIAG"
  exit 2
fi
if [[ "$pick" != "1" ]]; then
  echo "Dieser Agent läuft nicht (Status=$STATUS, Name=$AGENT_NAME)." | tee "$DIAG"
  exit 2
fi

echo
echo "Gewählt: $AGENT_NAME"
echo "  ID=$AGENT_ID  Status=$STATUS  Region=$REGION"
if ! confirm "Diesen Agenten nehmen?"; then
  echo "Abbruch (Agent)." | tee "$DIAG"
  exit 3
fi

echo
echo "2) SIP-Trunks"
lk sip outbound list --project "$PROJECT" --json >"$LOG_DIR/trunks.json" 2>"$LOG_DIR/trunks.err" || true
python3 - "$LOG_DIR/trunks.json" "$LOG_DIR/trunks.tsv" <<'PY'
import json, sys
from pathlib import Path
src, dst = sys.argv[1], sys.argv[2]
p = Path(src)
if not p.exists() or p.stat().st_size == 0:
    Path(dst).write_text("")
    raise SystemExit(0)
data = json.loads(p.read_text() or "{}")
items = data.get("items") or []
with open(dst, "w") as f:
    for i, t in enumerate(items, 1):
        nums = ",".join(t.get("numbers") or [])
        f.write("\t".join([
            str(i),
            t.get("sipTrunkId") or "",
            t.get("name") or "",
            t.get("address") or "",
            t.get("transport") or "",
            nums,
            t.get("authUsername") or "",
        ]) + "\n")
print(f"{len(items)} Trunk(s)")
PY

if [[ ! -s "$LOG_DIR/trunks.tsv" ]]; then
  echo "Kein Outbound-Trunk. In LiveKit Telephony anlegen." | tee "$DIAG"
  exit 1
fi
echo
printf "  %-4s %-18s %-16s %-16s %s\n" "#" "ID" "Name" "Host" "Nummer"
while IFS=$'\t' read -r n tid tname addr trans nums user; do
  printf "  %-4s %-18s %-16s %-16s %s\n" "$n" "$tid" "$tname" "$addr" "$nums"
done <"$LOG_DIR/trunks.tsv"
echo
TRUNK_COUNT=$(wc -l <"$LOG_DIR/trunks.tsv" | tr -d ' ')
if [[ "$TRUNK_COUNT" == "1" ]]; then
  IFS=$'\t' read -r _ TRUNK_ID TRUNK_NAME TRUNK_ADDR _ TRUNK_NUMS TRUNK_USER <"$LOG_DIR/trunks.tsv"
  echo "Trunk automatisch: $TRUNK_NAME ($TRUNK_ID)"
else
  read -r -p "Nummer des Trunks: " TCHOICE
  IFS=$'\t' read -r _ TRUNK_ID TRUNK_NAME TRUNK_ADDR _ TRUNK_NUMS TRUNK_USER < <(awk -F'\t' -v c="$TCHOICE" '$1==c{print; exit}' "$LOG_DIR/trunks.tsv")
  [[ -n "${TRUNK_ID:-}" ]] || { echo "Trunk nicht gefunden." | tee "$DIAG"; exit 2; }
fi

echo
read -r -p "Zielnummer (E.164, z.B. +3876...): " DEST
DEST="${DEST// /}"
if [[ ! "$DEST" =~ ^\+[0-9]{8,15}$ ]]; then
  echo "Ungültig. Braucht + und 8–15 Ziffern." | tee "$DIAG"
  exit 2
fi
if ! confirm "Jetzt $AGENT_NAME an $DEST anrufen?"; then
  echo "Abbruch (Nummer)." | tee "$DIAG"
  exit 3
fi

ROOM="out-${AGENT_NAME}-${STAMP}"
{
  echo "stamp=$STAMP"
  echo "project=$PROJECT"
  echo "agent_name=$AGENT_NAME"
  echo "agent_id=$AGENT_ID"
  echo "region=$REGION"
  echo "status=$STATUS"
  echo "trunk_id=$TRUNK_ID"
  echo "trunk_name=$TRUNK_NAME"
  echo "trunk_addr=$TRUNK_ADDR"
  echo "trunk_user=$TRUNK_USER"
  echo "from_numbers=$TRUNK_NUMS"
  echo "dest=$DEST"
  echo "room=$ROOM"
} >"$META"

echo
echo "3) Dispatch $AGENT_NAME → Raum $ROOM"
set +e
lk dispatch create --project "$PROJECT" --room "$ROOM" --agent-name "$AGENT_NAME" \
  >"$LOG_DIR/dispatch.out" 2>"$LOG_DIR/dispatch.err"
DC=$?
set -e
cat "$LOG_DIR/dispatch.out" || true
if [[ $DC -ne 0 ]]; then
  echo "Dispatch fehlgeschlagen ($DC)." | tee "$DIAG"
  cat "$LOG_DIR/dispatch.err" || true
  echo "dispatch_exit=$DC" >>"$META"
  exit "$DC"
fi

echo
echo "4) Wähle $DEST über $TRUNK_ID …"
set +e
lk sip participant create --project "$PROJECT" \
  --trunk "$TRUNK_ID" \
  --call "$DEST" \
  --room "$ROOM" \
  --identity "sip-${DEST#+}" \
  --name "GSM" \
  --wait \
  --timeout 90s \
  >"$LOG_DIR/sip.out" 2>"$LOG_DIR/sip.err"
SC=$?
set -e
cat "$LOG_DIR/sip.out" || true
if [[ -s "$LOG_DIR/sip.err" ]]; then
  echo "--- sip.err ---"
  cat "$LOG_DIR/sip.err"
fi
echo "sip_exit=$SC" >>"$META"
echo "dispatch_exit=0" >>"$META"

{
  echo "sip_exit=$SC"
  echo "room=$ROOM dest=$DEST agent=$AGENT_NAME"
  echo
  if [[ $SC -eq 0 ]]; then
    echo "OK: Teilnehmer verbunden (oder wait beendet ohne Fehler)."
  else
    echo "Anruf nicht durchgekommen."
    if grep -qi "max auth retry\|failed_precondition\|Failed to authenticate\|401" \
      "$LOG_DIR/sip.out" "$LOG_DIR/sip.err" "$ERR" 2>/dev/null; then
      echo "Hinweis: PBX hat LiveKit nicht als Ext erkannt (401 / auth retry)."
      echo "Fix: PJSIP Identify — LiveKit-IPs auf die Auth-Nebenstelle (330), nicht 300."
    elif grep -qi "timeout\|USER_UNAVAILABLE\|480\|408" \
      "$LOG_DIR/sip.out" "$LOG_DIR/sip.err" 2>/dev/null; then
      echo "Hinweis: niemand abgenommen oder Ziel nicht erreichbar."
    elif grep -qi "486\|busy\|603" \
      "$LOG_DIR/sip.out" "$LOG_DIR/sip.err" 2>/dev/null; then
      echo "Hinweis: besetzt / abgelehnt."
    else
      echo "Rohdaten: sip.out / sip.err / error.log in diesem Ordner."
    fi
  fi
} | tee "$DIAG"

echo
echo "Fertig. Alles unter: $LOG_DIR"
echo "Enter schließt das Fenster."
read -r _
exit "$SC"
