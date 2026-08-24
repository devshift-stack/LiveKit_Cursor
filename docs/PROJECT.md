# Projekt: Amina — Aquaphor Smile BiH (LiveKit)

Quellen: nur **Daten** aus den zwei Dograh-Exporten PAS-5 und PAS-6.  
Nicht übernommen: Knotenanzahl, Graph, Webhook-Namen als Pflicht, Dograh-QA-JSON.

Beide Dateien sind verkaufstechnisch **gleich**. PAS-5 hat nur einen Extra-QA-Knoten. Das ist kein Verkaufsunterschied.

---

## 1. In einfachen Worten

Amina ruft Menschen in **Bosnien** an und spricht **bosnisch** am Telefon.

Sie verkauft den **Aquaphor Smile Bokal** — eine Kanne, die Leitungswasser filtert.

Sie klingt wie eine echte Verkäuferin: warm, kurz, eine Frage pro Zug.  
Sie verkauft **nicht** in den ersten Sekunden. Erst Erlaubnis, dann Situation, dann passendes Angebot, dann Bestellung nur wenn der Mensch ja sagt.

Zahlung: **pouzeće** — Bargeld bei Lieferung. Kein Online-Bezahlen im Call.

---

## 2. Fakten aus den Workflows (SoT fürs Produktgespräch)

| Feld | Wert |
|------|------|
| Persona | Amina, warm, klar, nicht steif |
| Firma | `business_name`, Fallback **Firmira** |
| Produkt | Aquaphor Smile **bokal** (nicht vrč, nicht boca) |
| Markt | Bosnien und Herzegowina, Telefon outbound |
| Sprache | Bosnisch, ijekavica, BiH-Wörter |
| Zahlung | Pouzeće bei Zustellung |
| CRM-Lead | `zoho_lead_id` kommt von außen |
| Anrufer | `customer_number` |
| Nach dem Call | n8n: Order-Gate, Handoff-Ticket, Cekura, Langfuse-Scores |

### Was Amina **nie** erfinden darf

Preis, Lieferzeit, Lager, Garantie, Chemie, „Sie haben zugestimmt“.  
Nummer-Herkunft: nur Wahrheit (öffentliches Verzeichnis), nie Fake-Opt-in.

### Bosnisch-Sperre (QA-Wortliste)

| Ja (bs-BA) | Nicht |
|------------|--------|
| bokal | vrč |
| šta | što |
| ko | tko |
| hiljada | tisuća |
| sedmica | tjedan |
| tačno / tačka | točno / točka |
| firma | tvrtka |
| sagovornik | sugovornik |
| saglasnost | suglasnost |
| flaša | boca |
| porodica | obitelj |
| januar / februar | siječanj / veljača |

Ijekavica halten: mlijeko, lijep, vrijeme, sljedeći, dvije.

Einmal vorstellen. Nie Name+Firma in jedem Zug wiederholen.

---

## 3. Verkaufsmethode (PAS als **Gespräch**, nicht als 17 Knoten)

PAS = Problem → Agitation → Solution. Das ist **Rhetorik**, kein LiveKit-Graph.

Ein guter Mensch am Telefon macht dasselbe in **vier Phasen**:

| Phase | Job | Verboten |
|-------|-----|----------|
| 1 Öffnen | Name+Firma (TTS). Dann warum + 20 Sekunden fragen | Produktkatalog, Preis, Bestellung |
| 2 Entdecken | Eine Frage: slavina / flaširana / mješovito / schon Filter | Pitch |
| 3 Binden | Ein Satz zum **ihrem** Schmerz, fragen ob stört | Bestellformular |
| 4 Lösen / schließen | 1–2 Sätze Nutzen **zum Schmerz** + weiches „soll ich einen notieren?“ | Druck nach klarem Nein |

Schmerz-Map (Daten, nicht Skript-Zwang):

| Wasser | Schmerz, den man **prüfen** darf |
|--------|----------------------------------|
| slavina | Geschmack, Kesselstein an Kessel/Gläsern |
| flaširana | Kosten über die Woche, Schleppen, Müll |
| mješovito | Was stört mehr? |
| schon Filter | Zufrieden? Oder einfacherer Bokal? |

Kein Schmerz / klar uninteressiert → höflich Ende. Kein Erzwingen.

### Bestellung (eigene Mini-Schleife, Tasks)

