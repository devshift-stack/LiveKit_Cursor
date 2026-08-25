# Soniox TTS — Amina (Ist-Stand)

Quelle: `src/amina/agent_soniox.py` → `build_session()`  
Agents: `amina-soniox-v2` (Cloud), `amina-soniox-v5` (lokal, erweitertes STT)

## Python (LiveKit Plugin)

```python
from livekit.plugins import soniox

tts = soniox.TTS(
    model="tts-rt-v2",
    language="bs",
    voice="Nina",
    speed=0.9,
    websocket_url="wss://tts-rt.eu.soniox.com/tts-websocket",
)
```

## Umgebungsvariablen

| Variable | Default im Code | Beschreibung |
|----------|-----------------|--------------|
| `SONIOX_API_KEY` | — | Secret (nicht committen) |
| `SONIOX_TTS_WS` | `wss://tts-rt.eu.soniox.com/tts-websocket` | **EU-WebSocket Pflicht** |
| `SONIOX_TTS_VOICE` | `Nina` | Stimme |
| `SONIOX_TTS_MODEL` | `tts-rt-v2` | Realtime-Modell |
| `SONIOX_TTS_SPEED` | `0.9` | Float, langsamer = geduldiger Klang |

Code-Defaults (`agent_soniox.py`):

```python
SONIOX_WS = os.getenv("SONIOX_TTS_WS", "wss://tts-rt.eu.soniox.com/tts-websocket")
SONIOX_VOICE = os.getenv("SONIOX_TTS_VOICE", "Nina")
SONIOX_MODEL = os.getenv("SONIOX_TTS_MODEL", "tts-rt-v2")
SONIOX_SPEED = float(os.getenv("SONIOX_TTS_SPEED", "0.9"))
```

## Parameter-Tabelle

| Parameter | Wert | Hinweis |
|-----------|------|---------|
| Modell | `tts-rt-v2` | Soniox Realtime v2 |
| Stimme | `Nina` | Amina v2 Standard |
| Sprache | `bs` | Bosnisch |
| Speed | `0.9` | Über Env drehbar |
| Endpoint | EU WebSocket | Nicht US-WS |

## Prompt / Tags (LLM → TTS)

Steuerung liegt **nicht** in der TTS-Config, sondern im Systemprompt:  
`src/amina/prompts_soniox.py`

Erlaubte Soniox-Tags (vom LLM geschrieben):

- `[warm]` `[calm]` `[curious]` `[sincerely]` `[reassuringly]` `[softly]` `[pause]`

Verboten u.a.: `[happy]`, `[excited]`, bosnische Tags, Silben-Bindestriche (`Ami-na`).

## TTS-Pipeline v2

- `AminaSonioxV2Agent.tts_node` → `Agent.default.tts_node` (kein Fish-Hyphen-Lexikon)
- Geplant (Task 7): `tts_text_transforms` mit Replace-Map (`Aquaphor` → `Akvafór`, `NSF` → `N S F`) — **noch nicht eingebaut**

## A/B / andere Agenten

| Agent | Stimme | Anmerkung |
|-------|--------|-----------|
| Amina v2 | Nina 0.9 | Cloud live (`amina-soniox-v2`) |
| Amina v5 | Nina 0.9 | lokal (`amina-soniox-v5`), STT v5 |
| Mujo V3 | Daniel | gleicher Stack, andere Stimme |
| Fish (lokal) | Ela | separates TTS, `agent.py` |
