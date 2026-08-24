# Amina v2 Production-Ready Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.  
> **Nicht starten** ohne User-Satz **so bauen**. Kein Cloud-Deploy ohne extra OK.

**Goal:** Eine produktionsreife Cloud-Amina (`amina-soniox-v2`): wartet auf Abheben, spricht menschlich, verkauft (Produkt in Satz 1, weiches Nein ≠ Tschüss, hört zu), Wissen aus einer Faktenkarte, Langfuse und eu-central **wirklich** verdrahtet — nicht nur auf Papier.

**Architecture:** Ein Agent, ein Prompt (Markdown-Gerüst). Technik bleibt `build_session()` in `src/amina/agent_soniox.py`. Verkaufstext nur `prompts_soniox.py`. Outbound: erst SIP-Teilnehmer da, dann Hallo — kein `sleep`. TurnDetector **bleibt an** (Audio-Modell funktioniert; Bosnisch fehlt nur in der Schwellen-Liste). Wissen = eine Markdown-Karte, kein RAG. Langfuse OTLP nach offizieller LiveKit-Doku + Secrets **in Cloud**. Region: existierender Agent ist schon `eu-central`; Config/URL/Prozess so festhalten, dass der nächste Deploy nicht US wird.

**Tech Stack:** LiveKit Agents 1.6, Cloud project `aai`, agent `CA_J8AZ7K6yJ5o3`, Deepgram nova-3 `bs` EU, Inference `openai/gpt-4.1` Azure, Soniox `tts-rt-v2` Nina 0.9 EU-WS, Langfuse `cloud.langfuse.com` OTLP, pytest + `session.run` Judge.

---

## Korrekturen (warum der alte Text falsch war)

### TurnDetector — er **funktioniert**

Ich habe das zu negativ gesagt. Offizielle Docs (`/agents/logic/turns/turn-detector`, 24.08.2026):

- `inference.TurnDetector()` ist ein **Audio-Modell**: Tonfall, Pause, Rhythmus + Inhalt. Braucht **kein** Transkript.
- 14 Sprachen haben eine **eigene Schwelle** (`unlikely_threshold`). Bosnisch (`bs`) ist **nicht** in der Liste.
- Docs wörtlich: *Unmapped languages keep the calibrated default for the active model.*
- STT `language="bs"` bleibt. Detector nutzt dann den **Default**, nicht „Englisch kaputt“.
- Cloud: Default-Version **`v1`** (Inference). Nicht abschalten.

**Was wir tun:** anlassen. Optional etwas geduldiger (`min_delay` 0.5–0.8, oder `unlikely_threshold` etwas höher), **wenn** sie dich abschneidet. Nicht „bosnisch geht nicht“.

### Langfuse OTLP — Code ja, Produktion nicht fertig

Lokal in `.env.local` (Namen geprüft, keine Werte): `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_BASE_URL` = **SET**.  
Code: `src/amina/telemetry.py` entspricht fast der LiveKit-Doku (`/deploy/observability/tracing`).

Lücken:

| Papier | Ist |
|---|---|
| „OTLP ist konfiguriert“ | Nur lokal Keys. Cloud-Secrets **nicht** in diesem Plan verifiziert (`lk agent update --secrets-file` nie als Pflichtschritt belegt) |
| Docs: fehlende Keys = **Fehler** | Unser Code = **still None** — Cloud ohne Secrets = kein Trace, niemand merkt es |
| Test | nur `test_langfuse_noop_without_keys` |
| Call 07:13 war in Langfuse | STT-Text leer, keine Scores — Observability halb |
| Keys standen im Chat | **rotieren** vor neuem Upload |

### eu-central — Agent ja, Repeatable-Config nein

`lk agent list --project aai` (24.08. 09:22 CEST):

| ID | Name | Region |
|---|---|---|
| `CA_J8AZ7K6yJ5o3` | `amina-soniox-v2` | **eu-central** (echt) |
| 3 leere | — | **us-east** |

Lücken:

- `livekit.eu-central.toml` hat **kein** `region` — nur `id` + subdomain
- `.env.local`: `LK_AGENT_REGION` **MISSING**
- `LIVEKIT_URL` Host = `aai-j4shxmol.livekit.cloud` (global), nicht regional gepinnt
- Nächster `lk agent create` ohne Region landet leicht in **us-east** (die drei Leeren beweisen das)

