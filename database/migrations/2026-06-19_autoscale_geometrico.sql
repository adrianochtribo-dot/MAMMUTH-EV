-- ============================================================
-- MAMMUTH-EV — MIGRATION 2026-06-19
-- Auto-scaling geometrico dei crawl-worker: 1 -> 2 -> 4 -> ... -> 256
-- ============================================================
--
-- CONTESTO
-- Prima: il cron lanciava SEMPRE 5 worker fissi ogni minuto
--        (generate_series(1,5)), anche a coda vuota, con la
--        service_role_key scritta IN CHIARO dentro cron.job.
--
-- Ora:   un solo cron chiama autoscale_worker(), che legge la
--        profondita della coda (crawl_queue.status='pending') e
--        lancia un numero di worker pari alla potenza di 2 che
--        copre la coda, con tetto a 256. Coda vuota => 0 worker.
--        La chiave service_role e' letta dal Vault (cifrata)
--        tramite lancia_worker(), mai esposta nel comando cron.
--
-- INVARIATO
--   - orchestratore()   : resta il PRODUTTORE (accoda le pagine-sorgente attive)
--   - lancia_worker(n)   : invoca n volte crawl-worker leggendo la key dal Vault
--   - claim_next_job()   : anti-ban 1-dominio-per-worker (regge anche a 256 worker)
--   - cron 'valida-pending-hourly' : promozione BORGOVIA, non toccato
-- ============================================================


-- ------------------------------------------------------------
-- 1) FUNZIONE DI AUTO-SCALING GEOMETRICO
-- ------------------------------------------------------------
create or replace function autoscale_worker()
returns table(pending integer, worker_lanciati integer)
language plpgsql
as $function$
declare
  v_pending integer;
  v_worker  integer;
begin
  -- 1. quanti job aspettano di essere presi
  select count(*) into v_pending
  from crawl_queue
  where status = 'pending';

  -- 2. nessun lavoro -> nessun worker (stop allo spreco a vuoto)
  if v_pending = 0 then
    return query select 0, 0;
    return;
  end if;

  -- 3. potenza di 2 che copre la coda, tetto a 256
  --    1->1, 2..3->2, 4..7->4, 8..15->8 ... >=256 -> 256
  v_worker := least(256, power(2, ceil(log(2, v_pending)))::integer);
  if v_worker < 1 then
    v_worker := 1;
  end if;

  -- 4. lancia esattamente quei worker (usa il Vault, chiave cifrata)
  perform lancia_worker(v_worker);

  return query select v_pending, v_worker;
end;
$function$;


-- ------------------------------------------------------------
-- 2) RICONFIGURAZIONE CRON
--    Rimuove il vecchio job a 5 worker fissi (jobid 1, key in chiaro)
--    e installa il nuovo job di auto-scaling.
-- ------------------------------------------------------------

-- rimuove il vecchio cron fisso (era jobid 1)
select cron.unschedule(1);

-- nuovo cron: auto-scaling geometrico ogni minuto
select cron.schedule(
  'autoscale-crawler',
  '* * * * *',
  $$ select autoscale_worker(); $$
);


-- ------------------------------------------------------------
-- 3) VERIFICA DELLA PROGRESSIONE (solo controllo, non lancia worker)
--    Atteso:
--      0->0, 1->1, 2->2, 3->4, 4->4, 5->8, 7->8, 8->8,
--      15->16, 16->16, 50->64, 100->128, 128->128,
--      200->256, 256->256, 300->256, 1000->256
-- ------------------------------------------------------------
-- with prova(pending) as (
--   values (0),(1),(2),(3),(4),(5),(7),(8),(15),(16),(50),(100),(128),(200),(256),(300),(1000)
-- )
-- select pending,
--        case when pending = 0 then 0
--             else least(256, power(2, ceil(log(2, pending)))::integer)
--        end as worker_calcolati
-- from prova order by pending;


-- ------------------------------------------------------------
-- 4) VERIFICA STATO CRON (atteso: niente jobid 1, presente autoscale-crawler attivo)
-- ------------------------------------------------------------
-- select jobid, jobname, schedule, active, left(command,60) as comando
-- from cron.job order by jobid;


-- ============================================================
-- TEST IN PRODUZIONE (eseguito 2026-06-19):
--   select orchestratore();          -> accoda 2 pagine-sorgente
--   select autoscale_worker();       -> pending=2, worker_lanciati=2  [OK]
-- Progressione geometrica verificata su 17 casi: nessun errore di
-- arrotondamento floating-point su log(2,n).
-- ============================================================
