# Amina v2 — Aquaphor Smile BiH (LiveKit)

Fish Ela + Silben vor TTS (`prepare_tts_text`). Deepgram Nova-3 `bs` EU. GPT-4.1 Inference Azure.

## Lokal testen

```bash
/Users/activi/Code/Projects/LiveKit/scripts/start-amina-console.sh
```

Oder Desktop: `Amina-telefonieren.command`. Stopp: Ctrl+C.

v1 zurück: `git checkout v0.1-amina`  
v2: `git checkout v0.2-amina`


Outbound, bosnisch, Fish **Ela**, Deepgram Nova-3 EU, GPT-4.1 über LiveKit Inference (`provider=azure`).

## Lokal

```bash
cd /Users/activi/Code/Projects/LiveKit
uv sync --group dev
uv run python scripts/write_env_local.py   # schreibt .env.local, nicht committen
uv run pytest
uv run python scripts/fish_sample.py       # Ela-Hörprobe
uv run python -m amina.agent console       # Mikrofon
./scripts/start-amina-console.sh           # dasselbe
# oder Finder: Amina-telefonieren.command
```

Kein Cloud-Deploy ohne Freigabe (`lk agent create`).

## SoT

`docs/PROJECT.md`