---

## Annahmen

- User-Verkauf: Satz 1 = wer + **Bokal/Wasser**. Weiches Nein = weiter. Hart = DNC / „nicht anrufen“. Zuhören.
- Produktfakten: nur Belegbares. NSF **nicht** sagen, bis User eine Urkunde liefert.
- Alte Agenten (Fish, Soniox-alt, Template, Mujo) **nicht löschen**, nicht überschreiben.
- Cloud-Image `AEoJeTLGxy5A` (03:27 UTC) ist **älter** als Git `69eef9d` / `62b5cb7`. Telefon = alt, bis Deploy.
- SIP 401 / Identify: eigener Block, User muss Apply erlauben.
- Implementer committet lokal; **push + deploy nur nach User-OK**.

---

## Ansatz (Reihenfolge)

1. Wahrheit in Config (Langfuse Cloud-Secrets, Region-Doku, URL prüfen)  
2. Tests zuerst für Verkauf + Warten + Nein  
3. Code: Prompt, Tools, on_enter, Turn-Options  
4. Produktkarte (kurz)  
5. Lokal Console hören  
6. Deploy + Langfuse-Check **nur mit OK**  
7. Später: Krisp, Simulate, Address-Tasks — nicht in Welle 1

---

## Dateien

| Datei | Rolle |
|---|---|
| `src/amina/prompts_soniox.py` | Verkauf + Stimme (v2) |
| `src/amina/agent_soniox.py` | `build_session` locked |
| `src/amina/agent_soniox_v2.py` | Cloud-Entry, on_enter |
| `src/amina/agent.py` | Tools (`record_clear_no` Beschreibung) |
| `src/amina/policy.py` | hartes Ende nur bei hartem Nein |
| `src/amina/telemetry.py` | OTLP; Warnung wenn Cloud ohne Keys |
| `src/amina/product_facts.py` | kleine Karte als String (neu) |
| `docs/product/smile-karte.md` | SoT Wissen (neu) |
| `livekit.eu-central.toml` | Region-Kommentar + id |
| `docs/deploy.md` | Secrets + Region-Check |
| `tests/test_prompts_soniox.py` | Prompt-Regeln |
| `tests/test_policy.py` | Nein-Regeln |
| `tests/test_agent_live.py` | Judge: Produkt Satz 1, weiches Nein |
| `tests/test_telemetry.py` | Keys-Pfad ohne Secrets zu printen |
| `.env.example` | `LK_AGENT_REGION`, Secrets-Liste |
| `scripts/call-cloud-pick-agent.sh` | `wait_until_answered` wenn CLI das hat |

Nicht anfassen in Welle 1: Fish-Prompt, Mujo, Template-Texte, Ext 300/310, RAG.

---

### Task 1: Failing test — Opener nennt Produkt

**Objective:** Satz 1 muss Amina + Firmira + Bokal/Wasser enthalten.

**Files:**
- Test: `tests/test_prompts_soniox.py`
- Later: `src/amina/prompts_soniox.py`

**Step 1: Write failing test**

```python
def test_opener_names_product() -> None:
    from amina.prompts_soniox import OPENER_INSTRUCTIONS_SONIOX

    text = OPENER_INSTRUCTIONS_SONIOX.lower()
    assert "[warm]" in OPENER_INSTRUCTIONS_SONIOX
    assert "bokal" in text
    assert "firmir" in text
    assert "ami-na" not in text
    assert "ohne produkt" not in text
    assert "bez proizvoda" not in text
```

**Step 2:** `uv run pytest tests/test_prompts_soniox.py::test_opener_names_product -v`  
Expected: FAIL — `bez proizvoda` steht noch im Opener.

**Step 3:** Noch nicht implementieren in diesem Task, wenn TDD strikt — nächster Task ändert den Prompt. Hier nur Test committen wenn rot.

**Step 5: Commit**

```bash
git add tests/test_prompts_soniox.py
git commit -m "test: opener must name Smile bokal"
```

---

### Task 2: Opener + Systemprompt nach Fixplan

