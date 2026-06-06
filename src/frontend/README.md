# src/frontend/ — Frontend Web & Mobile

Questo layer contiene tutta l'interfaccia utente di MAMMUTH•EVENTS™.

## Stack

- **Next.js 14** — Web app, SSR, routing
- **TypeScript** — Tipizzazione strict
- **Tailwind CSS** — Styling
- **React Native** — App iOS/Android (sottocartella `mobile/`)
- **Leaflet.js** — Mappa interattiva eventi

## Struttura
frontend/
├── web/          ← Next.js 14 app
│   ├── app/      ← App Router
│   ├── components/
│   └── styles/
├── mobile/       ← React Native
│   ├── ios/
│   └── android/
└── shared/       ← Componenti condivisi web/mobile
## Design System

Tutte le interfacce seguono lo standard **ElppaK•Clean™**:
- Dark theme obbligatorio
- Font: IBM Plex Mono + Bebas Neue
- Palette: vedere `design-system/`

## Comandi

```bash
# Web
cd web && npm install && npm run dev

# Mobile
cd mobile && npm install && npx expo start
```

## Riferimenti

- Design System → `design-system/`
- API → `src/api/`
- EXOSKELETON™ → [Master Doc](https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/exoskeleton.html)

---
MAMMUTH•EVENTS™ · KREATIO UNIVERSAL SYSTEM™ · Code 3620
