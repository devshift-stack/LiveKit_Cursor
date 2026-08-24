# Gesamtstand 24.08.2026 10:01 CEST

Nichts umgebaut in dieser Aktualisierung. Cloud unverändert: `CA_J8AZ7K6yJ5o3` Version `AEoJeTLGxy5A`.

## Was gilt

| Thema | Stand |
|---|---|
| Verkauf | Satz 1 = Amina + Firmira + **Bokal/Wasser**. Weiches Nein ≠ Tschüss. Zuhören. |
| Phasen | Ein Agent, 0–7 in [FIXPLAN-AMINA-V2.md](FIXPLAN-AMINA-V2.md) |
| Wissen | Eine Faktenkarte, **kein** RAG zuerst. NSF nicht sagen |
| TurnDetector | **An, funktioniert.** Keine `bs`-Werkszahl → wir bauen **eine eigene Zahl** (0,55, Env) |
| `sleep(1.8)` | Falsch (klingelt schon). Weg, `wait_for_participant` |
| Langfuse | Code + lokale Keys ja. Cloud-Secrets / Warnung / Scores **nicht fertig** |
| eu-central | Agent **ist** eu-central. toml/env halten es nicht fest |
| SIP | 401, Identify 330 ausstehend. 300=TG, 330=LiveKit-Auth |
| Deploy | Nur nach „deployen“. Telefon = altes Image |

## Pläne (bauen erst nach „so bauen“)

1. [Schwellen-Zahl + Reihenfolge](../.hermes/plans/2026-08-24_100125-amina-v2-threshold-und-stand.md) — **zuerst**  
2. [Produktion Tasks 1–12](../.hermes/plans/2026-08-24_092208-amina-v2-production.md)

Kurz erklärt: [TURN-SCHWELLE.md](TURN-SCHWELLE.md)