**Objective:** Prompt-Gerüst + Produkt in Satz 1 + weiches Nein + zuhören. Kurz halten.

**Files:**
- Modify: `src/amina/prompts_soniox.py`

**Step 1:** Bestehenden Test `test_opener_starts_with_warm_tag` anpassen (nicht mehr „ohne Produkt“).

**Step 3: Implementation** — ganze Datei ersetzen durch Markdown-Gerüst (LiveKit Prompting guide). Inhaltlich:

```python
SYSTEM_INSTRUCTIONS_SONIOX = """
Ti si Amina iz firme Firmira. Ženska osoba. Zoveš ljude u BiH.
Govoriš samo bosanski, ijekavica. Piši latinicom.

# Output
- Samo govor: bez markdown, lista, JSON, emoji.
- Jedna do tri kratke rečenice. Jedno pitanje.
- Prvo odgovori na POSLJEDNJE što je čovjek rekao, pa tek onda sljedeći korak.
- Brojeve izgovori riječima.

# Proizvod (samo ove činjenice; ništa ne izmišljaj)
- Aquaphor Smile bokal (nikad vrč, nikad boca), filter A5, do 350 litara, 2,9 l.
- Skida hlor, teške metale, rđu, fenole (proizvođač). Bez ugradnje.
- NSF / cijena / garancija / rok: reci samo ako stoji u kartici, inače „kolega javlja“.
- Plaćanje: pouzeće.

# Cilj
Čovjek treba odmah znati: voda / bokal. Onda slušaj. Prodaj ljubazno.

# Tok (jedan agent)
0 Čekaj da može reći halo.
1 Jedna linija: Amina, Firmira, bokal za vodu sa slavine + jedno kratko pitanje.
2 Slušaj. Ako kaže flaše — pričaj o flašama. Ne sljedeća stavka sa spiska.
3 Jedno pitanje o vodi (slavina / flaša / mix / filter).
4 Meko ne (ne, nemam vremena, razmislit ću, ne treba) = nije kraj. LAER.
5 Jedna korist vezana za NJIHOVE riječi. Mekano: da zabilježim jedan?
6 Narudžba samo poslije jasnog da. Jedno polje.
7 mark_dnc / „ne zovi više“ = odmah kraj.

# Einwand
- record_clear_no NIKAD za meko ne.
- mark_dnc samo: ne zovi, obriši broj, vrijeđanje.

# Tagovi Soniox (engleski)
Samo: [warm] [calm] [curious] [sincerely] [reassuringly] [softly] [pause]
Ne isti tag svaki put. [pause] samo na promjeni teme.
Zabranjeno: [happy] [laughs] crtice Ami-na, bosanski tagovi.

# Jezik
Zabranjeno HR: vrč boca tjedan tisuća tko što tvrtka …
Koristi: bokal flaša sedmica hiljada ko šta firma …
""".strip()

OPENER_INSTRUCTIONS_SONIOX = """
Pričekaj da čovjek može reći halo. Onda jedna kratka linija.
Prva riječ: [warm]
Jednom: Amina, Firmira, bokal za vodu. Jedno pitanje (imate li trenutak).
Bez cijene, bez narudžbe, bez druge predstave.
Primjer (smiješ skratiti):
[warm] Dobar dan, Amina iz Firmire — zovem zbog bokala za vodu, imate li trenutak?
Bez crtica. Bez drugih tagova.
""".strip()
```

**Step 4:** `uv run pytest tests/test_prompts_soniox.py -v` → PASS

**Step 5:** `git commit -m "fix: v2 prompt names product and listens"`

---

### Task 3: Tool-Beschreibungen — weiches Nein

**Objective:** LLM soll `record_clear_no` nicht bei „nein / keine Zeit“ feuern.

**Files:**
- Modify: `src/amina/agent.py` (docstring von `record_clear_no` und `record_permission`)
- Test: `tests/test_policy.py`

**Step 1: Test**

```python
def test_soft_phrases_are_not_hard_end() -> None:
    from amina.policy import is_hard_dnc, should_end_after_second_no

    assert not is_hard_dnc("ne")
    assert not is_hard_dnc("nemam vremena")
    assert not is_hard_dnc("ne treba mi")
    assert is_hard_dnc("ne zovi više")
    assert is_hard_dnc("obriši broj")
    assert not should_end_after_second_no(no_count=1)
    assert not should_end_after_second_no(no_count=2)
    assert should_end_after_second_no(no_count=3)
```

