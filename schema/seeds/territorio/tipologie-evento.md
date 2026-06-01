# Tassonomia Tipologie Evento

Classificazione ufficiale MAMMUTH•EVENTS per il micro-territorio.

## Livello 1 — Macro-categoria

### 🌾 SAGRA
Evento enogastronomico legato a un prodotto tipico locale.
- Ricorrenza: tipicamente annuale, stagionale
- Ente organizzatore: Pro Loco, Comune, associazione di categoria
- Esempi: Sagra della Porchetta (Ariccia), Sagra delle Fragole (Nemi)
- Campo identificativo: `tipo: sagra`

### ⚔️ PALIO / RIEVOCAZIONE STORICA
Competizione o rappresentazione con origine medievale/rinascimentale.
- Ricorrenza: annuale, legata a data storica
- Ente: Comune, contrade, associazioni storiche
- Esempi: Palio di Ronciglione, Giostra della Quintana
- Campo identificativo: `tipo: palio` | `tipo: rievocazione`

### ⛪ FESTA RELIGIOSA / PATRONALE
Celebrazione legata al santo patrono o al calendario liturgico.
- Ricorrenza: data fissa nel calendario liturgico
- Ente: Parrocchia, Diocesi, Confraternita, Pro Loco
- Sottotipi: processione / pellegrinaggio / sagra patronale
- Campo identificativo: `tipo: festa_religiosa`

### 🏘️ FESTA DI COMUNITÀ / PRO LOCO
Evento aggregativo senza origine storica specifica.
- Ricorrenza: variabile
- Ente: Pro Loco (UNPLI)
- Campo identificativo: `tipo: proloco`

### 🏛️ MERCATO STORICO / FIERA
Mercato con origine medievale o tradizionale.
- Campo identificativo: `tipo: fiera_storica`

---

## Regola di classificazione

Un evento può avere **tipo primario** + **tipo secondario**.
Esempio: Festa di S. Pietro ad Abbazia di Valvisciolo
→ `tipo_primario: festa_religiosa` | `tipo_secondario: proloco`
