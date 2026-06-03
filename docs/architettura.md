# Architettura Globale del Micro-Dato

## Il Problema
Google Maps conosce Sermoneta ma non la Contrada Selva, non la piazza della Sagra della Polenta, non il capitello votivo dove si raduna la processione.

## La Soluzione
Un layer geografico proprietario a 4 livelli: Nazione → Regione → Comune → Micro-Entità

Le micro-entità (frazione, piazza, capitello, campo) vengono definite con coordinate custom + poligono GeoJSON + raggio di rilevanza in metri. Nessuna dipendenza da Google.

## Stack Geo
- PostGIS — query spaziali (ST_Within, ST_DWithin)
- OpenStreetMap + Overpass API — base dati libera
- GeoJSON — formato standard per ogni entità
- H3 (Uber) — indicizzazione esagonale, scala da Sermoneta al mondo senza riscrivere una riga

## Scalabilità
Ogni nuovo territorio è un seed nel database. L'architettura non cambia — si aggiungono dati.

## Geo-Meshing Iper-Locale
Risoluzione H3 L10/L11: esagoni con raggio da 10 a 25 metri mappano l'esatta porzione di territorio dove si svolge l'evento. Le coordinate temporali attivano e disattivano gli esagoni dinamicamente.

## Database
- PostgreSQL + PostGIS — persistenza dei confini storici e poligoni GeoJSON
- Redis Geospatial — query real-time e caching per latenze inferiori a 50ms
- Sharding geografico per codici ISO regionali — dati europei su nodi europei, rispetto GDPR

## Espansione Globale
Il modello pilota parte da Sermoneta (Provincia di Latina, Lazio, Italia). L'architettura è concepita per espandersi in tutta Europa e successivamente in tutti i continenti senza modifiche strutturali.
