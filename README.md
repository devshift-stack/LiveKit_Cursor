# Amina — Aquaphor Smile BiH (LiveKit)

Outbound, bosnisch, Fish **Ela**, Deepgram Nova-3 EU, GPT-4.1 über LiveKit Inference (`provider=azure`).

## Lokal

```bash
cd /Users/activi/Code/Projects/LiveKit
uv sync --group dev
uv run python scripts/write_env_local.py   # schreibt .env.local, nicht committen
uv run pytest
uv run python scripts/fish_sample.py       # Ela-Hörprobe
uv run python -m amina.agent console       # Mikrofon
```

Kein Cloud-Deploy ohne Freigabe (`lk agent create`).

## SoT

`docs/PROJECT.md`
