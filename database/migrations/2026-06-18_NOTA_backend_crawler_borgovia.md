# NOTA BACKEND — Sessione 2026-06-18

**Pipeline KREATIO — nodi toccati:** INGRESSO (crawler) → eventi_staging → BORGOVIA (nodo 6) → ATLAS•EVENTA (`eventi`)
**Ambito:** rendere eseguibile il tratto INGRESSO→VALIDAZIONE→PROMOZIONE senza inserimento manuale.

---

## 1. Crawler (Edge Function `crawl-worker`) — punti E / F / G

### E — bug `costo` HTML-encoded: INESISTENTE
Il punto E della checklist (regex `costo` rotta dal simbolo euro `&euro;`/`&#8364;`) **non si applica**:
- `decodeEntities()` nel crawler decodifica già `&euro;` e `&#8364;`;
- soprattutto, **il crawler non estrae affatto il prezzo** dalle pagine MyCity/AGID. Non c'è nessun campo `costo` da correggere.
- **Esito: punto E annullato.** Nessuna modifica necessaria.

### G — parser parametrico per N comuni: GIÀ FATTO
Il crawler **non era** monolitico su Terracina. Usa già un'architettura a coda parametrica:
- registro sorgenti: tabella `crawl_sources` (id, domain, base_url, robots_*, min_delay_sec, active...);
- coda lavori: tabella `crawl_queue` con RPC `claim_next_job` / `complete_job` / `fail_job`;
- un singolo parser MyCity/AGID serve migliaia di comuni italiani sulla stessa piattaforma.
- **Esito: punto G già soddisfatto.** Nessuna modifica necessaria.

### F — destinazione scrittura: MODIFICATO (l'unica vera modifica)
**Prima:** il crawler scriveva il grezzo direttamente in `eventi` via `upsert` — saltando ogni validazione.
**Dopo:** il crawler scrive in `eventi_staging` con `stato_validazione = 'pending'`. Niente entra in `eventi` senza passare da BORGOVIA.

Blocco modificato (sostituito `eventi`.upsert con `eventi_staging`.insert):
```ts
await supabase.from("eventi_staging").insert({
  dna_hash,
  titolo,
  descrizione,
  categoria,
  data_inizio,
  data_fine,
  orario_inizio,
  orario_fine,
  luogo,
  fonte_url,
  territorio_id: null,
  stato_validazione: "pending"
});
```
**Test confermato:** run su Terracina → 3 eventi in `eventi_staging` con `stato_validazione = 'pending'`
(Borgo Hermada centro storico, Borgo Hermada di Terracina, 56ª Giornata mondiale della terra).

---

## 2. Tabella `fonti` — DEPRECATA

Nella Fase 0 era stata creata `fonti` come registro sorgenti. È **ridondante**: il crawler usa `crawl_sources`, che è più completo (gestione robots.txt, delay, last_hit_at).

- **Registro canonico delle sorgenti = `crawl_sources`.**
- `fonti` NON va usata. Non collegarla al crawler. Va rimossa/ignorata.
- Motivo per cui resta documentata: evitare che in futuro qualcuno (o io stesso) la ritrovi e creda sia attiva.

---

## 3. BORGOVIA — Edge Function (nodo 6) — punti L / M / N

Creata e deployata nuova Edge Function `borgovia`.
URL: `https://pwfsuefyiiwnltikcdho.supabase.co/functions/v1/borgovia`

### L — lettura pending
Legge `eventi_staging WHERE stato_validazione = 'pending' LIMIT 50`.

### M — confidence (T.C.F. MINIMO PROVVISORIO)
**ATTENZIONE — debito tecnico dichiarato:** questo NON è il T.C.F. vero a 4 pilastri (punto K, ancora da costruire). È una versione minima provvisoria basata solo sulla **completezza dei campi**:

| Controllo | Punti |
|---|---|
| titolo > 3 caratteri | 25 |
| data_inizio presente | 25 |
| luogo presente | 25 |
| categoria ≠ 'da_classificare' | 25 |

Soglie (costanti dichiarate): `SOGLIA_AUTO = 75`, `SOGLIA_ONE_WORKER = 50`.
- score ≥ 75 → corsia `auto` → approva
- 50–74 → corsia `one_worker` → approva
- < 50 → quarantine

**Anello debole noto:** la categorizzazione. Quando si farà il punto K, BORGOVIA dovrà chiamare il T.C.F. vero al posto di questa funzione minima.

### N — promozione
Record approvati → `upsert` in `eventi` (onConflict `dna_hash`, ignoreDuplicates) con:
`validation_status='VALIDATED'`, `validation_origin='CRAWLER_AUTO'`, `validation_lane=<lane>`, `da_verificare=true`, `verificato=false`, `in_scope_pilot=false`, `reputation_score=<score>`.
Staging del record marcato `approved`.

**Skip strutturale dei record manuali:** lo staging per costruzione non contiene record manuali; BORGOVIA salta comunque `validation_origin='manual' OR locked_by IS NOT NULL`. La frontiera manuale/automatico è nei dati, non a parole.

### Test BORGOVIA — RIUSCITO
Risposta: `{ ok:true, processati:3, approvati:3, quarantena:0, errori:0 }`
- score 100 / 100 / 75, tutti corsia `auto`
- il 75 è la "Giornata della terra" (categoria `da_classificare`, l'anello debole sopra)

Verifica post-promozione (2 query):
```sql
SELECT titolo, validation_status, validation_lane, reputation_score
FROM eventi WHERE validation_origin='CRAWLER_AUTO';
-- → 3 righe VALIDATED / auto / 100,100,75

SELECT stato_validazione, COUNT(*) FROM eventi_staging GROUP BY stato_validazione;
-- → approved: 3
```

---

## Stato del ciclo dopo questa sessione
**Funzionante senza mani:** `crawl_queue` → `crawl-worker` → `eventi_staging` (pending) → `borgovia` → `eventi` (validato).

## Cosa NON è stato fatto (resta aperto)
- **K** — T.C.F. vero a 4 pilastri (Coerenza Territoriale, Anti-Rumore/MORPHEUS·JLX, Validazione Ontologica, Auditabilità). BORGOVIA oggi usa solo completezza campi.
- **I** — COLOR TRIAGE eseguibile (oggi solo doc HTML).
- **J** — MORPHEUS·JLX dedup eseguibile.
- **O** — tabella `borgovia_audit` (tracciabilità verdetti).
- **P** — geocoding automatico (12 eventi Sermoneta senza coordinate + i nuovi senza territorio_id/geom).
- **R/S/T/U/V/W/X/Y** — scheduling pg_cron, batch, rate limiting, retry/dead-letter, vista stato pipeline, dashboard, alert, metriche.
- **Z** — espansione fonti Provincia di Latina, BLOCCATA da debito tecnico ISTAT (Terracina id 37 ha 059030 e Sperlonga id 39 ha 059032: scambiati; altri comuni Latina sfalsati).
