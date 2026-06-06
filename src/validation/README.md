# src/validation/ — T.C.F.™ Validation Engine

Questo layer implementa il Total Coherence Framework — il guardiano del database MAMMUTH•EVENTS™.

## Responsabilità

- Validazione dei 4 pilastri T.C.F.™ su ogni record in ingresso
- Integrazione con MORPHEUS·JLX™ per l'anti-rumore semantico
- Assegnazione ID sequenziale (DNA del dato)
- Classificazione triage Verde / Giallo / Rosso
- Log CID_HUB per ogni operazione

## Stack

- **TypeScript** — Linguaggio principale
- **PostgreSQL** — Verifica coerenza geografica ISTAT
- **KDE** — Kernel Density Estimation per soglie dinamiche
- **ISTAT/ANAC Oracle** — Verifica fonti istituzionali esterne

## Struttura
validation/
├── tcf/              ← 4 pilastri T.C.F.™
│   ├── pillar-01-territorial.ts
│   ├── pillar-02-antinoise.ts
│   ├── pillar-03-ontological.ts
│   └── pillar-04-auditability.ts
├── morpheus/         ← Anti-rumore JLX
├── criterion/        ← ID sequenziale + triage
└── oracle/           ← Verifica ISTAT/ANAC
## I 4 Pilastri T.C.F.™

| Pilastro | Nome | Descrizione |
|----------|------|-------------|
| P01 | Coerenza Territoriale | ISTAT code + comune verificati |
| P02 | Anti-Rumore MORPHEUS·JLX™ | Duplicati e anomalie semantiche |
| P03 | Validazione Ontologica | Categoria dentro tassonomia chiusa |
| P04 | Auditabilità | VERSION + SOURCE_TYPE tracciabili |

## Regola Assoluta

> **Zero Invented Data.** Ogni record deve provenire da fonti istituzionali verificate.
> Vietato: blog, aggregatori, social media non istituzionali.

## Riferimenti

- Playground interattivo → [T.C.F.™ Playground](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/TCF-playground.html)
- Schema database → `database/`
- EXOSKELETON™ → [Master Doc](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/exoskeleton.html)

---
MAMMUTH•EVENTS™ · KREATIO UNIVERSAL SYSTEM™ · Code 3620
