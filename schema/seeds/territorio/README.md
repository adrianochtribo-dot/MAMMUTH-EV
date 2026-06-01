# TERRITORIO — Guida per sviluppatori

Questa sezione definisce il modello di validazione del **micro-territorio culturale** 
per MAMMUTH•EVENTS™ | KREATIO UNIVERSAL SYSTEM™ (Code 3620).

## Cosa trovi qui

| File | Scopo |
|------|-------|
| `tipologie-evento.md` | Tassonomia ufficiale degli eventi (sagra, palio, festa religiosa...) |
| `fonti-dati.md` | Fonti autoritative per reperire dati (ISTAT, proloco, diocesi...) |
| `validazione-schema.md` | Regole per validare un evento prima dell'inserimento |

## Relazione con i CSV

I file geografici di riferimento sono in `schema/seeds/`:
- `comuni_istat.csv` → codice ISTAT comune
- `codici_belfiore.csv` → codice catastale
- `cap.csv` → codice avviamento postale
- `province.csv` → province di riferimento

Ogni evento seed **deve** referenziare almeno `comune` + `codice_istat`.

## Perimetro iniziale

Fase 1: **Regione Lazio** — province RM, FR, LT, RI, VT.
Fase 2: espansione nazionale per cluster culturali omogenei.

## Principio guida

> "Non mappiamo eventi, diamo voce all'identità."
> Il micro-territorio è l'unità minima di cultura viva.
