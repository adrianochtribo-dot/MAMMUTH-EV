-- ============================================================================
-- Migration: 2026-06-18_fonti_staging_datafix  (v3 — AS EXECUTED)
-- Author:    Leonardo Adriano Chelariu (Nero Kaelum)
-- System:    KREATIO UNIVERSAL SYSTEM™ — Code 3620 | MAMMUTH•EVENTS™
-- Scope:     Checklist Motore — punti A + B + C (fondamenta dati pipeline)
--
-- IMPORTANTE: questo file riproduce ESATTAMENTE i comandi realmente eseguiti
-- in produzione il 2026-06-18, eseguiti in tre transazioni separate dal
-- SQL Editor Supabase, ciascuna conclusa con "Success".
--
-- SCOPERTE A RUNTIME (perché questo file differisce dalla v2 pianificata):
--   * I codici ISTAT in `territori` erano GIÀ corretti. Riscriverli generava
--     errore 23505 (duplicate key su territori_istat_code_key). Quindi NON si
--     toccano i codici: si eliminano solo le righe duplicate.
--   * I duplicati reali erano DUE, non uno solo:
--       - Bassiano: id 5 (istat 059004, errato) + id 9 (istat 059002, giusto) -> tieni 9
--       - Sezze:    id 34 (istat 059027, errato) + id 6 (istat 059028, giusto) -> tieni 6
--   * Terracina nel DB ha istat_code '059030' (Terracina e Sperlonga risultano
--     scambiati tra loro: Sperlonga id 39 = 059032). Per coerenza interna la
--     fonte usa '059030'. Lo scambio Terracina/Sperlonga è da risolvere a parte.
--   * Punto D (manual_locked) RIMOSSO: eventi ha già validation_origin /
--     locked_by; BORGOVIA salterà validation_origin='manual' o locked_by NOT NULL.
-- ============================================================================


-- ============================================================================
-- A) FIX DATI TERRITORI — dedup (come eseguito)
--    Sposta gli eventi dai duplicati alle righe corrette, poi elimina i duplicati.
-- ============================================================================
BEGIN;
UPDATE eventi SET territorio_id = 9 WHERE territorio_id = 5;    -- Bassiano: 5 -> 9
UPDATE eventi SET territorio_id = 6 WHERE territorio_id = 34;   -- Sezze:   34 -> 6
DELETE FROM territori WHERE id IN (5, 34);
COMMIT;


-- ============================================================================
-- B) TABELLA fonti — registro sorgenti da scandagliare (come eseguito)
-- ============================================================================
CREATE TABLE IF NOT EXISTS fonti (
    id                  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    comune              text    NOT NULL,
    istat_code          text    NOT NULL,
    territorio_id       integer REFERENCES territori(id),
    url                 text    NOT NULL,
    piattaforma         text    NOT NULL DEFAULT 'mycity'
                                CHECK (piattaforma IN ('mycity','agid','custom')),
    parser_type         text    NOT NULL DEFAULT 'mycity_v1',
    attivo              boolean NOT NULL DEFAULT true,
    crawl_frequency_min integer NOT NULL DEFAULT 1440,   -- 1440 = 1 volta/giorno
    last_crawl          timestamptz,
    last_status         text,
    created_at          timestamptz NOT NULL DEFAULT now(),
    UNIQUE (url)
);

INSERT INTO fonti (comune, istat_code, url, piattaforma, parser_type, attivo)
VALUES ('Terracina', '059030', 'https://www.comune.terracina.lt.it/eventi',
        'mycity', 'mycity_v1', true)
ON CONFLICT (url) DO NOTHING;


-- ============================================================================
-- C) TABELLA eventi_staging — grezzo PRIMA della validazione (come eseguito)
--    Colonne speculari a `eventi` -> promozione = INSERT ... SELECT pulito.
-- ============================================================================
CREATE TABLE IF NOT EXISTS eventi_staging (
    staging_id        bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fonte_id          bigint  REFERENCES fonti(id),
    dna_hash          varchar,
    titolo            varchar,
    sottotitolo       varchar,
    descrizione       text,
    categoria         varchar,
    sottocategoria    varchar,
    data_inizio       timestamptz,
    data_fine         timestamptz,
    orario_inizio     time,
    orario_fine       time,
    luogo             varchar,
    indirizzo         varchar,
    territorio_id     integer REFERENCES territori(id),
    geom              geometry(Point,4326),
    lat               double precision,
    lng               double precision,
    gratuito          boolean,
    prezzo_min        numeric,
    prezzo_max        numeric,
    organizzatore     varchar,
    fonte_url         text,
    tags              text[],
    ricorrenza        text,
    costo_raw         text,        -- prezzo grezzo (bug euro fino al fix E)
    confidence_score  numeric,     -- T.C.F. (nodo 5)
    stato_validazione text NOT NULL DEFAULT 'pending'
                      CHECK (stato_validazione IN
                             ('pending','approved','rejected','quarantine')),
    borgovia_verdetto text,        -- BORGOVIA (nodo 6)
    raw_payload       jsonb,
    estratto_il       timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_staging_stato    ON eventi_staging(stato_validazione);
CREATE INDEX IF NOT EXISTS idx_staging_fonte    ON eventi_staging(fonte_id);
CREATE INDEX IF NOT EXISTS idx_staging_dna_hash ON eventi_staging(dna_hash);


-- ============================================================================
-- DEBITO TECNICO NOTO (non risolto in questa migration)
--   1. Terracina (id 37) e Sperlonga (id 39) hanno gli istat_code scambiati:
--      Terracina = 059030, Sperlonga = 059032. Reali ISTAT: Terracina 059032.
--   2. Diversi altri comuni Latina hanno istat_code sfalsati rispetto
--      all'ufficiale (es. Aprilia 059001 vs reale, Campodimele 059003, ecc.).
--      Da riallineare prima di attivare il track Provincia di Latina.
-- ============================================================================

-- ============================================================================
-- VERIFICA (eseguire separatamente)
-- ============================================================================
-- SELECT id, nome, istat_code FROM territori WHERE nome ILIKE 'bassiano';   -- 1 riga (id 9)
-- SELECT id, nome, istat_code FROM territori WHERE nome ILIKE 'sezze';      -- 1 riga (id 6)
-- SELECT id, comune, istat_code, url, attivo FROM fonti WHERE attivo;       -- Terracina
-- SELECT COUNT(*) FROM eventi_staging;                                      -- 0
