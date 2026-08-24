# LiveKit Best Practice (Stand Docs 24.08.2026)

Quellen: MCP `livekit-docs` — `outbound-calls`, `turns/tuning`, `turn-detector`, `agents-handoffs`, `workflows`, `tasks`, `noise-cancellation`.  
Skill `livekit-agents`: APIs nie aus Gedächtnis; Tests; Kontext klein halten.

---

## Cloud + Inference

- Agent nach **eu-central** (Region nach Create fest).
- LLM: LiveKit Inference `openai/gpt-4.1` `provider=azure` (EU-PII).
- STT/TTS: eigene EU-Hosts (Deepgram `api.eu.deepgram.com`, Soniox `wss://tts-rt.eu.soniox.com/tts-websocket`).
- Secrets: `.env.local` → `lk agent update --secrets-file`, nicht Git.

## Outbound-Anruf (wichtig)

Offizielle Reihenfolge:

1. Agent in den Raum **oder** Agent wählt selbst.
2. `CreateSIPParticipant` mit `wait_until_answered=True`.
3. `ctx.wait_for_participant` — Mensch ist **wirklich** da.
4. `session.start` **danach**.
5. Bei Outbound: **nicht** automatisch begrüßen — erst der Callee **oder** erst nach Answer eine **kurze** Begrüßung.

Docs wörtlich: *remove the initial greeting or place it behind an if … wait for the user to speak first when placing an outbound call.*

**Falsch:** `asyncio.sleep` in `on_enter` — läuft oft schon **während es klingelt**.

UI Cloud hat **keinen** Wählknopf. CLI/API: dispatch + SIP participant.

## Turns & Unterbrechen

Empfohlene Config (Docs *Turn-taking tuning*):

```python
TurnHandlingOptions(
    turn_detection=inference.TurnDetector(),
    endpointing={"mode": "fixed", "min_delay": 0.5, "max_delay": 3.0},
    interruption={"mode": "adaptive", "min_duration": 0.5, "min_words": 0},
)
```

| Symptom | Stellschraube |
|---|---|
| Schneidet den Menschen ab | `min_delay` hoch, `adaptive` |
| Kurzes „aha“ unterbricht sie | `adaptive`, `min_duration` 0,5 |
| Sie klebt Sätze aneinander | `min_consecutive_speech_delay` 0,2–0,4 |
| Fühlt sich langsam an | preemptive LLM an (Default); nicht blindly preemptive TTS |

`allow_interruptions` Default = **True**. Extra True allein ändert wenig.

### TurnDetector und Bosnisch

Detector **funktioniert** (Audio: Ton, Pause, Rhythmus). Nicht abschalten.

14 Sprachen haben eine **Werks-Geduld-Zahl** (`unlikely_threshold`). **`bs` steht nicht in der Liste** → LiveKit nimmt den **Default**, nicht „aus“.

Wir setzen **unsere** Zahl (Scalar, weil Amina nur Bosnisch spricht). Höher = wartet länger. Jederzeit Env `AMINA_TURN_BS_THRESHOLD`. Kein neues Modell. Details: [TURN-SCHWELLE.md](TURN-SCHWELLE.md).

## Phasen: ein Agent vs Handoff vs Task

Docs *Workflows*: **erst ein Agent + Tools.** Teilen nur bei:

- Prompt zu dick (Modell wird schlecht)
- andere Tools/Rechte
- mehrstufige Datensammlung mit Korrektur

| Muster | Wann |
|---|---|
| Ein Agent | Amina-Verkauf **jetzt** |
| Task | Adresse/Telefon einsammeln |
| Handoff | andere Rolle (z. B. Billing) |
| TaskGroup | Bestellfelder mit Zurück |

Handoff = neuer Agent, neuer Prompt. Task = kurze Mission, Ergebnis zurück, Supervisor bleibt.

## Rauschen GSM

- Agent-seitig bevorzugt: `krisp.voice_isolation_telephony()` (**kostenpflichtig**).
- Oder `krisp_enabled` am SIP-Participant (nur NC-Modell).
- Tuning-Docs: SIP → Telephony-Modell, nicht Headset-QUAIL als Default.
- Erst A/B: kann leises Halo schlucken, kann falsches „Nein“ aus Rauschen senken.

## Tests

Skill: jedes Agent-Verhalten testen. Docs: Simulations + `session.run`.  
String-Asserts im Prompt reichen **nicht** als LiveKit-Test.

## Observability

- LiveKit Observability ≠ Langfuse. Amina-Traces: Projekt **LiveKit Aquaphore**, Keys aus `.env.local`.
- e2e = Ende User-Sprache bis sie spricht, nicht Summe der Teile.
