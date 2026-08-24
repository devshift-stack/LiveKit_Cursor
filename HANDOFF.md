# HANDOVER — VoiceAgents / LiveKit Amina

**Für das nächste Team.** Stand 24.08.2026 **10:01** CEST.  
Kein Secret in dieser Datei. Keys nur `.env.local` (nicht im Git).

Repo lokal: `/Users/activi/Code/Projects/LiveKit`  
GitHub: https://github.com/devshift-stack/VoiceAgents  
Branch: `main` (Docs-Stand nach dieser Aktualisierung)

**Nächster Auftrag (nicht starten ohne User-„so bauen“):**  
1. Schwellen-Zahl: `.hermes/plans/2026-08-24_100125-amina-v2-threshold-und-stand.md`  
2. Rest Produktion: `.hermes/plans/2026-08-24_092208-amina-v2-production.md`  
Kurz: `docs/PLAN-AMINA-V2.md` + `docs/FIXPLAN-AMINA-V2.md` + `docs/TURN-SCHWELLE.md`

---

## 1. Worum geht es

Bosnische **Telefon-Telesales** für **Aquaphor Smile Bokal** (Firma **Firmira**), Persona **Amina**.  
Stack: LiveKit Cloud + Deepgram Nova-3 EU + GPT-4.1 Azure (Inference) + Soniox Nina (v2) **oder** Fish Ela (lokal).

Parallel: Familien-Demo **Dr Mujo** (nicht verkaufen).  
Dograh / Guarddograh / Ext 300+310 = **anderer Stack**, nicht mischen.

---

## 2. Agenten (SoT: `AGENTEN.md`)

| Anzeige | `agent_name` | Datei | Stimme | Cloud |
|---|---|---|---|---|
| Amina Fish | `amina` | `src/amina/agent.py` | Fish Ela | nein |
| Amina Soniox alt | `amina-soniox` | `src/amina/agent_soniox.py` | Nina, Fish-Prompt | nein |
| **Amina v2** | `amina-soniox-v2` | `src/amina/agent_soniox_v2.py` + `prompts_soniox.py` | Nina + Tags | **ja** `CA_J8AZ7K6yJ5o3` eu-central |
| Template V1 | `template-v1` | `src/amina/template_v1/` | locked `build_session` | nein |
| Alans_mujo V3 | `alans-mujo-v3` | `src/alans_mujo_v3/` | Daniel | nein |

Tags Git: `v0.2-soniox` (v2-Code 24.08. 05:17), `v0.3-template-v1`, `v0.3-alans-mujo`.

**Cloud-Image** deployed **05:27** CEST, Version `AEoJeTLGxy5A` — **eine** Version.  
Lokal danach: Sleep 1,8 s + Prompt-Umbau (`69eef9d`) — **nicht** redeployed. Cloud ≠ aktuelles Git.

Dockerfile `CMD` = nur `python -m amina.agent_soniox_v2 start`. Nicht umbiegen.

---

## 3. Was der User will (verbindlich)

- Menschlich, Top-Telesales, bosnisch (latinica schreiben, hören darf ćirilica).
- **Sofort klar worum:** Amina + Firmira + **Bokal/Wasser**, nicht 3 Sätze Checkliste ohne Produkt.
- **Weiches Nein** („keine Zeit“, „nein“, „mal schauen“) = **weiterverkaufen**, Einwand, zuhören.
- **Hartes Nein** nur: nicht anrufen / DNC / drittes hartes Nein.
- Auf **letzte Kundenaussage** eingehen (Flaschen → Geld/Flaschen, nicht nächste Liste).
- Nicht sofort ins Bestellformular. Nicht bei kleinstem Widerstand Tschüss.
- Produktfakten (Zertifikat, Liter, Filter) = **Karte**, nicht erfinden. NSF für Smile **nicht** belegt (Stand Recherche).
- RAG **nicht** als Erstes. Eine Markdown-Karte + kurzer Prompt.
- Teamarbeit ab hier: zu viel für einen Agenten allein.

---

## 4. Was live schiefging (Langfuse, Call 07:13 CEST)

Trace `73dd49f6f6d75a4ad1d949baa48e9be3`, Session `amina-out-20260824-071327`, Agent `amina-soniox-v2`, 53 s.

