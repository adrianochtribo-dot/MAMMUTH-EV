-- Migration: fix in_scope_pilot to Sermoneta-only, extend eventi_view
-- Date: 2026-06-14
-- Author: Leonardo Adriano Chelariu

-- 1. Reset in_scope_pilot based on territorio_id (previous migration only
--    excluded Ponza by name-matching on `luogo`, missing Bassiano/Sezze).
--    Sermoneta = territorio_id 1 (ISTAT 059026). All other territories
--    (Bassiano x2, Sezze, Ponza) are out of pilot scope.
UPDATE eventi SET in_scope_pilot = (territorio_id = 1);
-- Result: 40 in-scope (Sermoneta), 28 out-of-scope.

-- 2. Extend eventi_view to expose sottocategoria and prezzo_max, required
--    by MappaEventi.tsx / CategoryFilterSheet for category filtering.
CREATE OR REPLACE VIEW public.eventi_view AS
SELECT id, titolo, categoria, sottocategoria, luogo, indirizzo, data_inizio, data_fine,
       gratuito, prezzo_min, prezzo_max, descrizione,
       ST_Y(geom::geometry) AS lat, ST_X(geom::geometry) AS lng
FROM eventi
WHERE in_scope_pilot = true;

-- Note: territori table has data quality issues (Bassiano duplicated as
-- territorio_id 3 and 5 with different istat_code; Sezze istat_code 059028
-- conflicts with prior memory attribution to Ponza). Flagged for separate
-- T.C.F. Auditabilita review, not addressed in this migration.
