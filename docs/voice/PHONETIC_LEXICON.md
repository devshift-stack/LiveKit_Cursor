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

## Automatik (aus, v2.1)

v2 hat **jedes** lange Wort zerlegt (`Reci-te`, `flašira-nu`) — klang schlechter als v1.
Live: **nur Lexikon** (Ami-na, pita-nja, trenu-tak, đ→dž). Rest wie v1.

## Regeln

1. Buchstaben lassen (čćšž).
2. Silben-Bindestrich, keine IPA.
3. Kein `A-kva-for` / `Smaj-l` (sieht englisch aus).
4. Neue Wörter nur nach Ohr in `phonetic-lexicon.json`.