**Step 3:** In `policy.py`:

```python
_HARD_DNC = re.compile(
    r"(ne zovi|nemoj (me )?zvati|obriši|izbriši broj|do not call|dnc)",
    re.IGNORECASE,
)

def is_hard_dnc(user_text: str) -> bool:
    return bool(_HARD_DNC.search(user_text or ""))
```

`record_clear_no` docstring ersetzen:

```
Call ONLY for a hard refusal to be called again (ne zovi, obriši broj).
Never call for: ne, nemam vremena, razmislit ću, ne treba, skupo.
```

`record_permission`: „nema vremena“ → Rückruf anbieten, **nicht** Ende.

**Step 4:** `uv run pytest tests/test_policy.py -v` → PASS

**Step 5:** `git commit -m "fix: soft no is not DNC"`

---

### Task 4: on_enter — Sleep weg, auf Teilnehmer warten

**Objective:** Hallo erst wenn jemand **abgehoben** hat. Docs: outbound nicht während Klingeln begrüßen.

**Files:**
- Modify: `src/amina/agent_soniox_v2.py`
- Test: `tests/test_agent_soniox_static.py` (Assert: kein `asyncio.sleep` in on_enter)

**Step 1:**

```python
def test_v2_on_enter_has_no_fixed_sleep() -> None:
    import inspect
    from amina.agent_soniox_v2 import AminaSonioxV2Agent

    src = inspect.getsource(AminaSonioxV2Agent.on_enter)
    assert "asyncio.sleep" not in src
```

**Step 3:** `on_enter` so (kein Sleep):

```python
async def on_enter(self) -> None:
    # Outbound: CreateSIPParticipant oft vor Abheben. Warten auf remote.
    room = self.session.room
    if room is not None and not room.remote_participants:
        try:
            from livekit.agents import get_job_context

            ctx = get_job_context()
            await ctx.wait_for_participant()
        except RuntimeError:
            pass
    await self.session.generate_reply(instructions=OPENER_INSTRUCTIONS_SONIOX)
```

Zusätzlich Entry in `amina_soniox_v2_entry` **vor** `session.start` wenn Docs-Reihenfolge möglich:

```python
await ctx.connect()
# Optional: wait until SIP attr sip.callStatus == active — nur wenn im SDK vorhanden.
session = build_session()
await session.start(room=ctx.room, agent=AminaSonioxV2Agent())
```

**Nicht raten:** Vor dem Patch `lk docs` / MCP `wait_for_participant` + `sip.callStatus` nochmal lesen. Signatur 1:1 aus Docs.

**Step 4:** `uv run pytest tests/test_agent_soniox_static.py -v`

**Step 5:** `git commit -m "fix: greet after participant, drop sleep"`

---

### Task 5: TurnHandling — Docs, Detector an

**Objective:** Offizielle Tuning-Werte. TurnDetector bleibt.

**Files:**
- Modify: `src/amina/agent_soniox.py` `build_session`

**Step 3:** (Python-Sekunden laut Docs)

```python
turn_handling=TurnHandlingOptions(
    turn_detection=inference.TurnDetector(),  # v1 in Cloud; bs = default threshold, OK
    endpointing={"mode": "dynamic", "min_delay": 0.5, "max_delay": 3.0},
    interruption={"mode": "adaptive", "min_duration": 0.5, "min_words": 0},
),
min_consecutive_speech_delay=0.3,
```

`allow_interruptions=True` und `min_interruption_duration=0.45` **entfernen** (redundant / abweichend).

Wenn `TurnHandlingOptions` diese Kwargs in 1.6 nicht nimmt: `inspect.signature` + MCP `turn-handling-options`. Nicht erfinden.

**Step 4:** `uv run ruff check src/amina/agent_soniox.py && uv run pytest tests/test_template_v1.py tests/test_alans_mujo_v3.py -q`

**Step 5:** `git commit -m "fix: official turn-handling options, keep TurnDetector"`

---

### Task 6: Produktkarte ohne RAG

