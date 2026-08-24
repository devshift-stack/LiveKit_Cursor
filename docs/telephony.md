# Telefonie (kein Secret in dieser Datei)

Kette: LiveKit Cloud → SIP UDP → FreePBX `ari.activi.io` → Yeastar TG400 → GSM.

| Ext | Rolle |
|---|---|
| 300 | TG400 (GSM) |
| 310 | Guarddograh (nicht LiveKit) |
| 320 | Hermes, frei |
| 330 | LiveKit-Nebenstelle (Auth) |

Outbound-Trunk in LiveKit Cloud: Name `LiveKit`, Number `+387…` der SIM, User **330**, Transport **UDP**, SRTP **disabled**.

Anruf aus der UI: **kein** Wählknopf. Skript:

```bash
./scripts/call-live-gsm.sh
```

Wenn PBX `Failed to authenticate`: LiveKit-From ist die +387-Nummer, nicht 330. PJSIP Identify für LiveKit-IPs auf Ext 330 setzen.

Nebenstellen nur in der FreePBX-GUI anlegen.
