# Phonetik-Liste Amina (Fish)

Fish hat **kein** Aussprache-Wörterbuch. Fix = Umschreiben direkt vor TTS.

Zwei Schichten:

1. Diese statische Liste (immer, 0 Latenz)  
2. LLM nur für **neue** Kundennamen (unsicher)

## Anfassen

| Original | Gesprochen | Status |
|----------|------------|--------|
| Đenita / Đenite / Đeniti | Dženita / Dženite / Dženiti | verifiziert (đ→dž) |
| Sarajevo | Sara-je-vo | Regel; **nicht** Sara-ye-wo |
| Baščaršija | Baš-čar-ši-ja | Silben, č/š behalten |
| Aquaphor | A-kva-for | **Ohr nach Clone** |
| Firmira | Fir-mi-ra | **Ohr nach Clone** |
| Smile | Smaj-l | **Ohr nach Clone** |

Maschine: `phonetic-lexicon.json`.

## Nicht anfassen

č ć š ž. Wörter wie bokal, flaša, slavina, sedmica, hanyaće — normale bs-Wörter.

## Regeln für neue Namen

1. Nur ändern, wenn es falsch **klingt**  
2. `đ` → `dž`  
3. Lange Namen: Bindestriche, Buchstaben lassen  
4. Kein ch/sh statt č/š  
5. Fälle extra listen (Amina/Amine/Amini)

## Nach Clone-ID

Kurze Testdatei sprechen, Ohr: Aquaphor, Smile, Firmira, Amina, Sarajevo, eine Adresse mit č/š, eine Telefonnummer.
