# Botliste — eine Gesamtliste

Stand: **24.08.2026 10:50 CEST**  
Plan: `.hermes/plans/2026-08-24_101325-amina-v2-komplett.md`

**Eine** Tabelle. Keine zweite Namensliste.

| # | Name (alle Synonyme) | Wer | Typ | Arbeit |
|---|---|---|---|---|
| 1 | **Orchestrator** | dieser Chat | Arbeit | verteilt, hält Plan |
| 2 | **Research** | `research` | Arbeit | Docs, SDK, SIP, Schwelle lesen |
| 3 | **Code** = Builder = **Prompt + Test** | `hermes-livekit` | Arbeit | Prompt, Turns, Tests, Console hören |
| 4 | **Karte / Docs** = **Anleitungen** | Docs-Agent | Arbeit | Produktkarte, HANDOFF, Anleitungen |
| 5 | **Review** | Orchestrator nach Commit | Arbeit | Diff gegen Plan, Tests, kein NSF/Sleep |
| 6 | **dev-op** | `dev-op` | Arbeit | Skript-Reihenfolge, Secrets-Check, Cloud-Liste, SIP-Hilfe |
| 7 | **Deploy** | dev-op bereitet vor, **du** sagst ja | Arbeit | Task 13 — kein Knopf ohne dich |
| 8 | **MCP / Skill / Plugin** | `agent-builder` | Arbeit Spur 2 | Werkzeug parallel, nicht Amina-`src/` |
| 9 | **Tor** | **du** | Mensch | so bauen, Keys, Hören, Deploy-Ja, Identify 330 |
| 10 | Amina Fish `amina` | `src/amina/agent.py` | Telefon | Ela, lokal `01`, nicht Cloud |
| 11 | Amina Soniox alt `amina-soniox` | `agent_soniox.py` | Telefon | Nina alt, `02`, nicht Cloud |
| 12 | **Amina v2** `amina-soniox-v2` | `agent_soniox_v2.py` | Telefon **Live** | Nina 0,9 · Cloud `CA_J8AZ7K6yJ5o3` · `03` |
| 13 | Template V1 `template-v1` | `src/amina/template_v1/` | Telefon | Klon, `04` |
| 14 | Alans_mujo V3 `alans-mujo-v3` | `src/alans_mujo_v3/` | Telefon | Daniel, `05`, nicht Cloud |

```
DU (9 Tor + 7 Deploy-Ja)
        |
   1 Orchestrator — 5 Review
      /        |         \
  2 Research  3 Code    4 Karte/Docs
              Prompt+Test  Anleitungen
         |
      6 dev-op —— 7 Deploy
         |
      8 agent-builder (MCP/Skill/Plugin)
         |
   10–14 Telefon   Live = nur 12
```

Nicht in dieser Liste: `barbares`, `dograh`, `hermesvoice`, `homer`, `marge`, `sommer`, `creative`, `mlops`, `n8n-workflow`, `xai-voice-dograh`, `ki-voice-agent`.

Zwei **Spuren** (Arbeit, nicht zwei Listen): Spur 1 = 2+3+4+6, dann 5; Spur 2 = 8. Nicht zwei Codeschreiber auf Zeile 3.
