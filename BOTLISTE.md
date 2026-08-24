# Botliste + Struktur

Stand: **24.08.2026 10:30 CEST**. Zwei Ebenen, nicht vermischen.

1. **Telefon-Bots** = Stimme im Anruf (dieses Repo)  
2. **Arbeits-Bots** = Hermes-Profile, die den Plan bauen

SoT Plan: `.hermes/plans/2026-08-24_101325-amina-v2-komplett.md`

```
                    DU (Tor: so bauen / Keys / Deploy / Identify)
                                      |
                              Orchestrator
                         (dieser Chat / hermes-livekit)
                         /         |          \
              Spur 1 Amina                    Spur 2 Werkzeug
         /        |        \                      |
   Research   Builder    Docs                 agent-builder
   (lesen)    Prompt+    Anleitungen          MCP + Skill + Plugin
              Voice-Test
                    |
              Telefon-Bots (src/)
                    |
         nur Cloud: amina-soniox-v2
```

---

## 1. Telefon-Bots (LiveKit)

| Anzeige | `agent_name` | Datei | Stimme | Cloud | Desktop |
|---|---|---|---|---|---|
| Amina Fish | `amina` | `src/amina/agent.py` | Fish Ela | nein | `01` |
| Amina Soniox alt | `amina-soniox` | `src/amina/agent_soniox.py` | Nina, Fish-Prompt | nein | `02` |
| **Amina v2** | **`amina-soniox-v2`** | `agent_soniox_v2.py` + `prompts_soniox.py` | Nina 0,9 | **ja** `CA_J8AZ7K6yJ5o3` eu-central | `03` |
| Template V1 | `template-v1` | `src/amina/template_v1/` | Nina, locked stack | nein | `04` |
| Alans_mujo V3 | `alans-mujo-v3` | `src/alans_mujo_v3/` | Daniel | nein | `05` |

Live = **nur v2**. Andere nicht löschen.  
Wählen: Desktop `00` (jetzt: Dispatch **vor** Wait — Plan Task 5 dreht das).  
Registry-Zahlen: `AGENTEN.md` (`uv run python scripts/update-agent-registry.py`).

---

## 2. Arbeits-Bots (Hermes-Profile)

| Rolle im Plan | Profil / Wrapper | Tut | Tut nicht |
|---|---|---|---|
| **Orchestrator** | default / `hermes-livekit` | verteilt, prüft Plan | nicht 200 Zeilen Prompt allein |
| **Research** | `research` | Docs, SDK, SIP, Schwelle | kein Prompt, kein Deploy |
| **Builder** | `hermes-livekit` oder `prompting-salesteleagent` | Prompt, Turns, Skript, Tests, Console | kein MCP-Server |
| **Docs** | ein Agent (research oder default) | `docs/`, Karte, HANDOFF | kein `src/` außer Karten-String |
| **Werkzeug** | `agent-builder` | Skill + dünner MCP + optional Plugin | **kein** Amina-`src/` |
| **Tor** | **du** | so bauen, Keys, Hören, deployen, Identify 330 | — |

### Profile die es gibt — für **diesen** Plan nicht nötig

`barbares`, `dograh`, `hermesvoice`, `homer`, `marge`, `sommer`, `creative`, `dev-op`, `mlops`, `n8n-workflow`, `xai-voice-dograh`, `ki-voice-agent`

Die nicht in Spur 1/2 ziehen (zu viel, falscher Stack).

---

## 3. Zwei Spuren

| Spur | Wer | Ziel |
|---|---|---|
| **1 Amina** | Research → Builder → Docs → du | Plan Tasks 1–8, 11–12, dann 9/13/14 mit dir |
| **2 Werkzeug** | agent-builder | paralleles Skill/MCP/Plugin; blockiert Spur 1 nicht |

Nicht: zwei Builder in `agent_soniox.py`. Nicht: 10er-Cluster.

---

## 4. Reihenfolge

1. Du: **so bauen**  
2. Parallel: Spur 1 Code + Spur 1 Docs-Karte + Spur 2 Gerüst  
3. Review gegen den Komplett-Plan  
4. Du: lokal `03`, dann Keys, dann **deployen**  
5. Call-Skript neue Reihenfolge, Identify extra  

---

## 5. Dateien

| Datei | Inhalt |
|---|---|
| Diese | Botliste + Team |
| `AGENTEN.md` | nur Telefon-Bots aus `src/` |
| `docs/PLAN-AMINA-V2.md` | Plan-Stand |
| `docs/agents/` | ein Blatt pro Telefon-Bot |
| `arhiv/` | alte Pläne |
