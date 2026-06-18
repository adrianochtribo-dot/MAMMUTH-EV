# CHECKLIST MOTORE — NOTA UFFICIALE PUNTO D
## (per il documento sviluppatori — evita il "buco" tra C ed E)

---

### D) `manual_locked` — STATO: RISOLTO PER ASSORBIMENTO (non implementato come nuova colonna)

**Decisione:** il punto D NON viene implementato come previsto in origine. NON si aggiunge
alcuna colonna `manual_locked` alla tabella `eventi`.

**Perché.** All'avvio del lavoro la checklist prevedeva una nuova colonna booleana
`manual_locked` per marcare i record validati a mano, che BORGOVIA (nodo 6) deve sempre
saltare. La verifica dello schema production reale (`information_schema`) ha però mostrato
che la tabella `eventi` possiede GIÀ la macchina di validazione completa:

    validation_lane      text
    validation_status    text
    validation_origin    text        <-- confine manuale/automatico
    locked_by            text        <-- lock applicativo
    locked_at            timestamptz
    risk_score           numeric
    predict_score        numeric
    reputation_score     numeric
    corroboration_count  integer
    verificato           boolean
    verificato_da        varchar
    verificato_at        timestamptz
    da_verificare        boolean

Aggiungere `manual_locked` avrebbe creato una SECONDA bandiera in competizione con
`validation_origin` / `locked_by`, cioè due fonti di verità per lo stesso concetto —
una garanzia di bug futuri e di disallineamento tra record.

**Come è realizzato il confine manuale/automatico (al posto di `manual_locked`).**
Il requisito originale ("BORGOVIA salta sempre i record validati a mano") è soddisfatto
usando le colonne esistenti. Regola di skip canonica per BORGOVIA:

    -- BORGOVIA NON tocca un record se è marcato manuale o bloccato:
    WHERE validation_origin = 'manual'
       OR locked_by IS NOT NULL

**Cosa resta da fare (verifica, non implementazione).** Prima di scrivere BORGOVIA
(nodo 6, punto L) va letto come sono marcati OGGI i record manuali nel DB, per fissare
la condizione di skip esatta sui valori reali. Query diagnostica (non modifica nulla):

    SELECT validation_origin, validation_status, validation_lane,
           (locked_by IS NOT NULL) AS locked, COUNT(*)
    FROM eventi
    GROUP BY validation_origin, validation_status, validation_lane, locked
    ORDER BY COUNT(*) DESC;

**Tracciabilità (REGOLA ASSOLUTA).** Questa decisione è documentata anche nel commit
della migration `2026-06-18_fonti_staging_datafix.sql` (riga: "Punto D (manual_locked)
rimosso: eventi ha già validation_origin/locked_by").

---

### Riepilogo FASE 0 dopo questa nota

| Punto | Stato | Note |
|-------|-------|------|
| A — Fix dati territori (dedup) | ✅ FATTO | Bassiano id 5→9, Sezze id 34→6, doppioni eliminati |
| B — Tabella `fonti` | ✅ FATTO | Seed Terracina (istat 059030) attivo |
| C — Tabella `eventi_staging` | ✅ FATTO | Colonne speculari a `eventi` + campi pipeline |
| D — `manual_locked` | ✅ RISOLTO PER ASSORBIMENTO | Usa `validation_origin` / `locked_by` esistenti; nessuna nuova colonna |

FASE 0 completa. Prossimo: E + F + G (crawl-worker → scrittura in `eventi_staging`).
