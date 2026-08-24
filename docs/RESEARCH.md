# Recherche (Session 24.08.2026)

Nur belegte Punkte. Keine Secrets.

---

## A. Stimme / Soniox-Tags

Quelle: Soniox Docs *Emotion & tone*.

- Tags **Englisch**, vor dem bosnischen Satz.
- Pausen: `[pause]` (Standard, **feste** Länge), `[long pause]` selten.
- Kurze Atemzüge: `,` und `...` — **kein** Millisekunden-Wert.
- Tempo gesamt: Parameter `speed` (bei uns **0,9**), nicht Tags.
- Emotion: `[warm] [calm] [curious] [sincerely] [reassuringly] [softly]` — `[happy]/[laughs]` bei uns verboten (kann albern / vorgelesen wirken).
- Unbekannte Tags können **vorgelesen** werden.

**Schluss:** Tags = *wie sie einen Satz spricht*.  
LiveKit endpointing = *wann sie nach dir antwortet*.  
Beides nötig. Nur Tags → Metronom (User-Ohr).

Maya + `tts-rt-v2` = HTTP 400. v2-Stimmen: Nina (Amina), Daniel (Mujo).

---

## A2. TurnDetector-Schwelle (24.08. 10:01)

Quelle: LiveKit Docs *turn-detector*.

- Audio-Modell **arbeitet ohne** `bs` in der 14er-Liste (Default-Zahl).
- „bs bauen“ = **eine Zahl** `unlikely_threshold` (Scalar), Env `AMINA_TURN_BS_THRESHOLD`.
- Start geplant **0,55**. Höher = geduldiger. Jederzeit ändern.
- Nicht: neues Modell, nicht VAD ersetzen.

Siehe `docs/TURN-SCHWELLE.md`.

---

## B. Verkauf / Literatur

| Quelle | Nutzen hier |
|---|---|
| Rackham, *SPIN Selling* (1988) | Situation → Problem → Implikation → Nutzen. Zu früh Lösung = Einwände |
| LAER | Bei Nein: hören, anerkennen, nachfragen, antworten |
| Pink, *To Sell Is Human* | Dienen, auf ihre Worte |
| Cialdini | Kleines Ja; keine Fake-Dringlichkeit |
| Dograh-Skills human/pacing/opening | Spiegeln, 1 Frage, Open = wer+warum |

**User-Korrektur:** Produkt **nicht** drei Sätze verstecken. Satz 1: wer + Bokal/Wasser.  
Weiches Nein ≠ Schluss. 4/5–6 Calls endeten zu früh.

---

## C. Produkt Smile (aquaphor.com/pitchers/smile)

Belegt: A5, bis 350 L, Kanne 2,9 L, Chlor/Schwermetalle/Rost/Phenole/PFAS (Hersteller), AQUALEN, kein Einbau.

**Nicht** auf der Smile-Seite gefunden: NSF-Nummer, BiH-Zulassung, Preis.  
Nicht am Telefon erfinden. Nächste Datei: `docs/product/smile-karte.md` nach User-URL.

RAG: erst bei vielen SKUs/PDFs. Jetzt: eine Karte + 10 Prompt-Zeilen + optional Tool.

---

## D. Langfuse letzter Call

| Feld | Wert |
|---|---|
| Zeit | 24.08.2026 07:13 CEST |
| id | `73dd49f6f6d75a4ad1d949baa48e9be3` |
| session | `amina-out-20260824-071327` |
| Dauer | 53 s |
| Agent | amina-soniox-v2 / `CA_J8AZ7K6yJ5o3` |
| Scores | keine |
| STT-Text in LF | leer |

Zeitlinie: Agent spricht +10,6 s (8,5 s); User +11,7 s (0,26 s) **währenddessen**.

---

## E. SIP 401

Log: INVITE From `+387…@3dsfdizoiyr.sip.livekit.cloud`, Digest User 330, Asterisk **artificial** / Failed to authenticate.  
Fix: PJSIP Identify LiveKit-Netze → Ext 330.

---

## F. Desktop

`~/Desktop/LiveKit Agents/`

- `00-Cloud-Anruf` — Agent wählen, Nummer, Logs unter `logs/calls/`
- `01`–`05` — lokal Mikro (Fish / Soniox alt / v2 / Template / Mujo)
