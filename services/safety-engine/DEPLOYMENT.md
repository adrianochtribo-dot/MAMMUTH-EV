# MAMMUTH•EVENTS™ — Safety Engine · Deployment Live

## Stato: PRODUZIONE ✅

| Campo | Valore |
|-------|--------|
| URL pubblico | https://mammuth-ev-production.up.railway.app |
| Swagger UI | https://mammuth-ev-production.up.railway.app/docs |
| Health Check | https://mammuth-ev-production.up.railway.app/api/v1/safety/health |
| Piattaforma | Railway.app |
| Runtime | Python 3.12.13 |
| Framework | FastAPI 0.111.0 |
| Scenario | A — Deterministico (Fruin LoS) |
| Versione | 1.0.0 |
| Deploy date | 2026-06-08 |

## Test live — Sagra di Sermoneta 2026

Payload testato il 2026-06-08:
- Presenze: 2000 · Area: 800 m²
- Risk score: **0.681** — livello **ALTO**
- Densità: 2.5 p/m² — Fruin LoS D
- Match storico: Piazza San Carlo Torino 2017 (similarità 0.948)

## Note architetturali

- Root directory Railway: `/services/safety-engine`
- Build system: Nixpacks con Python 3.12
- Porta: 8080