1. Einwilligung **bevor** Name/Adresse  
2. Ein Feld pro Zug: ime → adresa → telefon  
3. Jedes Feld zurücklesen; Telefon **Ziffer für Ziffer**, in Worten  
4. Finale Wiederholung: Produkt, Name, Adresa, Telefon, pouzeće  
5. Explizites Ja danach. Sonst keine Order.

Nebenwege (kein eigener 10-Knoten-Wald):

- Später → Termin vormittag/nachmittag + Nummer  
- Mensch → Name, Rückrufnummer, Kurznotiz (kein Live-Transfer)  
- Falsche Nummer / DNC → sofort Schluss, DNC blockiert alles

### Menschlich verkaufen (Top-Telesales)

- Spiegeln in **halber** Zeile, dann ein Schritt, **eine** Frage  
- „aha/mhm“ = weiter, nicht von vorn  
- Kaufsignale (Lieferung, wann kommt’s, für die Küche) → schließen, nicht weiter pitchen  
- Nach der Frage **schweigen**  
- Zweites klares Nein = Ende  
- Keine Maschinenzeilen: „Hoćete li kupiti?“, „Imate li još pitanja?“ als Füller, „Kako Vam mogu pomoći danas?“ auf Cold Call

---

## 4. LiveKit-Architektur (eigene Lösung)

Dograh-Graph **nicht** nachbauen. LiveKit-Doku: erst ein Agent; splitten nur bei Prompt-Aufblähung, anderen Tools, oder mehrstufiger Datensammlung.

Empfehlung:

```
Session
├── Agent Opener          (Erlaubnis, 15–20s)
│     handoff →
├── Agent Sales           (Entdecken + Schmerz + Angebot)
│     tools: none or FAQ-lookup
│     handoff / task →
├── TaskGroup Order       (Consent, Name, Adresse, Telefon, Readback)
│     tools: validate_address, submit_order_draft
└── Agent Wrap            (Callback / DNC / Handoff-Notiz)
```

Post-Call **außerhalb** der Stimme: `ctx.add_shutdown_callback` → n8n (Order-Gate, Ticket, Cekura, Langfuse).  
Kein QA-LLM im Live-Call.

Tests Pflicht: Permission, kein Early-Close, DNC, Readback, Language-Lock, zweites Nein.

---

## 5. Stimme & Technik (verifiziert)

### STT — Deepgram Nova-3 (gesetzt)

LiveKit: `deepgram/nova-3`, Sprache **`bs`** (in der Modellliste). Nicht `multi`.

| Einstellung | Wert | Warum |
|-------------|------|--------|
| language | `bs` | Bosnisch fest |
| keyterm | Aquaphor, Smile, Firmira, Amina, bokal, pouzeće, flaširana, slavina, kamenac | Marken/BS-Wörter |
| filler_words | true | aha/hm hören |
| punctuate | true | Sätze |
| EU-Host | `api.eu.deepgram.com` wenn Residenz | Default US |

Plugin statt nur Inference, wenn EU-Host oder eigener Key nötig.

### TTS — Fish Audio **s2.1-pro** (gesetzt)

LiveKit Inference listet s2.1-pro **ohne `bs`** und **ohne Custom-Clones**.  
Für Amina: **Fish-Plugin** + `FISH_API_KEY` + `d9b1befa09a34947b8c334268767abb6` (Ela, `bs`).

| Parameter | Empfehlung |
|-----------|------------|
| model | `s2.1-pro` |
| voice | `d9b1befa09a34947b8c334268767abb6` (Ela) |
| normalize | **false** (Docs: nur EN/ZH) |
| latency | `balanced` zuerst, A/B `low` |
| speed | ~0.95–1.05, Ohr |
| temperature | eher 0.5–0.7 (weniger Zufall) |

`normalize_loudness`: an.

### Fish-Tags — offizielle Liste (Studio-Hilfe, live)

Tags: klein, englisch, eckige Klammern. Werden **gespielt**, nicht gesprochen.  
**Unbekannte** Klammern kann Fish **vorlesen**. Deshalb keine Dograh-Tags erfinden.

