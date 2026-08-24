# Arbeits-Bots — nur den Plan umsetzen

**Orchestrator + Planner = Hermes main (`default`). Nicht der User.**

Stand: **24.08.2026 11:15 CEST**  
Plan-SoT: `.hermes/plans/2026-08-24_101325-amina-v2-komplett.md`

| # | Rolle | Profil | Plan-Tasks |
|---|---|---|---|
| 1 | **Architekt** | `hermes-livekit` Struktur | 3, 5, 8 — *wie* (SIP, Turns, Session) |
| 2 | **Planner** | **Hermes main** (`default`) — nicht der User | Plan halten, nichts bauen |
| 3 | **Research** | `research` | lesen (Docs/SDK) vor 3, 5, 8 |
| 4 | **Verify** | Research + Architekt | Signaturen/`lk` (kein extra Mensch) |
| 5 | **Code** = Prompt + Test = Implement | `hermes-livekit` | **1–8, 11–12** |
| 6 | **Karte / Docs** = Anleitungen | Docs-Agent | **6**, 10 Texte |
| 7 | **Review** | nicht der Coder | nach jedem Commit |
| 8 | **dev-op** | `dev-op` | 5 Skript, **9** Secrets-Check, **10** Cloud, **13** vorbereiten |
| 9 | **MCP / Skill / Plugin** | `agent-builder` | **nicht** im Plan Welle 1 — nur Spur 2 |

---

## Gegen den Plan (24.08. geprüft)

| Plan-Task | Rolle | Urteil |
|---|---|---|
| 1–2 Prompt | 5 Code | da |
| 3 Schwelle/Turns | 1 + 5 | da |
| 4 Weiches Nein | 5 | da |
| 5 Abheben/Skript | 1 + 5 + 8 | da |
| 6 Produktkarte | 6 Docs | da |
| 7 Aussprache | 5 | da |
| 8 Auflegen | 1 + 5 | da |
| 9 Langfuse Keys | 8 bereitet vor | **Mensch muss Keys setzen** — kein Bot |
| 10 eu-central | 6 + 8 | da |
| 11–12 Tests/Hören | 5 + Review | Ohr-Test Console = Mensch |
| 13 Deploy | 8 vorbereiten | **Ja nur Mensch** |
| 14 Identify 330 | 8 hilft | **Apply nur Mensch** + FreePBX |

**Komplett fürs Bauen: ja.**  
**Komplett bis Telefon live: nein** — Keys, Deploy-Ja, Identify sind kein Bot.

### Zuviel

| | |
|---|---|
| Code und Implement als zwei Sitze | **eins** — jetzt Zeile 5 |
| **9 MCP/Skill/Plugin** | Welle 1 braucht ihn **nicht**. Nur wenn Spur 2 gewollt |

### Nicht fehlen (absichtlich raus)

Tor, Telefon-Bots — liegen in `AGENTEN.md`.
