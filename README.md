# VoiceAgents

LiveKit-Telefonagenten (Bosnisch). Ein Repo, mehrere Agenten.  
Lokal: `/Users/activi/Code/Projects/LiveKit`  
GitHub: [devshift-stack/VoiceAgents](https://github.com/devshift-stack/VoiceAgents)

Secrets nie committen. `.env.local` bleibt lokal.

## Ordner

```
src/amina/            Fish + Soniox Amina + Template V1
src/alans_mujo_v3/    Dr Mujo (Familien-Demo)
scripts/              Start, Clone, GSM-Anruf
tests/                pytest
docs/                 Unterlagen
Dockerfile            Cloud-Worker = nur amina-soniox-v2
```

## Agenten

Ein Blick: **[AGENTEN.md](AGENTEN.md)** (nach neuem Agenten: `uv run python scripts/update-agent-registry.py`).

| Name | LiveKit `agent_name` | Stimme | Cloud |
|---|---|---|---|
| Amina Fish | `amina` | Fish Ela | nein |
| Amina Soniox (alt) | `amina-soniox` | Nina, ohne Tag-Prompt | nein |
| **Amina v2 Soniox** | `amina-soniox-v2` | Nina + Tags, 0.9 | **ja** eu-central |
| Template V1 | `template-v1` | wie v2, nur Vorlage | nein |
| Alans_mujo V3 | `alans-mujo-v3` | Daniel | nein |

Details: [docs/agents/](docs/agents/README.md)

## Stack (gesperrt bei Soniox-Klonen)

- STT: Deepgram Nova-3, `bs`, EU
- LLM: GPT-4.1 über LiveKit Inference, Azure
- TTS Amina v2: Soniox Nina, `tts-rt-v2`, Speed 0.9, EU-WS
- TTS Mujo: dieselbe Kette, Stimme **Daniel**
- Tags: `[warm] [calm] [curious] [sincerely] [reassuringly] [softly] [pause]`
- Keine Fish-Bindestriche auf Soniox

## Lokal

```bash
cd /Users/activi/Code/Projects/LiveKit
uv sync --group dev
cp .env.example .env.local   # Keys selbst eintragen
uv run pytest
./scripts/start-amina-soniox-v2-console.sh
# Mujo:
uv run python -m alans_mujo_v3.agent console
```

Desktop-Ordner `~/Desktop/LiveKit Agents/` — eine `.command` pro Agent.

## Cloud

Nur **amina-soniox-v2** ist deployed (`CA_J8AZ7K6yJ5o3`, eu-central).  
Dockerfile `CMD` nicht auf einen anderen Agenten stellen, sonst überschreibt der nächste Deploy Amina.

## GSM-Anruf (nach Yeastar)

```bash
./scripts/call-live-gsm.sh
```

Fragt die Zielnummer. Log: `~/.hermes/logs/livekit-calls/`.  
Ruft den **live** Cloud-Agenten (`amina-soniox-v2`), nicht Mujo.

## Neuer Agent vom Template

```bash
uv run python scripts/new-from-template-v1.py --slug firma_x --agent-name firma-x
```

Nur `prompts.py`, `soul.md`, `project.toml` ändern.  
In einer frischen Session Skill **`livekit-agent-from-brief`** laden — der fragt zuerst und baut dann.

## Unterlagen

| Datei | Inhalt |
|---|---|
| [docs/agents/README.md](docs/agents/README.md) | alle Agenten |
| [docs/stack.md](docs/stack.md) | Modelle, Tags, EU |
| [docs/local-dev.md](docs/local-dev.md) | uv, Tests, Console |
| [docs/deploy.md](docs/deploy.md) | LiveKit Cloud |
| [docs/telephony.md](docs/telephony.md) | FreePBX / TG / SIP (keine Secrets) |
| [docs/00-LESEN.md](docs/00-LESEN.md) | Index Unterlagen |
| [docs/HANDOFF.md](docs/HANDOFF.md) | Team-Handover |
| [docs/FIXPLAN-AMINA-V2.md](docs/FIXPLAN-AMINA-V2.md) | nächster Amina-Umbau (prüfen) |
| [docs/LIVEKIT-BEST-PRACTICE.md](docs/LIVEKIT-BEST-PRACTICE.md) | LiveKit-Regeln |
| [docs/RESEARCH.md](docs/RESEARCH.md) | Recherche Session |
| [docs/PROJECT.md](docs/PROJECT.md) | Amina Verkaufs-SoT (teilweise überholt) |
