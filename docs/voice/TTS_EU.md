# TTS Europa-Pin vs Fish

Stand: offizielle Seiten 2026-08-24.

## Kann man Fish auf Europa begrenzen?

**Nein — nicht im normalen API.**

Belege:

| Check | Ergebnis |
|-------|----------|
| TTS-OpenAPI `POST /v1/tts` | nur `https://api.fish.audio` — **kein** Region-Header, kein EU-Host |
| Enterprise-FAQ | Speicher default **USA**. Inferenz-Edge default **USA + Tokio** |
| EU-Residenz | nur Enterprise / **Self-Host** (ab ~10k Setup + 10k/Monat) |
| „Auto-Routing“ | ihre GPU-Last über US/APAC — **kein** Schalter „nur EU“ |

Wer Ela (`d9b1befa09a34947b8c334268767abb6`) über den normalen Key nutzt, kann den Hop **nicht** auf EU festnageln.

---

## Alternativen: EU fest + bs + Preis + Qualität

Grobe Kosten pro **Stunde erzeugter Sprache** (Anbieter-Angaben, nicht 1:1 vergleichbar):

| Anbieter | EU fest? | Bosnisch | Preis (öffentlich) | Qualität vs Fish/Ela | LiveKit |
|----------|----------|----------|--------------------|----------------------|---------|
| **Azure Neural** `bs-BA-Vesna` / `Goran` | **Ja** — Region z. B. `germanywestcentral` | Ja, offizielle Stimmen | ~16 USD / 1M Zeichen | **günstiger/ähnlich**, aber **flacher** (kein StyleList) | Plugin `azure.TTS` |
| **Soniox TTS** | **Ja** — `wss://tts-rt.eu.soniox.com` + regionales Projekt/Key | Ja: `language=bs`. **Keine eigenen bs-Stimmen** — Katalogstimme oder Clone spricht bs. Input: **latinica** (API spricht keine ćirilica). In BiH sind beide Schriften üblich, Verkaufstext = latinica. | ~**0,70 USD / Stunde** Audio | unbekannt vs Ela — **Ohr-A/B** | LiveKit-Plugin |
| **ElevenLabs EU Residency** | **Ja** — `api.eu.residency.elevenlabs.io` + ZRM | multilingual, Clone | Credits; Business ~5 ct/min Extra; **EU = Enterprise** | nah an Fish (Clone+Emotion) | Plugin |
| **Cartesia Sonic** | GDPR ja; EU-Pin nicht als Self-Serve-URL belegt | **kein bs** auf der Sprachenliste (hr ja) | — | für BiH ungeeignet | Plugin |
| **Fish Self-Host** | Ja, in eurer VPC | Ela bleibt | Enterprise, nicht Fish-API-Preis | gleich | eigener Endpoint |
| Fish Cloud (jetzt) | **Nein** | Ela ja | 15 USD / 1M UTF-8-Bytes (~12 h Sprache) | Referenz | Plugin |

---

## Was das in einfachen Worten heißt

- **Billig + fest in Europa + echtes Bosnisch:** Azure Vesna in Frankfurt/GWC. Klingt solider, weniger „Mensch“ als Ela.  
- **Billiger als Fish + behauptet EU + bs:** Soniox. Erst hören, dann glauben.  
- **Nahe Fish-Qualität + EU-Schloss:** ElevenLabs Isolated EU. Teurer, Enterprise.  
- **Fish-Qualität 1:1 in EU:** nur Fish Self-Host, nicht der 15-USD-API-Tarif.

Es gibt **keine** Self-Serve-TTS, die gleichzeitig Ela-Niveau, Fish-Preis und harten EU-Pin hat.

---

## Empfehlung für Amina

1. **Latenz/EU hart:** Azure Vesna `@ germanywestcentral` als EU-Pfad (habt ihr schon auf voiceeu).  
2. **Qualität wie jetzt:** Fish Ela behalten und den US/Tokio-Hop **akzeptieren**, oder Fish Sales wegen EU-Edge fragen (schriftlich).  
3. **Mittelding zum Testen:** Soniox EU + bs, gleicher Text wie Ela, Ohr.

Nicht: Cartesia. Nicht: Google TTS (kein bs).
