# NOTA BACKEND — BORGOVIA a 4 pilastri reali

**Data:** 2026-06-18
**Nodo pipeline:** 6 (BORGOVIA VALIDATION LAYER)
**Edge Function:** `borgovia` — https://pwfsuefyiiwnltikcdho.supabase.co/functions/v1/borgovia
**Codice versionato:** `borgovia_index_v2_4pilastri.ts` (deployato come `index.ts`)
**Tabella nuova:** `borgovia_audit`

---

## In una riga
BORGOVIA non è più una versione minima a conteggio-campi: ora valida su **4 pilastri
T.C.F. reali**, tutti calcolati senza API esterne, browser-only.

---

## I 4 pilastri — tutti reali

### Pilastro 3 — VALIDAZIONE ONTOLOGICA
titolo sano (25) + categoria ∈ insieme fidato (40) + date coerenti (35).
L'insieme fidato di categorie è costruito a runtime dalle `categoria` distinte dei record
validati a mano (`validation_origin IN ('MANUAL_LOCKED','MANUAL_CONFIRM')`). Valida sui
dati certificati, non su una lista hardcoded; si adatta da solo. Modalità degradata
(categoria solo non-placeholder) se l'insieme è vuoto.

### Pilastro 1 — COERENZA TERRITORIALE
Risolve `territorio_id` reale via match comune: normalizza `luogo` e il comune estratto
dal dominio della fonte (comune.X.lt.it), confronta con `territori.nome`. Niente API di
geocoding: coerenza a livello comune. Assegna `territorio_id` in promozione → chiude il
debito "territorio_id null". Punto-nel-poligono con lat/lng resta upgrade futuro.

### Pilastro 2 — ANTI-RUMORE (MORPHEUS-JLX)
- dedup ESATTO via dna_hash: se esiste già in `eventi` → `rejected`, non promosso.
- dedup FUZZY: similarità Jaccard sui token del titolo + vicinanza di data; sopra
  soglia 0.82 → `quarantine`. Implementato in TypeScript puro.

### Pilastro 4 — AUDITABILITA'
Ogni verdetto scritto nella tabella `borgovia_audit` (staging_id, dna_hash, titolo,
score_ontologico, score_territoriale, territorio_id_risolto, dup_esatto,
fuzzy_similarita, fuzzy_duplicato, lane, esito, verdetto jsonb, worker_id, creato_il).

---

## Soglie / decisione corsia
- dup esatto                         → rejected
- dup fuzzy                          → quarantine
- ontologico >=75 E territoriale >=75 → auto (approva)
- ontologico >=50                    → one_worker (approva con riserva)
- altrimenti                         → quarantine

Costanti: SOGLIA_AUTO=75, SOGLIA_ONE_WORKER=50, SOGLIA_TERRITORIALE_AUTO=75, SOGLIA_FUZZY=0.82.

---

## Test 2026-06-18 — RIUSCITO
`territori_caricati: 31, eventi_confronto_fuzzy: 70, processati: 3, approvati: 3,
quarantena: 0, rifiutati: 0, errori: 0`, modalita_categorie: insieme_fidato.

| Evento | ontologico | territoriale | territorio_id | lane |
|---|---|---|---|---|
| Il Centro storico di Borgo Hermada | 100 | 100 | 37 | auto |
| Il Borgo Hermada di Terracina | 100 | 100 | 37 | auto |
| 56ª Giornata mondiale della terra | 60 | 100 | 37 | one_worker |

Verificato in `eventi` (territorio_id=37 su tutti e 3) e in `borgovia_audit` (3 righe).
La Giornata della terra (categoria da_classificare) resta separata onestamente in
one_worker, non auto.

---

## Dipendenze e stato
- Richiede la tabella `borgovia_audit` (creata nella stessa sessione, 2026-06-18).
- Sostituisce ogni versione precedente di BORGOVIA (conteggio-campi, K-ontologico-v1).
- Upgrade futuri: punto-nel-poligono con lat/lng (geocoding lat/lng vero), e collegare
  K al T.C.F. formale a 4 pilastri quando definito come modulo separato.
