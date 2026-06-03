# Global Micro-Data Architecture

## The Problem
Google Maps knows Sermoneta but not Contrada Selva, not the square where the Sagra della Polenta takes place, not the votive chapel where the procession gathers.

## The Solution
A proprietary geographic layer with 4 levels: Nation → Region → Municipality → Micro-Entity

Micro-entities (hamlet, square, chapel, field) are defined with custom coordinates + GeoJSON polygon + relevance radius in meters. No dependency on Google.

## Geo Stack
- PostGIS — spatial queries (ST_Within, ST_DWithin)
- OpenStreetMap + Overpass API — free base data
- GeoJSON — standard format for every entity
- H3 (Uber) — hexagonal territory indexing, scales from Sermoneta to the world without rewriting a single line

## Scalability
Every new territory is a seed in the database. The architecture never changes — data is added.

## Hyper-Local Geo-Meshing
H3 Resolution L10/L11: hexagons with a radius of 10 to 25 meters map the exact portion of territory where the event takes place. Temporal coordinates dynamically activate and deactivate hexagons.

## Database
- PostgreSQL + PostGIS — persistence of historical boundaries and GeoJSON polygons
- Redis Geospatial — real-time queries and caching for latencies under 50ms
- Geographic sharding by ISO regional codes — European data on European nodes, GDPR compliant

## Global Expansion
The pilot model starts from Sermoneta (Province of Latina, Lazio, Italy). The architecture is designed to expand across Europe and subsequently to all continents without structural changes.

---
MAMMUTH EVENTS™ · KREATIO UNIVERSAL SYSTEM™ · Code 3620
