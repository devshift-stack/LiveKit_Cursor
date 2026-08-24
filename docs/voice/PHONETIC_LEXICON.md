# Phonetik-Liste Amina (Fish)

Fish hat **kein** Aussprache-Wörterbuch und **keine** bosnischen Phonem-Tags.
Offiziell nur EN (CMU Arpabet), ZH (Pinyin), JA (Romaji) via `<|phoneme_start|>`.

Für `bs`: Text umschreiben, **bevor** er zu Fish geht. 0 Extra-Latenz.

## Live (Ohr 2026-08-24)

| Original | An Fish | Status |
|----------|---------|--------|
| Amina / Amine / Amini | Ami-na / Ami-ne / Ami-ni | Ohr ok |
| pitanje / pitanja / … | pita-nje / pita-nja | Ohr ok |
| trenutak / … | trenu-tak | Ohr ok |
| Đenita | Dženita | đ→dž |
| Aquaphor, Smile, Firmira | unverändert | keine ASCII-Bindestriche |

## Automatik (live)

`prepare_tts_text` macht **letzte Silbe** bei Wörtern mit **≥3 Vokalen**:
`Amina→Ami-na`, `pitanja→pita-nja`, `flaširanu→flašira-nu`.
1–2 Silben bleiben (`Dobar`, `vodi`). Marken in `do_not_touch` bleiben.
Lexikon-Liste gewinnt zuerst (đ→dž, Ohr-Fälle).

Nicht: LLM Hyphens schreiben. Nicht: IPA. Nicht: jedes Wort.

## Regeln

1. Buchstaben lassen (čćšž).
2. Silben-Bindestrich, keine IPA.
3. Kein `A-kva-for` / `Smaj-l` (sieht englisch aus).
4. Neue Wörter nur nach Ohr in `phonetic-lexicon.json`.
