# Agenten-Registry

Ein Blick. Quelle: Dateien unter `src/`. Neu schreiben:

```bash
uv run python scripts/update-agent-registry.py
```

Zuletzt gebaut: **2026-08-24 07:44 CEST**

| Anzeige | LiveKit-Name | Datei | Stimme | Rolle | Letzter Git |
|---|---|---|---|---|---|
| Alans_mujo V3 Soniox | `alans-mujo-v3` | `src/alans_mujo_v3/agent.py` | Soniox Daniel | Familien-Demo Dr Mujo | 2b3d1cb 2026-08-24T07:10:42+02:00 |
| amina | `amina` | `src/amina/agent.py` | Fish Ela | Amina Verkauf Fish | b318644 2026-08-24T05:17:47+02:00 |
| Template V1 | `template-v1` | `src/amina/template_v1/agent.py` | Soniox Nina | Vorlage (Klon) | 114343e 2026-08-24T07:04:48+02:00 |
| amina-soniox | `amina-soniox` | `src/amina/agent_soniox.py` | Soniox Nina | Amina Soniox alt | 2b3d1cb 2026-08-24T07:10:42+02:00 |
| amina-soniox-v2 | `amina-soniox-v2` | `src/amina/agent_soniox_v2.py` | Soniox Nina | Amina Verkauf — Cloud | b318644 2026-08-24T05:17:47+02:00 |

## Cloud (manuell prüfen: `lk agent list --project aai`)

| ID | Name |
|---|---|
| `CA_J8AZ7K6yJ5o3` | `amina-soniox-v2` |

Mujo und Template sind **nicht** deployed.

## Start

| Agent | Befehl |
|---|---|
| Fish | Desktop `01-Amina-Fish.command` |
| Amina Soniox alt | Desktop `02-Amina-Soniox-alt.command` |
| Amina v2 | Desktop `03-Amina-v2-Soniox.command` |
| Template V1 | Desktop `04-Template-V1.command` |
| Mujo | Desktop `05-Alans-Mujo-V3.command` |
| GSM-Call (Cloud-Amina) | `./scripts/call-live-gsm.sh` |