| Zweck | Erlaubt | Nicht (aus altem WF) |
|-------|---------|----------------------|
| Stimmung, max. 1/Satz am Anfang | `[joyful]` `[excited]` `[soft]` `[tired]` `[nervous]` | `[happy]` `[calm]` `[empathetic]` `[serious]` |
| Pause | `[short pause]` `[pause]` `[long pause]` `[breath]` | — |
| Name/Wort betonen | `[emphasis]` direkt davor | — |
| Reaktion sparsam | `[sighing]` `[chuckling]` `[clears throat]` | Lachen im Close |

Dichte: ein Stimmungs-Tag pro Satz, nicht jeden Satz.

**Korrektur:** `[happy]` `[calm]` `[empathetic]` `[serious]` stehen in der **offiziellen** Emotions-Doku. Die frühere Warnung kam nur aus der engeren Studio-MCP-Liste. SoT: `docs/voice/FISH_TAGS.md`.

### Phonetik (Fish hat kein SSML/Lexikon)

Zwei Schichten, nicht nur Prompt:

1. **Statische Liste** vor TTS (Filter): bekannte Problemwörter  
2. Prompt: neue Namen silbenweise, nur wenn nötig

Regeln (verifiziert Fish+bs):

- `đ` → `dž` (Đenita → Dženita)  
- Lange Namen: Bindestriche `Baš-čar-ši-je`  
- **č ć š ž nicht** zu ch/sh machen  
- Marken prüfen: Aquaphor, Smile, Firmira, Amina, Sarajevo  

Zahlen/Preise in **Worten**. Telefon zifferweise.

LLM schreibt Tags + bosnischen Text. Filter ersetzt Lexikon zuletzt. Kein zweites LLM nur für Aussprache.

---

## 6. LLM-Empfehlung

Cascaded bleibt (STT→LLM→TTS). S2S ist für diesen Verkauf + Audit falsch.

| Rolle | Modell | Warum |
|-------|--------|--------|
| **Primär Gespräch** | **GPT-4.1** Azure/Foundry **Data Zone EU** | BKS + Tools; Inferenz in EU (Sweden/France/Germany) |
| Latenz-A/B | GPT-4.1 in **France Central** vs **Sweden Central** | Ohr + TTFT messen; nicht raten |
| Nicht live | US-Inference, Grok, Mini/Nano ohne A/B | US-Hop oder schwaches BKS |
| Gemma 4 31B | nur wenn LiveKit Inference **im selben eu-central DC** und bs-A/B ok | Default-Modell, Verkauf unbewiesen |

Stimme steuert das LLM: kurz, Tags nur aus der erlaubten Liste, Output TTS-fertig.

---

## 7. Skills / MCP / Tools für den Bau

Schon da und **nutzen**:

| Stück | Wofür |
|-------|--------|
| Skill `livekit-agents` | Handoffs, Tests, kein API-Raten |
| Skill `livekit-simulations` | Szenarien lokal |
| MCP `livekit-docs` / `lk docs` | aktuelle APIs |
| Skill `bosnian-voice-prompts` | gesprochener bs |
| Skill `dograh-human-conversation` | nicht maschinell |
| Skill `dograh-telesales-pacing` | kein Close in 10s |
| Skill `dograh-voice-opening-greeting` | Greeting vs. erster Zug |
| Skill `tts-pronunciation-correction` | Fish-Phonetik |
| Skill `balkan-voice-agent-stack` | bs-Stack |
| Skill `closing` / `objection-handling` | spät schließen |
| MCP `fish-audio` | Stimme, Tags, Probe |
| MCP `langfuse-*` | Scores nach Call |

Neu / klären:

| Stück | Warum |
|-------|--------|
| Fish-Plugin + Voice-ID | Custom bs, Inference hat kein bs/Clone |
| Deepgram-Plugin + EU-URL | Residenz + keyterm |
| LiveKit SIP Outbound-Trunk | Telefon |
| n8n-Webhooks als Shutdown-Tools | Order-Safety bleibt |

Nicht brauchen: llms-full.txt, Dograh-Node-Kopie, SSML-Optimizer (Fish = Klammern, kein Azure-SSML).

---

## 8. Entschieden (diese Session)

| Thema | Entscheidung |
|-------|----------------|
| Stimme | Fish Ela `d9b1befa09a34947b8c334268767abb6` **bleibt** |
| Zweiter TTS | Soniox **parallel A/B**, nur wenn Ohr ≈ Ela |
| Preis | Nur wenn der Kunde fragt |
| STT | Deepgram Nova-3 **nur** `https://api.eu.deepgram.com` |
| LLM | Azure/Foundry EU (France/Sweden), nicht US |
| LiveKit Agent | `eu-central` (Frankfurt) |

