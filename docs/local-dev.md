# Lokal entwickeln

```bash
uv sync --group dev
cp .env.example .env.local
uv run pytest
uv run ruff check src tests
```

`.env.local` nie committen.

| Agent | Befehl |
|---|---|
| Fish | `./scripts/start-amina-console.sh` |
| Soniox v2 | `./scripts/start-amina-soniox-v2-console.sh` |
| Mujo | `uv run python -m alans_mujo_v3.agent console` |

Stopp: Ctrl+C. Headset, Mikro erlauben.
