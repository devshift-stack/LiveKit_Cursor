# Deepgram Nova-3 — Amina (Ist-Stand)

Quelle: `src/amina/agent.py` → `build_deepgram_stt()` (genutzt von `agent_soniox.build_session()` / v2 / v5 / Template / Mujo).

Replace-Map: `docs/voice/deepgram-replace.json` — pflegen mit `./scripts/replace.sh`

## Python (LiveKit Plugin)

Runtime: `build_deepgram_stt()` in `src/amina/agent.py` — gleiche Parameter wie unten.

```python
from livekit.plugins import deepgram

stt = deepgram.STT(
    model="nova-3",
    language="bs",              # Bosnisch fest — nicht "multi"
    keyterm=[
        "Aquaphor",
        "Smile",
        "Firmira",
        "Amina",
        "bokal",
        "pouzeće",
        "flaširana",
        "slavina",
        "kamenac",
    ],
    filler_words=True,
    punctuate=True,
    smart_format=True,
    endpointing_ms=300,
    vad_events=True,
    replace={"flaširana": "flasirana"},  # aus deepgram-replace.json
    base_url="https://api.eu.deepgram.com/v1/listen",  # EU-Residenz — Pflicht
)
```

## Umgebungsvariablen

| Variable | Wert | Pflicht |
|----------|------|---------|
| `DEEPGRAM_API_KEY` | Secret (nicht committen) | ja |
| `DEEPGRAM_BASE_URL` | `https://api.eu.deepgram.com/v1/listen` | ja (EU) |

Default in Code: `resolve_deepgram_eu_base_url()` → immer `api.eu.deepgram.com/v1/listen` (US-URL wird ignoriert)  
(`src/amina/agent.py`)

## Parameter-Tabelle

| Parameter | Wert | Hinweis |
|-----------|------|---------|
| Modell | `nova-3` | Deepgram Nova 3 |
| Sprache | `bs` | Bosnisch |
| Region | EU | `api.eu.deepgram.com`, nicht US-Default |
| keyterm | 9 Marken/BS-Wörter | siehe Liste oben |
| filler_words | `true` | |
| punctuate | `true` | |
| smart_format | `true` | in `build_deepgram_stt` |
| endpointing_ms | `300` | in `build_deepgram_stt` |
| vad_events | `true` | explizit in `build_deepgram_stt` |
| replace | aus `deepgram-replace.json` | `./scripts/replace.sh` |
| extra_keyterms | optional | `build_session(extra_keyterms=[...])` erweitert KEYTERMS |

## Empfohlene & verfügbare Features für Voice Agents

Nova-3 + Sprache `bs` (Bosnisch) unterstützt diese Optionen laut [LiveKit Deepgram STT](https://docs.livekit.io/agents/models/stt/deepgram/) und Deepgram Nova-3. Für Live-Voice-Agents sinnvoll:

| Feature | Plugin-Parameter | Empfehlung | Kurz erklärt | Ist-Stand Amina |
|---------|------------------|------------|--------------|-----------------|
| Find & Replace | `replace={"…": "…"}` | z. B. `{"flaširana": "flasirana"}` | STT-Text normalisieren, bevor LLM/TTS | **gesetzt** (JSON + `replace.sh`) |
| Smart Format | `smart_format=True` | `true` | Zahlen, Datum, Währung, URLs lesbar formatieren | **gesetzt** |
| Endpointing | `endpointing_ms=300` | `300` (ms) | Stille-Dauer bis „Turn fertig“ — weniger Fragmentierung als Default 25 ms | **gesetzt** |
| Keyterm Prompting | `keyterm=[...]` | 9 Marken/BS-Wörter | Begriffe gezielt boosten (Nova-3) | gesetzt |
| Punctuation | `punctuate=True` | `true` | Satzzeichen + Großschreibung im Transkript | gesetzt |
| Speech Started | `vad_events=True` | `true` | `SpeechStarted`-Events bei Sprachbeginn (VAD) | **gesetzt** |

**Hinweise**

- Sprache **`bs` fest** — nicht `multi` (Nova-3 kann `multi`, wir nutzen Bosnisch-Verkauf).
- **EU-Residenz:** `base_url="https://api.eu.deepgram.com/v1/listen"` — nicht US-Default `api.deepgram.com`.
- `endpointing_ms` im LiveKit-Plugin entspricht Deepgram-API `endpointing` (Millisekunden).
- `replace`: Plugin als Dict `{"find": "replace"}`; bei Inference `extra_kwargs` alternativ `"find:replace"` als String.
- `vad_events`: LiveKit-Plugin default `true`; bei Inference-Doku oft `false` — für Voice Agents explizit `true` setzen.
- `filler_words=True` (bereits gesetzt) bleibt sinnvoll für Turn-Detector und natürliche Transkripte.

### Empfohlene Plugin-Konfiguration (Ziel)

```python
stt = deepgram.STT(
    model="nova-3",
    language="bs",
    keyterm=[
        "Aquaphor", "Smile", "Firmira", "Amina",
        "bokal", "pouzeće", "flaširana", "slavina", "kamenac",
    ],
    filler_words=True,
    punctuate=True,
    smart_format=True,
    endpointing_ms=300,
    vad_events=True,
    replace={
        "flaširana": "flasirana",  # Beispiel — Map nach Bedarf erweitern
    },
    base_url="https://api.eu.deepgram.com/v1/listen",
)
```

## Weitere Defaults des Plugins

- Kein `diarize`, `multichannel` explizit
- Kein eigenes `interim_results`-Override im Code (`true` = Plugin-Default)
- Inference-Pfad nicht genutzt — **Plugin + eigener EU-Key**

## Geplant (Plan v2, noch nicht im Code)

- TurnDetector-Schwelle über `AMINA_TURN_BS_THRESHOLD` (Task 3 im Plan)
- Datei `src/amina/turns.py` existiert noch nicht
