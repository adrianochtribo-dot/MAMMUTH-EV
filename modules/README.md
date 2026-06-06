# modules/ — Moduli KREATIO

Questa cartella contiene i moduli funzionali del KREATIO UNIVERSAL SYSTEM™.
Ogni modulo è indipendente e ha la propria logica, test e documentazione.

## Moduli Presenti

| Modulo | Stato | Cartella | Descrizione |
|--------|-------|----------|-------------|
| ANTHROPIC HOLE™ | ◐ IN SVILUPPO | `anthropic-hole/` | Pipeline WhatsApp → OCR → Claude API |
| MORPHEUS·JLX™ | ◐ IN SVILUPPO | `morpheus-jlx/` | Anti-rumore semantico |
| T.C.F.™ | ● LIVE | `tcf/` | Total Coherence Framework |

## Regole di Modularità

- Ogni modulo è **indipendente** — nessuna dipendenza diretta tra moduli
- La comunicazione tra moduli avviene via `src/api/` o eventi asincroni
- Ogni modulo ha il proprio `README.md`, `tests/` e `package.json`
- Stato del modulo dichiarato nel README: LIVE / IN SVILUPPO / PIANIFICATO

## Come Aggiungere un Modulo

1. Crea cartella `modules/[nome-modulo]/`
2. Aggiungi `README.md` con descrizione, stack e stato
3. Aggiungi `tests/` con test unitari
4. Documenta nel [Developer Portal](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/developer-index.html)

## Riferimenti

- Mappa completa moduli → [EXOSKELETON™](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/exoskeleton.html)
- Validazione → `src/validation/`

---
MAMMUTH•EVENTS™ · KREATIO UNIVERSAL SYSTEM™ · Code 3620
