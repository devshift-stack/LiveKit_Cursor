# HANDOVER — neue Session: LiveKit Amina weiterbauen

**Stand:** 24.08.2026 ~12:45 CEST  
**Du bist:** Hermes **main** (`default`) = Orchestrator + Planner. **Nicht** der User.  
**User:** nur Freigabe, Keys, Hörtest, Deploy-Ja, Identify/FreePBX.  
**Bauen:** erst nach User-Satz **so bauen**. **Deploy:** extra Satz.

Kein Secret in dieser Datei. Keys nur `.env.local` (nie committen, nie in den Chat).

---

## Sofort lesen (Reihenfolge)

1. Diese Datei  
2. `.hermes/plans/2026-08-24_101325-amina-v2-komplett.md` — **einziger Bau-Plan**  
3. `docs/FIXPLAN-AMINA-V2.md` — Verkaufsphasen  
4. `docs/RESEARCH.md` — Literatur (SPIN/LAER/Pink/Cialdini) — **nicht im Agent**  
5. `docs/LIVEKIT-BEST-PRACTICE.md`  
6. `docs/TURN-SCHWELLE.md`  
7. `AGENTEN.md` + `BOTLISTE.md`  
8. Code: `src/amina/prompts_soniox.py`, `agent_soniox_v2.py`, `agent_soniox.py`, `policy.py`

Alte Pläne nur in `arhiv/` — **nicht** ausführen.

Repo: `/Users/activi/Code/Projects/LiveKit`  
GitHub: https://github.com/devshift-stack/VoiceAgents · Branch `main`  
Desktop-Klicks: `~/Desktop/LiveKit Agents/`

---

## Worum es geht

Bosnische **Telefon-Telesales**: Persona **Amina**, Firma **Firmira**, Produkt **Aquaphor Smile Bokal** (nicht Vrč, nicht Flasche als Produktname).

Stack: LiveKit Cloud Projekt **`aai`**, eu-central · Deepgram Nova-3 `bs` **EU** · `openai/gpt-4.1` Azure Inference · Soniox **Nina** `tts-rt-v2` Speed **0.9** EU · optional Fish **Ela** nur lokal.

Nicht mischen: Dograh / Guarddograh / Ext **310**.

---

## Agenten (nicht überschreiben)

| Anzeige | `agent_name` | Datei | Cloud | Git-Tag |
|---|---|---|---|---|
| Fish | `amina` | `src/amina/agent.py` | nein | `v0.1-amina` / `v0.2.1-amina` |
| Soniox-alt | `amina-soniox` | `agent_soniox.py` | nein | `v0.2-soniox` |
| **Live** | **`amina-soniox-v2`** | `agent_soniox_v2.py` + `prompts_soniox.py` | **ja** `CA_J8AZ7K6yJ5o3` | Datei entsteht in `v0.2-soniox`; Code-Stand lokal **`v0.4-amina-soniox-v2`** = `69eef9d` |
| Template V1 | `template-v1` | `src/amina/template_v1/` | nein | `v0.3-template-v1` |
| Mujo | `alans-mujo-v3` | `src/alans_mujo_v3/` | nein | `v0.3-alans-mujo` |

**Name nie nur „v2“.** LiveKit-Name ist immer **`amina-soniox-v2`**.

Dockerfile CMD = nur `python -m amina.agent_soniox_v2 start`. Nicht auf Mujo/Template drehen.

---

## Drei Stände — nicht verwechseln

| Wo | Was du hörst |
|---|---|
| **Telefon / Cloud** | Image `AEoJeTLGxy5A`, Deploy **05:27 CEST**. ≈ Prompt/Turns von **`v0.2-soniox`**. Redet sofort, Nein oft = Tschüss |
| **Desktop `03`** | aktuelles `main` (v2-Code = `69eef9d` + spätere Docs) |
| **Desktop `03-…-v0.4`** | Worktree `/Users/activi/Code/Projects/LiveKit-v0.4-amina-soniox-v2` = Tag **`v0.4-amina-soniox-v2`**. Einmal `.venv` (87 Pakete) — normal |

User-Ohr: **v0.4 VAD/Reinreden schlechter** als Template. **Prompt v4 klingt komplett anders** als Template (stimmt — anderer Text).

---

## Was der User verbindlich will

- Menschlich, Top-Telesales, bosnisch **ijekavica**, schreiben **latinica** (hören darf ćirilica).  
- **Satz 1:** Amina + Firmira + **Bokal/Wasser** + ein Nutzen. Nicht 2–3 Sätze ohne Produkt.  
- Auf **letzte Kundenworte** eingehen — keine Checkliste.  
- **Weiches Nein** (keine Zeit, mal schauen, brauch ich nicht) = **weiterverkaufen**.  
- **Hartes Nein** / „nicht anrufen“ / DNC = Schluss. Nicht beim ersten ähnlichen „nein“.  
- Wissen: **eine Faktenkarte**, kein RAG zuerst. **Kein NSF** ohne Beleg (Smile-Seite hat keins). Preis/Lager/Garantie nicht erfinden.  
- Fish-Tags englisch (`[warm]` nicht `[toplo]`). Keine Bindestriche Ami-na auf Soniox.  
- Speed **0.9** lassen.  
- TurnDetector **an**. `bs` fehlt in der Werks-Liste ≠ aus. Geplant: eigene Zahl **0,55** Env, jederzeit drehbar.  
- Orchestrator = **Hermes main**, nicht User. Nicht 10er-Cluster, nicht 7 Roots.