### LiveKit-Schalter „Inference region restriction = Enabled“

Gilt **nur** für **LiveKit Inference** (Modelle, die Cloud selbst durchreicht).  
Nicht für: Fish-Plugin, Deepgram mit eigener EU-URL, Soniox-Plugin, SIP, Recordings/Observability.

Also: **nicht** „alles von LiveKit bleibt in Europa“. Media geht weiter zum nächsten Cluster, außer Agent-Region + SIP-URL + Pin.  
Inference-Toggle: wenn ihr GPT/Deepgram **über Inference** nutzt, nur Modelle, die in der **Projekt-Datenregion** liegen. Fish aus Dograh/Plugin ist **außerhalb** dieses Schalters — passt zu eurer Messung (API-Origin USA, Edge Zagreb).

Fish so lassen: Edge-Hop Zagreb erklärt die gute Latenz trotz US-Rechnen.

### Soniox parallel (Preis bestätigt)

Offizielle Seite: TTS ~**0,70 USD / Stunde erzeugter Sprache** (`tts-rt-v2`).  
EU-Pin: `wss://tts-rt.eu.soniox.com/tts-websocket` — Default ohne das ist **US**.  
`language=bs`. Keine native bs-Stimme in der Liste — Maya/Mina oder Clone.  
BiH hat **latinica und ćirilica**; Amina schreibt **latinica**. Soniox-TTS liest **keine ćirilica** (API-Grenze, nicht „Bosnisch ist nur Latein“).  
Tags auf Englisch: `[happy]` `[calm]` `[pause]` `[laughs]` `[sighs]` `[breathy]` — wie Fish.  
Qualität vs Ela: **unbekannt**, nur Ohr-A/B.

### Fish Regionen

Standard-API nicht auf EU begrenzbar. Behalten wegen Latenz/Qualität. Detail: `docs/voice/TTS_EU.md`.

Noch offen: Preis KM, SIP-Carrier, n8n, Tonfall, Soniox-Clone **nach** Ela-Ohr.

**v2 (tag `v0.2-amina`):** Silben vor Fish (`prepare_tts_text` + Lexikon). Console: `scripts/start-amina-console.sh`.

Agent-Code: `src/amina/` — lokal `uv run python -m amina.agent console`. Kein Cloud-Deploy ohne Freigabe.

### LiveKit: Auto-Routing vs Pin (Docs live)

**Pin ist nicht nötig, damit Europa existiert.** Alle Pläne: globaler Endpoint routet zur **nächsten** Region (Last + Distanz). Bosnien landet oft schon in EU.

| Mechanik | Welcher Plan | Was passiert |
|----------|--------------|--------------|
| Default Realtime `*.livekit.cloud` | alle | nächster Cluster (kann EU **oder** bei Überlast woanders sein) |
| Agent nur in `eu-central` anlegen | alle mit Cloud-Agents | Rechenkern Frankfurt; Caller geht standardmäßig zum nächsten **Agent**-Deploy. Wenn der voll ist, **kann** ein anderer Kontinent drankommen |
| SIP global `*.sip.livekit.cloud` | alle | Inbound: Region des Trunk-Providers. Outbound: Region des API-Calls |
| SIP fest `*.eu.sip.livekit.cloud` | alle (nur andere URL) | erzwingt FR/DE für Telefonie — **kein** Scale-Plan |
| `destination_country=de` | alle | Outbound startet in Frankfurt |
| Protocol **Region-Pin `eu`** | **Scale+**, Support schaltet frei | sperrt Realtime **hart** auf EU; schaltet Auto-Failover in andere Kontinente aus |

Für BiH-Latenz: Agent **nur** `eu-central` + Deepgram EU + LLM EU + SIP `eu` / `destination_country=de`.  
Pin nur wenn **garantiert nie** US/Asien — nicht für „gibt es EU-Routing?“.

## 9. Dateien Stimme

- `docs/voice/FISH_TAGS.md`  
- `docs/voice/PHONETIC_LEXICON.md`  
- `docs/voice/phonetic-lexicon.json`  
- `docs/voice/TTS_EU.md`
