# Arbeits-Bots — nur den Plan umsetzen

Stand: **24.08.2026 11:00 CEST**  
Auftrag: recherchieren, verifizieren, planen, erstellen, bauen, testen, implementieren.  
Plan-SoT: `.hermes/plans/2026-08-24_101325-amina-v2-komplett.md`

Telefon-Bots und „Tor = du“ stehen **nicht** in dieser Liste (`AGENTEN.md`).

| # | Rolle | Profil | Phase |
|---|---|---|---|
| 1 | **Architekt** | `hermes-livekit` (Struktur) | Reihenfolge SIP/Dispatch, Turns, Session, Dateischnitt — **bevor** viel Code |
| 2 | **Planner** | dieser Chat / Plan-Skill | Plan aktuell halten, Tasks schneiden, nichts bauen |
| 3 | **Research** | `research` | Docs, SDK, MCP lesen |
| 4 | **Verify** | `research` + Architekt | Signaturen, CLI, `lk`, Live-Fakten prüfen |
| 5 | **Code** = Prompt + Test | `hermes-livekit` | Prompt, Turns, Skript, Unit-/Live-Tests schreiben |
| 6 | **Implement** | dieselbe Spur wie Code | Tasks 1–8, 11–12 einbauen (TDD) |
| 7 | **Karte / Docs** = Anleitungen | Docs-Agent | Produktkarte, Anleitungen |
| 8 | **Review** | nach jedem Commit, nicht der Coder | Plan-Check, Tests, kein NSF/Sleep |
| 9 | **dev-op** | `dev-op` | Skript-Ops, Secrets-Check, Cloud-Liste, Deploy **vorbereiten** |
| 10 | **MCP / Skill / Plugin** | `agent-builder` | Spur 2 parallel |

```
2 Planner  ←→  1 Architekt
        \      /
         3 Research → 4 Verify
                |
         5/6 Code + Implement
         7 Docs          9 dev-op
                \        /
                 8 Review
         10 agent-builder (daneben)
```

Ohne **1+2** kein Bauen. Architekt legt fest *wie* (SDK). Planner legt fest *in welcher Reihenfolge*. Code baut nur das.