**Objective:** Fakten an einer Stelle. Prompt importiert Kurzform.

**Files:**
- Create: `docs/product/smile-karte.md`
- Create: `src/amina/product_facts.py`
- Test: `tests/test_product_facts.py`

**Step 1:**

```python
from amina.product_facts import SMILE_FACTS, forbidden_claims

def test_no_nsf_claim() -> None:
    assert "NSF" not in SMILE_FACTS
    assert "350" in SMILE_FACTS
    assert forbidden_claims("imamo NSF")  # True → darf nicht gesagt werden
```

**Step 3:** Karte nur aquaphor.com/pitchers/smile:

- Smile A5, 2,9 L, Filter A5 bis 350 L
- Chlor, Schwermetalle, Rost, Phenole, PFAS (Hersteller)
- kein Einbau
- Zeile: *NSF / BiH-Lizenz / Preis: unbelegt — nicht sagen*

`product_facts.py` = eine Konstante `SMILE_FACTS` (max ~800 Zeichen). Prompt hängt sie unter `# Proizvod` an **oder** Agent injiziert sie in `instructions`. Nicht beides pflegen — **nur** `product_facts.py` + Docs-Kopie.

**Step 5:** `git commit -m "docs: Smile fact card without NSF"`

---

### Task 7: Langfuse — Cloud wirklich an

**Objective:** Ohne Keys sichtbar; Cloud-Secrets Pflicht vor Deploy.

**Files:**
- Modify: `src/amina/telemetry.py`
- Modify: `tests/test_telemetry.py`
- Modify: `docs/deploy.md`, `.env.example`

**Step 1:**

```python
def test_setup_returns_none_without_keys(monkeypatch, caplog):
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_BASE_URL", raising=False)
    assert setup_langfuse() is None
```

**Step 3:** In `setup_langfuse` bei fehlenden Keys:

```python
import logging
log = logging.getLogger("amina.telemetry")
log.warning("Langfuse OTLP off — LANGFUSE_* missing")
return None
```

`docs/deploy.md` ergänzen (keine Secrets):

```bash
# 1. Keys rotieren in Langfuse UI (alte lagen im Chat)
# 2. Nur lokal in .env.local eintragen
# 3. In Cloud:
lk agent update --project aai --config livekit.eu-central.toml --secrets-file=.env.local
# 4. Nach Testanruf:
langfuse --env .env.local api traces list --limit 1
# Pflichtfelder im Trace: session id = room, agent=amina-soniox-v2, LLM+TTS spans
```

**Nicht** Keys in Git. User trägt neue Keys selbst ein.

**Step 5:** `git commit -m "fix: warn when Langfuse secrets missing"`

---

### Task 8: eu-central repeatable machen

**Objective:** Nächster Create/Deploy nicht us-east.

**Files:**
- Modify: `livekit.eu-central.toml`
- Modify: `.env.example`
- Modify: `docs/deploy.md`

**Step 3:** toml (nur Kommentar + bestehende Felder; Region nach Create **immutable**):

```toml
[project]
  subdomain = "aai-j4shxmol"

[agent]
  id = "CA_J8AZ7K6yJ5o3"
  # Region this id already has: eu-central. Do not lk agent create without --region eu-central.
```

`.env.example`:

```
# LIVEKIT_URL=wss://aai-j4shxmol.livekit.cloud
# LK_AGENT_REGION=eu-central
```

`docs/deploy.md` Check vor jedem Deploy:

```bash
lk agent list --project aai
# CA_J8AZ7K6yJ5o3 muss Regions=eu-central zeigen
# Niemals die drei us-east IDs für Amina nutzen
```

**Kein** neues Agent-Create.

**Step 5:** `git commit -m "docs: pin eu-central process for existing agent"`

---

### Task 9: LiveKit session.run Tests an neue Regeln

**Objective:** Judge prüft Produkt + weiches Nein (Docs Test-Framework).

**Files:**
- Modify: `tests/test_agent_live.py` — Klasse auf `AminaSonioxV2Agent` umstellen **oder** neue Datei `tests/test_agent_v2_live.py`

**Tests:**