Literatur (SPIN, LAER, Pink, Cialdini) = `docs/RESEARCH.md` + Fixplan. **In keinem laufenden Agenten vollständig.** Grund: User wollte Plan zuerst; **so bauen** für Welle 1 kam nicht. v4 = nur Teil (weiches Nein, kürzeres Hallo) — **ohne** Produkt in Satz 1.

---

## Was lokal in `69eef9d` / v4 schon drin ist (Cloud hat das nicht)

- `asyncio.sleep(1.8)` vor Opener — **falsch** für Outbound (Docs: nicht Sleep; SIP `--wait` **vor** Dispatch). User: VAD wirkt tot.  
- `allow_interruptions=True`, `min_interruption_duration=0.45` — User: schlechter als Template-Default.  
- `record_clear_no` / Policy Ende ab **3** (Fish+Soniox).  
- Neuer „Kämpfer“-Prompt — **ohne** Produkt im Opener (`Bez proizvoda` steht noch).

Template (`04`) = **alter** Prompt (wie Cloud) + **kein** Sleep. Deshalb redet sie anders und VAD fühlt sich besser an.  
Achtung: `04` auf heutigem `main` teilt `build_session()` → hat **auch** 0,45 s, wenn jemand `main` startet.

---

## Telefonie

Kette: LiveKit Cloud → **UDP** SIP → FreePBX `ari.activi.io` → Yeastar TG400 → GSM SIM `+387…8463`.

| Ext | Rolle (Soll, User früher) | Ist (User 24.08. später) |
|---|---|---|
| **300** | TG400 nur GSM | prüfen |
| **310** | Guarddograh — **nicht anfassen** | nicht anfassen |
| **330** | LiveKit-Auth, **nicht** am Yeastar | User: Yeastar hängt **auch an 330** |

Identify 330 (LiveKit-IPs → Ext) = **Mensch**, User sagte **stop**. 401 kam mit artificial From `+387…@….livekit.cloud`.

LiveKit-UI wählt **nicht**. Desktop `00-Cloud-Anruf.command`. Skript `scripts/call-cloud-pick-agent.sh` dispatch **vor** SIP `--wait` = **falsche Reihenfolge** (Agent schon beim Klingeln).

Media: **kein SRTP**.

---

## Desktop

`~/Desktop/LiveKit Agents/`

| Datei | Startet |
|---|---|
| `00-Cloud-Anruf.command` | Cloud wählen |
| `01` Fish | lokal Ela |
| `02` Soniox-alt | lokal |
| `03` | `main` v2 |
| `03-Amina-v2-Soniox-v0.4.command` | Tag v0.4 Worktree |
| `04` Template | lokal |
| `05` Mujo | lokal |

Logs Calls: `logs/calls/<timestamp>/`.

---

## Nächster Bau (nur nach **so bauen**)

Plan-Tasks 1→12 in **einer** Spur Code. Parallel nur Docs/Karte.

1. Tests: Opener **muss** `bokal` + Firmira enthalten.  
2. Prompt neu: Produkt Satz 1, Zuhören, weiches≠hartes Nein, Tag-Wechsel, Fixplan 0–7, Karten-Fakten.  
3. Turns: Detector an + `unlikely_threshold` `bs` 0,55 Env. Sleep **weg**. Interrupt nicht blind 0,45 — gegen Template/Ohr.  
4. Skript: SIP `--wait` **dann** Dispatch.  
5. Produktkarte `docs/product/smile-karte.md` — keine erfundenen Zertifikate.  
6. Tests `session.run` + Console-Ohr (User).  
7. Deploy nur nach extra OK. Identify extra OK.

Skills laden: `livekit-agents`, `livekit-voice-build`, `livekit-outbound-telephony`, `bosnian-voice-prompts`, `objection-handling`, `langfuse`. APIs nicht aus Gedächtnis — MCP `livekit-docs` / `lk docs`.

Verify: `uv run pytest tests -q --ignore=tests/test_agent_live.py` + ruff.

---

## Nicht tun

- Ohne **so bauen** Prompt/Turns/Skript/Cloud ändern  
- Alte Agenten löschen oder überschreiben  
- `.env.local` committen, Keys in Chat  
- NSF / Preis / BiH-Lizenz erfinden  
- TurnDetector aus  
- Sleep als Abheben-Lösung lassen  
- Ext 310 anfassen  
- Mujo deployen ohne extra OK  
- 7 Hermes-Roots / alle Profile gleichzeitig heiß  
- Kube3-1/2/3 als „neuen Hermes-Server“ leerziehen (das ist k3s)

---

## Team (bauen, nicht Telefon-Bots)

Orchestrator = **diese** Session (Hermes main).  
Architekt / Code / Docs / Review / dev-op / Research — siehe `BOTLISTE.md`.  
Arbeits-Bots **neu** bauen: `docs/SESSION-PROMPT-ARBEITSTEAM.md` — nur wenn User das will, **nicht** Amina-Code.

Mensch bleibt: Keys rotieren, Deploy, Identify, Hörtest.

---

## Start dieser Session

1. Plan + diese Datei gelesen?  
2. `git log -5 --oneline` + `lk agent list --project aai` — Cloud noch `AEoJeTLGxy5A`?  
3. User fragen: **so bauen** (Welle 1) oder nur prüfen?  
4. Nichts deployen, bis er es sagt.