- Sie redete bei **+10,6 s** (8–11 s Monologe). User **0,3–0,9 s**, oft **während** sie sprach.
- User: kein Halo, zu schnell, nicht reinreden, Antwort fühlte sich langsam an.
- Gemessen: LLM ~0,9 s; e2e nach durchgekommenem Turn ~1,3 s. Problem = **sie redet zuerst und zu lange**, nicht 5 s Denkpause.
- Tags waren an (`[warm]`/`[curious]`), Ton trotzdem flach (immer gleicher Tag, gleiche Satzlänge).
- User: 4 von 5–6 Anrufen endeten mit Danke-Tschüss — `record_clear_no` zu empfindlich.

Früherer SIP-Versuch 06:48: **401** — LiveKit From `+387…@….livekit.cloud`, PBX kennt ihn nicht als Ext 330 (Identify fehlt).

---

## 5. Telefonie (kein Secret)

Kette: LiveKit Cloud → UDP SIP → FreePBX `ari.activi.io` → Yeastar TG400 → GSM SIM.

| Ext | Rolle |
|---|---|
| 300 | TG400 GSM (User-SoT) |
| 310 | Guarddograh — nicht anfassen |
| 320 | Hermes, frei |
| 330 | LiveKit-Auth (User: Login 330) |

Trunk Cloud: `ST_ity6jXX3KWMw` Name `LiveKit`, Number `+387671048463`, User **330**, UDP, SRTP aus.  
Dialplan GSM: historisch über 330 gesetzt; User-Tabelle sagt TG=300. **Vor nächstem Test live prüfen.**

Identify: LiveKit-IPs (`161.115…` kam im Log) der Ext **330** zuordnen. Nicht 300.

UI LiveKit hat **keinen** Wählknopf. Desktop: `00-Cloud-Anruf.command`. Logs: `logs/calls/<timestamp>/`.

---

## 6. Skills / MCP für das Team

| Skill | Wofür |
|---|---|
| `livekit-agents` | Denken, Tests, keine API aus Gedächtnis |
| `livekit-voice-build` | Projektpfad LiveKit, EU-Stack |
| `bosnian-livekit-template-v1` | Klon nur Prompt/Soul |
| `livekit-agent-from-brief` | Wizard: erst `clarify`, dann bauen |
| `dograh-human-conversation` | Spiegeln, nicht Roboter |
| `objection-handling` / `closing` | LAER, nicht Early-Close |
| `langfuse` | Traces, Route LiveKit ≠ voiceeu |

MCP: `livekit-docs` (APIs), `langfuse-livekit` (Amina), `soniox-docs`.  
CLI: `lk` Projekt `aai`. Langfuse: `langfuse --env .env.local api traces list`.

---

## 7. Dateien lesen (Reihenfolge)

1. `docs/PLAN-AMINA-V2.md`  
2. `docs/TURN-SCHWELLE.md`  
3. `docs/FIXPLAN-AMINA-V2.md`  
4. `docs/LIVEKIT-BEST-PRACTICE.md`  
5. `docs/RESEARCH.md`  
6. `docs/PROJECT.md` (Open ohne Produkt — **überholt**)  
7. `AGENTEN.md`  
8. Code: `prompts_soniox.py`, `agent_soniox_v2.py`, `agent_soniox.py`, `agent.py`

---

## 8. Nicht tun

- `.env.local` committen / Keys in Chat  
- Dockerfile-CMD auf Mujo/Template  
- Ext 300/310 als LiveKit-Auth  
- Gemma als Default  
- NSF/Preis/Garantie erfinden  
- Dograh-Graph 1:1 nachbauen  
- Cloud deployen ohne User-OK  
- `sleep(1.8)` als „Warten nach Abheben“ belassen  
- TurnDetector **abschalten** (er funktioniert; wir setzen nur eine Zahl)  

---

## 9. Offene Arbeit (Team)

1. **Geduld-Zahl** einbauen (`turns.py`, Start 0,55, Env) — Plan 10:01  
2. Fixplan: Phasen + weiches Nein + Zuhören + Produkt Satz 1  
3. Sleep ersetzen durch `wait_for_participant`  
4. `TurnHandlingOptions` laut Docs + unsere Schwelle  
5. Produktkarte — User liefert Zertifikat-URL  
6. Langfuse: Keys rotieren, Cloud-Secrets, Warnung wenn leer  
7. eu-central Prozess in toml/docs festhalten  
8. Identify 330 + Dialplan vs Ext 300  
9. Dann erst `lk agent deploy`  
10. Hörtest + Zahl ggf. drehen  

Owner: Team. User sagt **so bauen**.
