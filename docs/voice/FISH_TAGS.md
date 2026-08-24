# Fish Audio s2.1-pro — Tags für Amina

Zwei Quellen, nicht verwechseln:

| Quelle | Was sie sagt |
|--------|----------------|
| [docs.fish.audio Emotions](https://docs.fish.audio/developer-guide/core-features/emotions) | S2/`s2.1-pro`: `[eckige Klammern]`. Liste mit **64+** Tags inkl. **`[happy]` `[calm]` `[empathetic]`**. Zusätzlich **freie** Formulierungen (`[whispers sweetly]`). |
| Fish Studio MCP `studio_help` / tags | Engere Studio-Liste. Unbekannte Tokens „können vorgelesen werden“. |

**SoT für uns: Entwickler-Doku s2.1-pro**, nicht die Studio-Kurzliste.  
Die Warnung „alte Tags werden vorgelesen“ galt für die **Studio-Hilfe**, nicht für die API-Doku. `[happy]` `[calm]` `[empathetic]` `[serious]` sind **gültig**.

S1 = runde `(happy)` — **nicht** verwenden. Wir sind s2.1-pro = eckig.

---

## Offizielle Basis-Emotionen (Auszug, Docs)

`[happy]` `[sad]` `[angry]` `[excited]` `[calm]` `[nervous]` `[confident]` `[surprised]` `[satisfied]` `[delighted]` `[scared]` `[worried]` `[upset]` `[frustrated]` `[depressed]` `[empathetic]` `[embarrassed]` `[disgusted]` `[moved]` `[proud]` `[relaxed]` `[grateful]` `[curious]` `[sarcastic]`

Plus Advanced: `[hopeful]` `[determined]` `[confused]` `[disappointed]` … (volle Tabelle auf der Emotions-Seite).

## Ton / Effekte / Pausen (Docs)

| Zweck | Docs-Tag | Studio-Alias (auch ok) |
|-------|----------|-------------------------|
| leise | `[soft tone]` | `[soft]` |
| betonen | `[emphasis]` | gleich |
| kurz Pause | `[break]` | `[short pause]` / `[pause]` |
| lange Pause | `[long-break]` | `[long pause]` |
| flüstern | `[whispering]` | gleich |
| lachen | `[laughing]` `[chuckling]` | gleich |
| seufzen | `[sighing]` | gleich |
| räuspern | `[clear throat]` | `[clears throat]` |

s2.1-pro akzeptiert auch Freitext in Klammern. Trotzdem **kurze, bekannte** Tags — weniger Risiko.

---

## Amina am Telefon (empfohlen, nicht alles auf einmal)

| Phase | Tags |
|-------|------|
| Öffnen | `[happy]` oder `[joyful]` |
| Erklären / Wasser | `[calm]` `[relaxed]` |
| Mitgefühl | `[empathetic]` |
| Angebot | `[confident]` oder `[happy]` |
| Wichtig / Einwilligung | `[serious]` oder `[calm]` |
| Pause vor Frage | `[break]` |
| Name / Marke | `[emphasis]` davor |
| DNC / Nein | `[calm]` — kein Lachen |

Dichte: ein Stimmungs-Tag pro Satz, nicht jeden Satz taggen.

## Beispiele

```
[happy] Dobar dan.
Zovem zbog kratkog pitanja o vodi kod kuće. [break] Da li ste sada tu na trenutak?
```

```
[empathetic] Razumijem, flaše dodijaju. [break] Da li vam to smeta kroz sedmicu?
```

```
[confident] Baš zbog toga spominjem [emphasis] Aquaphor Smile bokal.
[break] Da li da zabilježim jedan za vašu adresu?
```

## LLM-Regel

Bosnisch. Nur eckige Tags. Ein primäres Gefühl pro Satz. Pausen `[break]`. Keine runden S1-Klammern. Keine langen Romane in Klammern.
