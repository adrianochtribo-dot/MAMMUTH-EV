# DECISIONE ARCHITETTURALE — Metropoli in GEONODE / BORGOVIA

**Data:** 17 giugno 2026
**Stato:** DECISA — da implementare (non ancora a schema)
**Autore:** Leonardo Adriano Chelariu — KREATIO UNIVERSAL SYSTEM™ · Code 3620

---

## Il problema

Il modello attuale àncora ogni evento a un **comune** (codice ISTAT), e funziona perfettamente per i micro-territori tipo Sermoneta (ISTAT 059026). Ma per le metropoli "comune = territorio" non basta: Roma ha migliaia di eventi su quartieri che funzionano come città intere. Se Roma fosse un solo territorio_id, Trastevere, EUR e il Centro Storico finirebbero nello stesso sacco — perdendo l'hyper-local che è l'identità del progetto.

**Conclusione:** le metropoli hanno bisogno di un **livello sub-comunale**.

## Il nodo: Roma ha 4 suddivisioni parallele

| Suddivisione | Numero | Tipo | Pro | Contro |
|---|---|---|---|---|
| Municipi | 15 | amministrativa | ufficiali, con codice | troppo grossi (un Municipio = una città) |
| Toponomastica (rioni/quartieri/suburbi/zone agro) | 116 | storica | nomi reali che la gente usa | nessun codice ISTAT ufficiale |
| Zone urbanistiche | 155 | pianificazione | ufficiali, codice proprio, ognuna dentro un solo Municipio | numeri tecnici, nessuno li nomina parlando |
| Informale (Nord/Sud/Est/Ovest rispetto al GRA) | 4 | mercato/parlato | intuitiva | non ufficiale, non mappabile |

Esempio chiave: **Garbatella** è ufficialmente la "zona urbanistica 11C", sta nel quartiere toponomastico **Ostiense**, controllata dal **Municipio VIII**. Tre nomi diversi per lo stesso pezzo di città.

## La decisione

Doppio binario: **ancora tecnica** + **etichetta leggibile**.

- **Ancora tecnica = le 155 zone urbanistiche.** Ufficiali, codice proprio, e ogni zona è interamente contenuta in un solo Municipio → gerarchia pulita.
- **Etichetta utente = il nome toponomastico** (Garbatella, Trastevere, EUR). È quello che la gente cerca. Mappato sul codice della zona urbanistica.

L'utente cerca "Garbatella" e il sistema sa: zona urbanistica 11C, Municipio VIII, Comune Roma (058091).

## Gerarchia in GEONODE

Nazione → Regione → Città Metropolitana → Comune (Roma 058091) → Municipio (I–XV) → Zona urbanistica (155, ANCORA dell'evento) ↔ nome toponomastico (etichetta).

**BORGOVIA aggancia l'evento alla zona urbanistica, non al comune Roma intero.**

## Da costruire (prossima sessione)

1. Tabella `zone_urbane` collegata a `territori`. Campi: id, comune_id (FK), municipio, codice_zona_urbanistica, nome_toponomastico, tipo_toponomastico.
2. `eventi` deve poter puntare a `zona_urbana_id` oltre che a `territorio_id` (NULL per i comuni piccoli — Sermoneta non ne ha bisogno).
3. Mappatura nome toponomastico ↔ codice zona (Open Data Roma Capitale).

## Validità generale

Vale per ogni metropoli: Milano (88 NIL), Napoli (10 Municipalità). Ancora internazionale: EU LAU.

---

**Prossimo passo:** progettare lo schema `zone_urbane` con i dati reali di Roma davanti — a mente fresca, NON al buio.
