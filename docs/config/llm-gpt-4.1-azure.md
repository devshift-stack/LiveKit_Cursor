# LLM — GPT-4.1 Azure via LiveKit Inference (Ist-Stand)

Quelle: `src/amina/agent_soniox.py` → `build_session()`  
Prompt: `src/amina/prompts_soniox.py` (`SYSTEM_INSTRUCTIONS_SONIOX`, `OPENER_INSTRUCTIONS_SONIOX`)

## Python (LiveKit Inference)

```python
from livekit.agents import inference

llm = inference.LLM(
    model="openai/gpt-4.1",
    provider="azure",
)
```

Keine weiteren Kwargs im Code (kein explizites `temperature`, `max_tokens`, `parallel_tool_calls`).

## Umgebungsvariablen (Azure / Foundry EU)

| Variable | Beschreibung |
|----------|--------------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI Key |
| `AZURE_OPENAI_ENDPOINT` | z.B. France Central oder Sweden Central |
| `AZURE_OPENAI_BASE_URL` | alternativ/parallel (in `write_env_local.py`) |
| `AZURE_OPENAI_DEPLOYMENT` | optional, z.B. `gpt-4.1` |

LiveKit Cloud Secrets: alle Keys in `.env.local`, Deploy mit:

```bash
lk agent update --project aai --config livekit.eu-central.toml --secrets-file=.env.local
```

## AgentSession-Kontext (zusätzlich zum LLM-Objekt)

Aktuell in `build_session()` (`agent_soniox.py`):

```python
AgentSession(
    stt=...,
    llm=inference.LLM(model="openai/gpt-4.1", provider="azure"),
    tts=...,
    turn_handling=TurnHandlingOptions(
        turn_detection=inference.TurnDetector(),  # Default-Schwelle
    ),
    allow_interruptions=True,
    min_interruption_duration=0.45,
)
```

Geplant (Plan v2, Task 3 — noch nicht im Code):

```python
turn_handling={
    "turn_detection": inference.TurnDetector(
        unlikely_threshold=0.55,  # Env: AMINA_TURN_BS_THRESHOLD
    ),
    "endpointing": {"mode": "dynamic", "min_delay": 0.5, "max_delay": 3.0},
    "interruption": {"mode": "adaptive", "min_duration": 0.5, "min_words": 0},
},
min_consecutive_speech_delay=0.3,
```

## Systemprompt (nicht LLM-Config, aber steuert Verhalten)

Datei: `src/amina/prompts_soniox.py`

| Konstante | Verwendung |
|-----------|------------|
| `SYSTEM_INSTRUCTIONS_SONIOX` | Agent-Instruktionen (Identität, Verkauf, Tags, Einwand) |
| `OPENER_INSTRUCTIONS_SONIOX` | Erster Satz nach Begrüßung / Stille-Opener |

`AminaSonioxV2Agent` / `AminaSonioxV5Agent` setzen `instructions=SYSTEM_INSTRUCTIONS_SONIOX` und rufen in `on_enter` `generate_reply(instructions=OPENER_INSTRUCTIONS_SONIOX)` auf.

## Function Tools (LLM-aufrufbar)

Definiert in `src/amina/agent.py` (`AminaAgent`):

| Tool | Zweck |
|------|-------|
| `record_permission` | Hat Person Zeit? |
| `record_water_source` | slavina / flasirana / mjesovito / filter |
| `record_clear_no` | Hartes Nein zählen (nicht weiches Nein) |
| `mark_dnc` | Do-not-call, sofort Ende |
| `request_callback` | Rückruf terminieren |
| `start_order` | Nach klarem Ja |
| `submit_order_draft` | Name, Adresse, Telefon |

## Architektur

| Aspekt | Wert |
|--------|------|
| Pipeline | Cascaded STT → LLM → TTS (kein S2S) |
| Provider | Azure über LiveKit Inference |
| Modell | `openai/gpt-4.1` |
| Region-Ziel | EU (France / Sweden / Germany Data Zone) |
| Observability | Langfuse OTLP (`src/amina/telemetry.py`) |

## Messwerte (Handoff)

- LLM TTFT ~0,9 s
- E2E nach durchgekommenem Turn ~1,3 s  
(Hauptproblem laut Handoff: Agent redet zu früh/zu lang, nicht LLM-Latenz)
