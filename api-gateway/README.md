# api-gateway/ — API Gateway

Layer di comunicazione esterno e interno di MAMMUTH•EVENTS™.
Gestisce autenticazione, routing, rate limiting e sicurezza.

## Responsabilità

- Punto di ingresso unico per tutte le richieste esterne
- Autenticazione JWT e autorizzazione per ruolo
- Rate limiting per prevenire abusi
- Routing verso i microservizi interni
- Logging di tutte le richieste

## Stack

- **Node.js + Express** — Gateway server
- **JWT** — Token autenticazione
- **OAuth 2.0** — Autenticazione esterna
- **Redis** — Rate limiting e cache sessioni

## Struttura
api-gateway/
├── auth/         ← JWT, OAuth, middleware autenticazione
├── routes/       ← Routing verso src/api/
├── middleware/   ← Rate limiting, logging, CORS
└── config/       ← Variabili ambiente, whitelist domini
## Endpoint Protetti

| Ruolo | Accesso |
|-------|---------|
| `public` | GET eventi, ricerca, mappa |
| `contributor` | POST eventi, ingestion WhatsApp |
| `validator` | Operazioni T.C.F.™, triage |
| `admin` | Tutto + gestione utenti + ban |

## Sicurezza

- HTTPS obbligatorio
- CORS configurato per domini autorizzati
- Rate limit: 100 req/min per IP pubblico
- Tutti i log salvati in CID_HUB

## Riferimenti

- Backend → `src/api/`
- Validazione → `src/validation/`
- EXOSKELETON™ → [Master Doc](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/exoskeleton.html)

---
MAMMUTH•EVENTS™ · KREATIO UNIVERSAL SYSTEM™ · Code 3620
