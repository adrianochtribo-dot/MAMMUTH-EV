-- Migration: add in_scope_pilot flag and update eventi_view
-- Date: 2026-06-13
-- Author: Leonardo Adriano Chelariu

-- 1. Add scope flag column, default true (all existing events remain in-scope unless flagged)
ALTER TABLE eventi ADD COLUMN IF NOT EXISTS in_scope_pilot boolean DEFAULT true;

-- 2. Flag out-of-scope events (Ponza / Palmarola - not part of Sermoneta pilot, ISTAT 059026)
UPDATE eventi SET in_scope_pilot = false
WHERE luogo ILIKE '%ponza%' OR luogo ILIKE '%palmarola%';

-- 3. Recreate public view to expose only in-scope events
CREATE OR REPLACE VIEW public.eventi_view AS
SELECT id, titolo, categoria, luogo, indirizzo, data_inizio, data_fine,
       gratuito, prezzo_min, descrizione,
       ST_Y(geom::geometry) AS lat, ST_X(geom::geometry) AS lng
FROM eventi
WHERE in_scope_pilot = true;

-- 4. Category correction: id 130 reclassified from invalid category
-- 'videogiochi di cultura pop' -> 'pop_culture_gaming' (T.C.F. whitelist compliance)
-- (already applied directly; documented here for audit trail)
