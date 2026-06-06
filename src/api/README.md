# src/api/ — Backend API

Questo layer gestisce tutta la logica server-side di MAMMUTH•EVENTS™.

## Stack

- **Node.js** — Runtime
- **Express / Fastify** — Framework HTTP
- **PostgreSQL + PostGIS** — Database principale
- **Typesense** — Search engine full-text
- **JWT** — Autenticazione

## Struttura
api/
├── routes/       ← Endpoint REST
├── controllers/  ← Logica business
├── models/       ← Schema database
├── middleware/   ← Auth, rate limiting, logging
├── services/     ← Integrazioni esterne (WhatsApp, Claude API)
└── config/       ← Variabili ambiente, connessioni DB
## Endpoint Principali

| Metodo | Path | Descrizione |
|--------|------|-------------|
| GET | `/api/events` | Lista eventi validati |
| GET | `/api/events/:id` | Evento singolo per ID DNA |
| POST | `/api/events` | Inserimento nuovo evento |
| GET | `/api/territory/:istat` | Eventi per codice ISTAT |
| POST | `/api/validate` | Validazione T.C.F.™ |
| POST | `/api/ingest/whatsapp` | Ingestion foto WhatsApp |

## Variabili Ambiente

Vedere `.github/.env.example` per la lista completa.

## Riferimenti

- Validazione → `src/validation/`
- Database schema → `database/`
- EXOSKELETON™ → [Master Doc](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/exoskeleton.html)

---
MAMMUTH•EVENTS™ · KREATIO UNIVERSAL SYSTEM™ · Code 3620
