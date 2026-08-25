# Amina v5 Soniox (`amina-soniox-v5`)

Lokaler Nachfolger von v2 mit **erweitertem Deepgram-STT** über `build_deepgram_stt()`:

- `smart_format`, `endpointing_ms=300`, `vad_events`
- Replace-Map: `docs/voice/deepgram-replace.json` (pflegen: `./scripts/replace.sh`)

v2 (`amina-soniox-v2`) bleibt **Cloud-Default** (Dockerfile CMD) bis expliziter Deploy-Wechsel.

- Datei: `src/amina/agent_soniox_v5.py`
- Prompt: `src/amina/prompts_soniox.py` (wie v2)
- Stack: `build_session()` in `agent_soniox.py`
- TTS: Nina, tts-rt-v2, 0.9, EU-WS
- Start lokal: `./scripts/start-amina-soniox-v5-console.sh`
- Cloud: **noch nicht** deployed
