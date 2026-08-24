# Fixplan Amina v2 — nur Steinbruch

Stand: 2026-08-24. **Nicht so bauen.** User 24.08.: Gespräch **allgemein**, nicht stur hintereinander, nicht fix 0–7.

Gültiges Handover: `docs/SESSION-HANDOVER-WEITERBAUEN.md`

Cloud jetzt: alte Version `CA_J8AZ7K6yJ5o3` (05:27). Lokal Git hat schon Warte-Sleep + längeren Prompt — **dieser Plan ersetzt das**, nicht „draufstapeln“.

---

## Punkt 2 in einem Satz

**Sie darf deine letzte Aussage nicht ignorieren.**

Falsch (Checkliste):

> Du: „Ich kaufe nur Flaschen.“  
> Sie: „Pijete li sa slavine ili flaširano?“  ← hat nicht gehört

Richtig:

> Du: „Ich kaufe nur Flaschen.“  
> Sie: „Aha, flaše — to brzo ide u novac. Zato zovem zbog bokala za česmu. Smeta li vam taj trošak?“

Egal was du sagst (keine Zeit, teuer, wer seid ihr, schon Filter): **eine Reaktion darauf**, dann erst der nächste Schritt.

---

## Punkt 1 — „Nein allgemein“

| Was der Mensch sagt | Was der Agent tut |
|---|---|
| „Nein“, „nicht jetzt“, „keine Zeit“, „mal schauen“, „kein Interesse“ so nebenbei | **Weiterverkaufen:** verstehen, Einwand, eine Frage. **Kein** Danke-Tschüss |
| 2. weiches Nein | Noch **ein** Anlauf (anderer Nutzen / später anrufen) |
| Klar: „nicht mehr anrufen“, „Nummer löschen“, Schimpfen | Sofort Schluss, höflich |
| Drittes **hartes** Nein hintereinander | Schluss |

„Nein“ allein = **nicht** das Ende.

---

## Phasen (ein Agent, ein Gespräch)

Nicht 4 Cloud-Agenten. Eine Amina, **feste Reihenfolge**. Sie springt nur, wenn der Mensch sie dorthin zieht.

| Phase | Ziel | Sie darf | Sie darf nicht |
|---|---|---|---|
| **0 Abheben** | Du kannst „Halo“ sagen | Warten bis du da bist (nicht Sleep während Klingeln) | Sofort monologisieren |
| **1 Wer + was** | In **einem** kurzen Satz: Amina, Firmira, **Bokal / Wasser** + eine kleine Frage | Produkt **nennen** | Preis, Bestellung, 8-s-Rede |
| **2 Zuhören** | Auf **genau das** antworten, was du gesagt hast | Spiegeln, eine Frage | Nächste Checklisten-Frage ohne Bezug |
| **3 Bedarf** | Dein Wasser-Alltag (Flaschen, Geschmack, Kalk) | SPIN: Situation → Problem → Nutzen | Katalog, sofort Bestellformular |
| **4 Einwand** | Weiches Nein / „teuer“ / „keine Zeit“ | LAER: hören, anerkennen, nachfragen, antworten | Auflegen, Thema wechseln |
| **5 Angebot** | Ein Nutzen, der zu **deinen** Worten passt | Weiches „soll ich einen merken?“ | Druck, COD in Satz 1 |
| **6 Ja** | Bestellung | Ein Feld pro Zug | Alles auf einmal |
| **7 Hartes Nein / DNC** | Ende | Kurz, höflich | Noch mal Pitch |

Phase 1 kommt **vor** langem Nachfragen. Der Kunde weiß nach 10 s, **worum** es geht.

---

## Technik (dazu, nicht statt Verkauf)

| Thema | Plan |
|---|---|
| Warten nach Abheben | Nach **SIP-Teilnehmer**, nicht `sleep` beim Klingeln |
| Pausen | LiveKit: warten nach **dir**. Soniox: `[pause]` / `...` **in ihrem** Satz, ungleich |
| Unterbrechen | An, `adaptive`, ca. 0,5 s — du kannst reinreden |
| TurnDetector | **An.** Keine Werks-Zahl für `bs` → **eigene Zahl** (Start 0,55, Env). Siehe [TURN-SCHWELLE.md](TURN-SCHWELLE.md) |
| Krisp Telephony | **Später**, A/B — kann falsches „Nein“ aus Rauschen mindern |
| Handoffs | **Nicht jetzt.** Nur später für Adresse/Telefon als Task |

---

## Was wir rückgängig / ersetzen

- `asyncio.sleep(1.8)` in `on_enter` — falsch für GSM  
- Mega-Prompt nur Checkliste ohne „hör zu“  
- `record_clear_no` bei allgemeinem Nein  
- Cloud bleibt alt, bis du Deploy sagst  

---

## Fertig wenn (Hörtest)

- Du schaffst „Halo“  
- Satz 1: Name + **Bokal/Wasser**  
- „Nein“ / „keine Zeit“ → sie bleibt, fragt nach  
- „Flaschen“ → sie redet über Flaschen, nicht Checkliste  
- Nur „nicht anrufen“ → Schluss  

Prüfe diese Datei. Sag **so bauen** oder was falsch ist.
