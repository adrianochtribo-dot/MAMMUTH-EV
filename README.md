> 🌍 **GLOBAL FOLK & TRADITIONS — Where Communities Come Alive**  
> Il sistema nervoso della cultura locale. Sagre, palii, feste religiose 
> e tradizioni invisibili del micro-territorio mondiale.

---

# MAMMUTH•EV™ | KREATIO UNIVERSAL SYSTEM™

## Cosa facciamo

Le infrastrutture digitali globali ignorano il **micro-evento invisibile**:
la sagra di paese, il palio medievale, la processione del santo patrono,
la rievocazione storica che si ripete da secoli nello stesso borgo.

**MAMMUTH•EV™** è il primo sistema open-source che mappa, valida e 
distribuisce questi eventi come dati strutturati e geolocalizzati.

> "Non mappiamo eventi, diamo voce all'identità."

---

## Quick Start — 3 passi

### 1. Visualizza i dati
Apri [geojson.io](https://geojson.io) e incolla un seed GeoJSON per 
vedere gli eventi sulla mappa.

### 2. Esplora i seed
Vai in `schema/seeds/eventi-seed/` e apri uno dei seed disponibili:
- `001-valvisciolo.md` → Abbazia di Valvisciolo, Sermoneta (LT)
- `002-sagra-porchetta-ariccia.md` → Sagra della Porchetta, Ariccia (RM)
- `003-palio-ronciglione.md` → Palio di Ronciglione, Ronciglione (VT)

### 3. Contribuisci
Copia `schema/seeds/eventi-seed/_TEMPLATE.md`, compilalo con un evento
del tuo territorio e apri una Pull Request.

---

## Formato dati — GeoJSON

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [12.9833, 41.5500]
  },
  "properties": {
    "event_id": "IT-LAZ-LT-059027-001",
    "place_id": "IT-LAZ-LT-059027",
    "nome_evento": "Abbazia di Valvisciolo — Polo Culturale Vivente",
    "tipo_primario": "festa_religiosa",
    "micro_territorio": "LAZ-02",
    "comune": "Sermoneta",
    "provincia": "LT",
    "data_o_periodo": "Ciclo liturgico annuale",
    "elemento_identitario": "Architettura cistercense, simbolismo templare"
  }
}
```

---

## Struttura del Repository
MAMMUTH-EV/
├── schema/
│   └── seeds/
│       ├── eventi-seed/          ← seed eventi compilati
│       │   ├── _TEMPLATE.md      ← template per nuovi seed
│       │   ├── 001-valvisciolo.md
│       │   ├── 002-sagra-porchetta-ariccia.md
│       │   └── 003-palio-ronciglione.md
│       ├── territorio/           ← documentazione micro-territorio
│       │   ├── README.md
│       │   ├── tipologie-evento.md
│       │   ├── validazione-schema.md
│       │   └── fonti-dati.md
│       └── geo/
│           └── micro-territori.md
├── database/                     ← entità geografiche
├── CONTRIBUTING.md               ← come contribuire
├── LICENSE                       ← ODbL 1.0
└── README.md                     ← questo file
---

## Cluster attivi — Fase 1 (Lazio)

| ID | Micro-territorio | Province |
|----|-----------------|---------|
| LAZ-01 | Castelli Romani | RM |
| LAZ-02 | Monti Lepini | LT/FR |
| LAZ-03 | Ciociaria | FR |
| LAZ-04 | Maremma Laziale | VT |
| LAZ-05 | Sabina | RI/RM |
| LAZ-06 | Agro Pontino | LT |
| LAZ-07 | Roma storica | RM |

---

## Visione & Identità

KREATIO è l'infrastruttura globale che garantisce solidità, sicurezza e 
fluidità. Ogni progetto innestato è un modulo che eredita la struttura 
logica del sistema madre. L'ispirazione estetica e funzionale è 
**ElppaK•Clean™**: massima potenza tecnologica, massima complessità 
gestita, ma un'esperienza utente finale di una semplicità disarmante, 
leggera, dinamica e intuitiva.

## Ruolo dell'IA

L'IA che sviluppa questo sistema è il Guardiano della Logica. Non è un 
assistente, è l'architetto del sistema. Il suo compito è mantenere 
l'integrità dell'ecosistema, garantendo che ogni componente rispetti i 
vincoli di sicurezza, la coerenza dei dati e la visione Family-Centric.

## Obiettivo

Essere il punto di riferimento in cui tecnologia e umanità si incontrano. 
L'ecosistema è un'oasi di memoria reale, protetta e accessibile, dove il 
movimento, la scoperta e l'esperienza del micro-territorio diventano 
un'esperienza globale, fluida e sicura per l'intera famiglia.

## Framework Operativo

Il progetto è regolato dal **MASTER_FRAMEWORK.md** (Checklist 
macro-sistemi) e dalle direttive di ingegneria dei dati definite nel 
**Core 3620™**.

---

Leonardo Adriano Chelariu  
Founder & Author (KREATIO UNIVERSAL SYSTEM™ • Code 3620)  
K•Word•Festival (KWF)

---
