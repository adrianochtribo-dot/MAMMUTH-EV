# src/ — Source Code

Questa cartella contiene tutto il codice applicativo di MAMMUTH•EVENTS™.

## Struttura
src/
├── frontend/     ← Next.js 14 + TypeScript (web app)
├── api/          ← Node.js backend + REST API
└── validation/   ← T.C.F.™ validation engine
## Regole

- Ogni sottocartella ha il proprio `README.md` con istruzioni specifiche
- Nessun dato reale in questa cartella — i dati stanno in `atlas-eventa/` e `database/`
- Ogni modulo deve avere i propri test prima del merge su `main`
- Standard di codice: TypeScript strict, ESLint, Prettier

## Entry Points

| Layer | Cartella | Stack |
|-------|----------|-------|
| Web frontend | `src/frontend/` | Next.js 14 + Tailwind CSS |
| Mobile | `src/frontend/mobile/` | React Native |
| Backend API | `src/api/` | Node.js + Express |
| Validazione | `src/validation/` | TypeScript + T.C.F.™ |

## Riferimenti

- Architettura completa → [EXOSKELETON™](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/exoskeleton.html)
- Stack tecnico → [Developer Portal](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/developer-index.html)

---
MAMMUTH•EVENTS™ · KREATIO UNIVERSAL SYSTEM™ · Code 3620
