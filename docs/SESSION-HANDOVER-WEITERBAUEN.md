# HANDOVER — neue Session: LiveKit Amina weiterbauen

**Stand:** 24.08.2026 ~13:00 CEST  
**Du bist:** Hermes **main** (`default`) = Orchestrator + Planner. **Nicht** der User.  
**User:** Freigabe, Keys, Hörtest, Deploy-Ja, Identify/FreePBX.  
**Bauen:** erst nach **so bauen**. **Deploy:** extra Satz.

Kein Secret. Keys nur `.env.local`.

Altes Handover (zu starrer 0–7-Ablauf) liegt in `arhiv/SESSION-HANDOVER-WEITERBAUEN-2026-08-24-starr.md`.

---

## Sofort lesen

1. Diese Datei  
2. `.hermes/plans/2026-08-24_101325-amina-v2-komplett.md` — Bau-Plan (Technik). Verkauf darin **nicht** als starre Phasen-Kette umsetzen.  
3. `docs/RESEARCH.md` — Ideen (SPIN/LAER/…), **kein** Pflicht-Skript  
4. `docs/LIVEKIT-BEST-PRACTICE.md`, `docs/TURN-SCHWELLE.md`  
5. `AGENTEN.md`, `BOTLISTE.md`  
6. Code: `prompts_soniox.py`, `agent_soniox_v2.py`, `agent_soniox.py`, `policy.py`

`docs/FIXPLAN-AMINA-V2.md` = alter Vorschlag mit 0–7. **Nicht** so bauen. Nur als Steinbruch.

Repo: `/Users/activi/Code/Projects/LiveKit`  
GitHub: https://github.com/devshift-stack/VoiceAgents · `main`  
Desktop: `~/Desktop/LiveKit Agents/`

---

## Worum

Bosnische Telefon-Telesales: **Amina**, Firma **Firmira**, **Aquaphor Smile Bokal**.

LiveKit Cloud **`aai`** eu-central · Deepgram Nova-3 `bs` EU · GPT-4.1 Azure · Soniox Nina `tts-rt-v2` **0.9** · Fish Ela nur lokal.

Nicht mischen: Dograh, Ext **310**.

---

## Gespräch — allgemein, nicht stur

Kein festes 0-1-2-3. Kein Abhaken. Wie ein Mensch am Telefon.

Immer gelten:

- **Früh klar worum:** Amina, Firmira, **Bokal / Wasser zu Hause**, ein Nutzen. Nicht lange ohne Produkt.  
- **Zuhören:** auf das, was der Mensch **gerade** gesagt hat.  
- **Weiches Nein** (keine Zeit, mal schauen, brauch ich nicht) = bleiben, eine Frage, nicht Tschüss.  
- **Hartes Nein** / nicht anrufen / DNC = Schluss.  
- Bosnisch ijekavica, schreiben latinica. Tags englisch, wechseln, keine Ami-na-Striche.  
- Nur **Karten-Fakten**. Nichts erfinden. Kein NSF ohne Beleg.  
- Speed 0.9. TurnDetector **an**. Geplant: Zahl 0,55 Env — kein neues Modell.

Literatur in RESEARCH = **Hilfen**, keine Reihenfolge zum Abspielen.

---

## Agenten (nicht überschreiben)

| Anzeige | `agent_name` | Cloud | Tag |
|---|---|---|---|
| Fish | `amina` | nein | `v0.1-amina` / `v0.2.1-amina` |
| Soniox-alt | `amina-soniox` | nein | `v0.2-soniox` |
| **Live** | **`amina-soniox-v2`** | **ja** `CA_J8AZ7K6yJ5o3` | lokal Code **`v0.4-amina-soniox-v2`** = `69eef9d` |
| Template | `template-v1` | nein | `v0.3-template-v1` |
| Mujo | `alans-mujo-v3` | nein | `v0.3-alans-mujo` |

Nie nur „v2“ sagen. Dockerfile CMD bleibt `python -m amina.agent_soniox_v2 start`.

---

## Drei Stände

| Wo | Stand |
|---|---|
| Telefon | Image `AEoJeTLGxy5A` 05:27 ≈ `v0.2-soniox`. Sofort reden, Nein oft Tschüss |
| Desktop `03` | `main` |
| `03-…-v0.4` | Worktree Tag v0.4. User: VAD schlechter, Prompt klingt anders (anderer Text) |

v4 hat Sleep 1,8 s (falsch), Interrupt 0,45 (User: schlechter als Template), Nein ab 3, Kämpfer-Prompt **ohne** Produkt im Opener.

Literatur **nirgends** fertig. Grund: kein **so bauen** für Welle 1.

---

## Telefonie

LiveKit → UDP SIP → FreePBX `ari.activi.io` → Yeastar TG400 → GSM.

| Ext | |
|---|---|
| 300 | GSM-Soll |
| 310 | Guarddograh — nicht anfassen |
| 330 | LiveKit-Auth. User: Yeastar hängt **auch** an 330 |

Identify = Mensch, User **stop**. UI wählt nicht. Skript dispatch vor `--wait` = falsch (redet beim Klingeln). Kein SRTP.

---

## Desktop

`00` Cloud · `01` Fish · `02` Soniox-alt · `03` main-v2 · `03-…-v0.4` Tag · `04` Template · `05` Mujo.  
Logs: `logs/calls/<timestamp>/`.

---

## Nächster Bau (nach **so bauen**)

Technik aus dem Komplett-Plan. Verkauf **locker**:

1. Opener-Test: Bokal + Firmira kommt vor — **kein** Pflicht-Skript danach.  
2. Prompt: früh Produkt, zuhören, weich≠hart, Tags wechseln, Karten-Fakten. **Keine** Phasen-Maschine 0–7.  
3. Turns: Detector + optionale Zahl 0,55. Sleep weg. 0,45 nicht blind — Ohr/Template.  
4. Skript: `--wait` dann Dispatch.  
5. Produktkarte, nichts erfinden.  
6. Tests + User hört.  
7. Deploy / Identify nur nach extra OK.

Skills: `livekit-agents`, `livekit-voice-build`, `livekit-outbound-telephony`, `bosnian-voice-prompts`, `langfuse`. APIs über MCP/`lk docs`.  
`pytest tests -q --ignore=tests/test_agent_live.py` + ruff.

---

## Nicht tun

Ohne **so bauen** Code/Cloud · Agenten löschen · Secrets · NSF erfinden · Detector aus · Sleep als Abheben · 310 · Mujo-Deploy ohne OK · 7 Roots · Kube3 leerziehen · Gespräch als starre 0–7-Kette bauen

---

## Team

Orchestrator = diese Session. Rollen: `BOTLISTE.md`. Arbeits-Bots: `SESSION-PROMPT-ARBEITSTEAM.md` nur wenn User will.

---

## Start

Lesen → `git log` + `lk agent list --project aai` → User: prüfen oder **so bauen**? → kein Deploy ohne Satz.
