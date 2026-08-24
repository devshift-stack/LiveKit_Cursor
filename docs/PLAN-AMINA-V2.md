# Gesamtstand 24.08.2026 10:13 CEST

Nichts am Agent-Code in dieser Aktualisierung. Cloud unverändert: `CA_J8AZ7K6yJ5o3` / `AEoJeTLGxy5A`.

## Ein Plan (SoT)

[`.hermes/plans/2026-08-24_101325-amina-v2-komplett.md`](../.hermes/plans/2026-08-24_101325-amina-v2-komplett.md)

Alte Pläne liegen in [`arhiv/`](../arhiv/) (nicht ausführen).

## Was der neue Plan zusätzlich richtig macht

| Vorher falsch/lückenhaft | Jetzt |
|---|---|
| `wait_for_participant` = abgehoben | **Nein.** SIP kann schon beim Klingeln im Raum sein |
| Sleep / Dispatch dann wählen | Skript: **`--wait` zuerst**, dann Dispatch |
| Outbound sofort reden | Docs + du: **Mensch zuerst**, nach 2,5 s Stille Opener |
| Task 5 vs Task 0 widerspruch | Eine Datei, Zahl = Task 3 |
| Aussprache / Auflegen / STT-Trace | eigene Tasks 7–9 |

## Weiter wie bisher

Verkauf Phasen 0–7 · weiches Nein · Faktenkarte · Detector an · Zahl 0,55 Env · Langfuse Secrets · eu-central Prozess · Identify 330 blockiert

Bauen erst nach **so bauen**. Deploy extra.
