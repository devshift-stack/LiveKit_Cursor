# Botliste + Struktur

Stand: **24.08.2026 10:45 CEST**. Zwei Ebenen, nicht vermischen.

Die ersten Rollen sind **nicht gestrichen** — sie waren nur umbenannt. Hier wieder mit denselben Namen:

| Früher gesagt | Ist dieselbe Rolle |
|---|---|
| Code / Builder | **Code** |
| Review | **Review** |
| Karte / Docs | **Karte/Docs** |
| Deploy | **Deploy** — vorbereiten = **dev-op**, Knopf = **du** |

SoT Plan: `.hermes/plans/2026-08-24_101325-amina-v2-komplett.md`

```
                         DU (so bauen, Keys, Hören, Deploy-Ja, Identify)
                                          |
                                   Orchestrator
                              /        |         \
                    Spur 1 Amina              Spur 2 Werkzeug
               /    |     |     \                   |
        Research  Code  Karte  Review          agent-builder
        (lesen)  Prompt  Docs  Plan-Check      MCP+Skill+Plugin
                  Test
                    |
                 dev-op  (Skript, Secrets, Deploy-Vorbereitung, SIP-Hilfe)
                    |
              Telefon-Bots — Cloud nur amina-soniox-v2
```

---

## 1. Telefon-Bots (LiveKit)

| Anzeige | `agent_name` | Datei | Stimme | Cloud | Desktop |
|---|---|---|---|---|---|
| Amina Fish | `amina` | `src/amina/agent.py` | Fish Ela | nein | `01` |
| Amina Soniox alt | `amina-soniox` | `src/amina/agent_soniox.py` | Nina, Fish-Prompt | nein | `02` |
| **Amina v2** | **`amina-soniox-v2`** | `agent_soniox_v2.py` + `prompts_soniox.py` | Nina 0,9 | **ja** `CA_J8AZ7K6yJ5o3` | `03` |
| Template V1 | `template-v1` | `src/amina/template_v1/` | Nina | nein | `04` |
| Alans_mujo V3 | `alans-mujo-v3` | `src/alans_mujo_v3/` | Daniel | nein | `05` |

Live = **nur v2**. Andere nicht löschen.  
`00-Cloud-Anruf`: Plan Task 5 dreht auf SIP-Wait **vor** Dispatch.

---

## 2. Arbeits-Bots (alle Rollen)

| Rolle | Profil | Arbeit | Nicht |
|---|---|---|---|
| **Orchestrator** | dieser Chat | verteilt, hält Plan | nicht alles selbst coden |
| **Research** | `research` | Docs/SDK lesen | kein Prompt, kein Deploy-Knopf |
| **Code** (Builder) | `hermes-livekit` | Prompt, Turns, Tests, Console | kein MCP-Server, kein `lk deploy` ohne dich |
| **Karte / Docs** | Docs-Agent | Produktkarte, Anleitungen, HANDOFF | kein Produktionscode außer Fakten-String |
| **Review** | Orchestrator nach jedem Commit | Diff gegen Plan, Tests, kein NSF/Sleep | nicht den Code selbst schreiben |
| **dev-op** | `dev-op` | Call-Skript-Reihenfolge, Secrets-Check, `lk agent list`, Deploy-Befehle vorbereiten, SIP/Identify **mit dir** | kein Prompt, kein „deployen“ ohne dein Ja |
| **Deploy** | **dev-op bereitet vor**, **du drückst ja** | Task 13 | Keys nicht in den Chat |
| **Werkzeug** | `agent-builder` | Skill + MCP + Plugin (Spur 2) | kein Amina-`src/` |
| **Tor** | **du** | so bauen, Keys, Hören, Deploy-Ja, Identify 330 | — |

**dev-op ist Pflicht** — nicht optional. Ohne ihn bleiben Skript, Secrets und Cloud-Check liegen.

---

## 3. Nicht in diesem Plan

`barbares`, `dograh`, `hermesvoice`, `homer`, `marge`, `sommer`, `creative`, `mlops`, `n8n-workflow`, `xai-voice-dograh`, `ki-voice-agent`

(`dev-op` steht **oben** — nicht in dieser Liste.)

---

## 4. Spuren

| Spur | Wer | Tasks |
|---|---|---|
| **1a Code** | Code | 1–5, 7–8, 11–12 |
| **1b Karte** | Karte/Docs | 6, Anleitungen |
| **1c Ops** | dev-op | Skript-Reihenfolge, 10 eu-central, 9 Secrets-Check |
| **1d Review** | Review | nach jedem Commit von 1a–1c |
| **2 Werkzeug** | agent-builder | parallel, blockiert 1 nicht |
| **Tor** | du + dev-op | 13 Deploy, 14 Identify |

Nicht zwei Codeschreiber in `agent_soniox.py`.

---

## 5. Reihenfolge

1. Du: **so bauen**  
2. Parallel: Code + Karte + dev-op (Skript) + Spur 2  
3. Review  
4. Du hörst `03`  
5. dev-op legt Deploy bereit → du sagst **deployen**  
6. Identify nur mit deinem Apply  

---

## 6. Dateien

| Datei | Inhalt |
|---|---|
| Diese | Botliste + Team |
| `AGENTEN.md` | nur Telefon-Bots |
| `docs/PLAN-AMINA-V2.md` | Plan-Stand |
| `arhiv/` | alte Pläne |
