# Amina v2 — Schwellen-Zahl + aktueller Gesamtstand

> **For Hermes:** Use subagent-driven-development. Nicht starten ohne User-**so bauen**. Kein Deploy ohne extra OK.

**Goal:** Die TurnDetector-**Geduld-Zahl** fest einbauen (jederzeit änderbar) und denselben Plan wie bisher produktionsreif umsetzen.

**Architecture:** Ein Agent. Detector **bleibt an**. Bosnisch hat keine Werks-Schwelle → wir setzen **eine eigene Zahl** (kein neues Modell). Verkauf, Warten nach Abheben, Langfuse/Region wie im großen Plan.

**Tech Stack:** unverändert (LiveKit 1.6, `CA_J8AZ7K6yJ5o3` eu-central, nova-3 `bs`, GPT-4.1 Azure, Nina 0.9, Langfuse OTLP).

**SoT dieses Plans:** ersetzt die Unschärfe in `2026-08-24_092208-amina-v2-production.md` Task 5 (dort stand „optional Schwelle“). Die Zahl ist jetzt **Pflicht-Einbau**, klein und umkehrbar.

---

## Was die Zahl ist (für den Implementer)

Keine neue Sprache, kein Training.

```python
# src/amina/turns.py  (neu, eine Konstante)
# Höher = sie wartet länger (du darfst nachdenken).
# Niedriger = sie antwortet schneller (schneidet eher ab).
# LiveKit-Beispiel in Docs: 0.5. Start bei uns: 0.55 (etwas geduldiger — User wurde überschnitten).
TURN_BS_THRESHOLD = 0.55
```

Einbau (Docs `TurnDetector(unlikely_threshold=…)`):

```python
inference.TurnDetector(
    unlikely_threshold=float(os.getenv("AMINA_TURN_BS_THRESHOLD", str(TURN_BS_THRESHOLD)))
)
```

**Scalar**, nicht `{"bs": 0.55}`: Amina spricht nur Bosnisch. Scalar gilt für jede Sprache. Dict mit nur `bs` kann intern unmapped bleiben — nicht riskieren.

Ändern jederzeit: Env `AMINA_TURN_BS_THRESHOLD=0.65` in `.env.local` / Cloud-Secrets, Worker neu — **kein** Retrain.

---

### Task 0: Konstante + Test (TDD)

**Files:**
- Create: `src/amina/turns.py`
- Create: `tests/test_turns.py`
- Modify: `src/amina/agent_soniox.py` (`build_session`)
- Modify: `.env.example`

**Step 1: failing test**

```python
from amina.turns import TURN_BS_THRESHOLD, turn_detector_threshold

def test_default_threshold_is_between_zero_and_one() -> None:
    assert 0.0 < TURN_BS_THRESHOLD < 1.0

def test_env_overrides(monkeypatch) -> None:
    monkeypatch.setenv("AMINA_TURN_BS_THRESHOLD", "0.7")
    assert turn_detector_threshold() == 0.7
```

**Step 2:** `uv run pytest tests/test_turns.py -v` → FAIL (Modul fehlt)

**Step 3:**

```python
# src/amina/turns.py
from __future__ import annotations
import os

TURN_BS_THRESHOLD = 0.55

def turn_detector_threshold() -> float:
    raw = os.getenv("AMINA_TURN_BS_THRESHOLD")
    if raw is None or raw.strip() == "":
        return TURN_BS_THRESHOLD
    value = float(raw)
    if not 0.0 < value < 1.0:
        raise ValueError("AMINA_TURN_BS_THRESHOLD must be between 0 and 1")
    return value
```

In `build_session`:

```python
from amina.turns import turn_detector_threshold

turn_handling=TurnHandlingOptions(
    turn_detection=inference.TurnDetector(
        unlikely_threshold=turn_detector_threshold(),
    ),
    endpointing={"mode": "dynamic", "min_delay": 0.5, "max_delay": 3.0},
    interruption={"mode": "adaptive", "min_duration": 0.5, "min_words": 0},
),
```

`.env.example`:

```
# Geduld TurnDetector (0–1). Höher = wartet länger. Default 0.55
# AMINA_TURN_BS_THRESHOLD=0.55
```

**Step 4:** `uv run pytest tests/test_turns.py -v` → PASS  
`uv run ruff check src/amina/turns.py src/amina/agent_soniox.py`

**Step 5:** `git commit -m "feat: tunable TurnDetector threshold for Amina"`

---

Rest der Produktion = Datei  
`.hermes/plans/2026-08-24_092208-amina-v2-production.md`  
Tasks 1–4, 6–12 **unverändert**, Task 5 durch **Task 0 hier** ersetzt.

Reihenfolge nach „so bauen“:

0. Zahl (dieser Task)  
1–4. Prompt, Nein, on_enter, (Turns-Options stecken schon in Task 0)  
6. Produktkarte  
7–8. Langfuse + eu-central Doku  
9–10. Live-Tests + Suite  
11. Deploy nur mit OK  
12. SIP Identify blockiert

---

## Hör-Tuning der Zahl (nach Einbau, kein Code)

| Du hörst | Zahl |
|---|---|
| Sie fällt dir ins Wort | **hoch** (0.60 → 0.70) |
| Lange tote Luft nach dir | **runter** (0.50 → 0.45) |
| Passt | stehen lassen |

Ein Wert pro Test, nicht raten und drei Sachen gleichzeitig ändern.
