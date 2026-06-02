[CONTRIBUTING.md](https://github.com/user-attachments/files/28523275/CONTRIBUTING.md)
# Contributing to MAMMUTH•EV™

> **KREATIO UNIVERSAL SYSTEM™ · Code 3620**
> *Where Communities Come Alive*

---

## Benvenuto, Developer

Grazie per il tuo interesse nel contribuire a MAMMUTH•EV™. Questo documento spiega le regole e le procedure per contribuire al progetto in modo coerente con l'architettura del **KREATIO UNIVERSAL SYSTEM™**.

> ⚠️ **Prima di contribuire**, leggi il [Developer Portal](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/developer-index.html) per comprendere l'architettura del sistema.

---

## Principi Non Negoziabili

Ogni contributo deve rispettare i pilastri del sistema:

- **ElppaK•Clean™** — codice pulito, minimalista, senza ridondanze
- **Anti-Ranking** — nessuna logica di promozione commerciale
- **Family-Centric** — privacy e sicurezza dei dati familiari sempre prioritarie
- **Vincolo ID Sequenziale** — nessun ID consumato inutilmente
- **Versioning Obbligatorio** — mai sovrascrivere, sempre versioning

---

## Come Contribuire

### 1. Segnalare un Bug
Apri una **Issue** su GitHub con:
- Titolo chiaro e descrittivo
- Passi per riprodurre il problema
- Comportamento atteso vs comportamento osservato
- Screenshot se rilevante

### 2. Proporre una Funzionalità
Apri una **Issue** con il tag `enhancement` descrivendo:
- Il problema che risolve
- Come si integra con i protocolli esistenti (T.C.F.™, MORPHEUS•JLX™, ecc.)
- Impatto sulla pipeline di dati

### 3. Contribuire con Codice

```bash
# 1. Forka il repository
git fork https://github.com/adrianochtribo-dot/MAMMUTH-EV

# 2. Crea un branch descrittivo
git checkout -b feat/nome-funzionalita

# 3. Fai le modifiche rispettando i principi sopra

# 4. Commit con messaggio chiaro
git commit -m "feat: descrizione della modifica"

# 5. Push e apri una Pull Request
git push origin feat/nome-funzionalita
```

### 4. Contribuire con Dati (GeoJSON)
I dati degli eventi devono rispettare lo schema JLX™:

```json
{
  "type": "Feature",
  "properties": {
    "nome": "Nome Evento",
    "tipo": "festa_religiosa | sagra | palio",
    "comune": "Nome Comune",
    "provincia": "XX",
    "periodo": "Descrizione periodo",
    "ente_organizzatore": "Nome ente",
    "descrizione_storica": "Descrizione"
  },
  "geometry": {
    "type": "Point",
    "coordinates": [longitudine, latitudine]
  }
}
```

---

## Pipeline di Validazione dei Contributi

Ogni Pull Request viene valutata secondo i protocolli del sistema:

```
PR Aperta → Review T.C.F.™ → Check MORPHEUS•JLX™ → Approvazione → Merge
```

| Check | Criterio |
|---|---|
| **Coerenza Territoriale** | Il dato è ancorato a un territorio reale verificabile? |
| **Anti-Rumore** | Non introduce duplicati o dati generici? |
| **Validazione Ontologica** | Rispetta la tassonomia definita? |
| **Auditabilità** | Il codice è tracciabile e documentato? |

---

## Struttura del Repository

```
MAMMUTH-EV/
├── index.html              # Mappa interattiva principale
├── data/                   # GeoJSON degli eventi
│   └── lazio/              # Dati per regione
├── developer/              # Developer Portal
│   ├── developer-index.html
│   └── *.html              # Documenti tecnici
├── database/               # Schema e struttura dati
├── design-system/          # Design tokens e linee guida
└── schema/                 # Schema JLX™ e tassonomia
```

---

## Comunicazione

- **Issues** → Per bug e proposte
- **Pull Requests** → Per contributi di codice
- **Discussions** → Per domande architetturali

---

## Codice di Condotta

MAMMUTH•EV™ è un progetto **Toxic-Free**. Ogni interazione deve essere:
- Rispettosa e costruttiva
- Focalizzata sul problema, non sulla persona
- In linea con la filosofia Family-Centric del sistema

---

*Leonardo Adriano Chelariu · Founder & Author · KREATIO UNIVERSAL SYSTEM™ · Code 3620*
*Ð I ⅅΓ•ⅅΛΞ•Ƨ⊥ⅅΛΞ*
