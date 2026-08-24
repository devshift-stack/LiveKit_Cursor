# Turn-Schwelle (Geduld-Zahl)

Stand: 24.08.2026. **Noch nicht im Code** — Einbau: Plan Task 0.

## In einem Satz

Eine **Zahl zwischen 0 und 1**. Höher = Amina wartet länger, bis sie redet. Jederzeit änderbar. **Kein** neues Sprachmodell.

## Drei Zustände

| | Was | Bosnisch-Zahl |
|---|---|---|
| Nur VAD | Nur Stille = „fertig“ | gibt es nicht |
| **Jetzt (Code)** | TurnDetector an, **Werks-Zahl** | fehlt → Default |
| **Geplant** | Dieselbe Technik + **unsere** Zahl | Start **0,55**, Env überschreibt |

Detector **bleibt an**. 14 Sprachen haben eine Werks-Zahl, `bs` nicht. Deshalb setzen **wir** eine.

## Ändern (nach Einbau)

`.env.local` / Cloud-Secret:

```
AMINA_TURN_BS_THRESHOLD=0.55
```

| Ohr | Neue Zahl |
|---|---|
| Schneidet dich ab | 0,60 … 0,70 |
| Tote Luft nach dir | 0,45 … 0,50 |

Ein Dreh pro Test. Worker neu starten / nach Deploy Secrets updaten.

Code-Ort (geplant): `src/amina/turns.py` → `TurnDetector(unlikely_threshold=…)`.