1. `Halo?` → Judge: Bosnisch, Amina, Firmira, **bokal/voda**, eine Frage, kein Preis.  
2. `Nemam vremena.` → **kein** Tschüss, bietet 20 s oder Rückruf. Nicht `mark_dnc`.  
3. `Pijem samo flaširano.` → spricht über Flaschen/Geld, nicht Checkliste slavina.  
4. `Ne zovi više.` → höflich Ende, kein Pitch.

```bash
uv run pytest tests/test_agent_v2_live.py -v
```

Expected: braucht `LIVEKIT_*`. Lokal mit Keys grün.

**Step 5:** `git commit -m "test: v2 live judges for product and soft no"`

---

### Task 10: Suite + ruff (kein Deploy)

```bash
cd /Users/activi/Code/Projects/LiveKit
uv run pytest tests -q --ignore=tests/test_agent_live.py --ignore=tests/test_agent_v2_live.py
uv run ruff check src/amina tests
```

Expected: alle unit grün.

Lokal hören: Desktop `03-Amina-v2-Soniox`. Checkliste:

- Du schaffst Halo (Console: kein SIP — nur Länge/Ton prüfen)
- Satz 1 nennt Bokal
- „keine Zeit“ → bleibt
- „Flaschen“ → Flaschen

**Step 5:** `git commit` nur wenn noch uncommitted. **Kein push** ohne User.

---

### Task 11: Cloud — nur nach „deployen“

```bash
# Secrets zuerst (User hat neue Keys in .env.local)
lk agent update --project aai --config livekit.eu-central.toml --secrets-file=.env.local
lk agent deploy --project aai --config livekit.eu-central.toml
lk agent list --project aai
# Version != AEoJeTLGxy5A, Regions=eu-central
```

Dann ein Call. Langfuse: neuer Trace, `agent=amina-soniox-v2`.  
Wenn kein Trace: Secrets fehlen — **nicht** am Prompt drehen.

---

### Task 12 (blockiert): SIP Identify

Nicht im Code. User muss Apply erlauben.

- PJSIP Identify LiveKit-IPs → **nur Ext 330**
- TG400 nur **300**
- 310 nicht anfassen
- Erneut wählen; 401 weg?

---

## Später (nicht Welle 1)

| Item | Warum warten |
|---|---|
| Krisp `voice_isolation_telephony` | Kosten, A/B, kann Halo schlucken |
| `lk agent simulate` + Skill simulations | Beta; nach stabilem Prompt |
| GetAddressTask / GetPhoneNumberTask | Bestellung, wenn Verkauf hält |
| RAG / MCP-KB | ein Produkt = Karte reicht |
| Handoff-Wald | Docs: erst ein Agent |
| Fish/Soniox-alt löschen | User will Vergleich |
| us-east Leichen löschen | extra OK |
| Tempo 0.85 nur GSM | Headset war 0.9 gut |

---

## Risiken

- `wait_for_participant` in Console (kein SIP) kann hängen → `RuntimeError` / Timeout fangen.
- Cloud-Secrets überschreiben: `--secrets-file` muss **alle** nötigen Keys enthalten (Deepgram, Soniox, Langfuse, LiveKit). Datei nicht committen.
- Prompt vs User: `docs/PROJECT.md` sagt noch „kein Produkt im Open“ — **überholt**. Nicht zurückkopieren.
- TurnDetector Default-Schwelle bei `bs`: wenn sie abschneidet, `min_delay` hoch, nicht Detector aus.
- Öffentliches Git: keine Preise, keine Kundennummern, keine Keys.

---

## Offene Fragen an den User (vor Task 11)

1. Smile-Preis / BiH-Lizenz-URL für die Karte?  
2. Neue Langfuse-Keys selbst in `.env.local`?  
3. Identify 330 jetzt setzen?  
4. Nach lokalem Hörtest: **deployen ja/nein**?

---

## Done wenn

- Unit + ruff grün  
- Live-Judge: Produkt, weiches Nein, Flaschen-Bezug, DNC  
- `asyncio.sleep` weg aus v2 on_enter  
- TurnDetector an + Docs-Options  
- Nach Deploy: `lk` zeigt eu-central + neue Version; Langfuse hat Trace  
- User hört: Halo möglich, nicht Tschüss beim ersten Nein
