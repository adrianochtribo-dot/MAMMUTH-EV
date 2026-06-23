-- ============================================================
-- MAMMUTH-EV — MIGRATION 2026-06-20
-- Comando unico: processa_comune() / aggiungi_comune()
-- ============================================================
--
-- CONTESTO
-- "Scrivo un posto e BORGOVIA esegue tutto." Due funzioni che,
-- dato il nome di un comune, accodano il crawl e lanciano i
-- worker con UN comando solo. Il flusso prosegue da se':
-- crawl_queue -> crawl-worker -> eventi_staging -> BORGOVIA -> eventi.
--
-- processa_comune(nome)      : accoda un comune che ha gia' una
--                              sorgente attiva in crawl_sources.
-- aggiungi_comune(nome, url) : registra una sorgente nuova e la
--                              accoda subito.
--
-- DIPENDENZE (gia' esistenti nel DB):
--   - crawl_sources (id, domain, base_url, active, ...)
--   - crawl_queue   (source_id, target_url, status, priority, ...)
--   - autoscale_worker()  : lancia i worker leggendo la key dal Vault
--
-- NOTA / DEBITO TECNICO (2026-06-20)
-- Test su Cori (source 5): il sito comune.cori.lt.it risponde 403
-- ai bot, quindi il crawler non entra (eventi_staging = 0).
-- PROSSIMO PASSO: nel crawl-worker, aggiungere header da browser
-- vero (User-Agent Chrome, Accept, Accept-Language) alla fetch(),
-- per superare i blocchi anti-bot. Sblocca Cori e tutti i comuni
-- che rifiutano i crawler.
-- ============================================================


-- ------------------------------------------------------------
-- 1) processa_comune(nome) — comune con sorgente gia' attiva
-- ------------------------------------------------------------
create or replace function processa_comune(p_nome text)
returns text as $func$
declare
  v_source crawl_sources%rowtype;
  v_nome text := lower(trim(p_nome));
begin
  select * into v_source
  from crawl_sources
  where active = true
    and (lower(domain) like '%'||v_nome||'%' or lower(base_url) like '%'||v_nome||'%')
  limit 1;

  if v_source.id is null then
    return 'NESSUNA_SORGENTE: «'||p_nome||'» non ha una fonte attiva. Usa aggiungi_comune() per registrarla.';
  end if;

  insert into crawl_queue(source_id, target_url, status, attempts, priority, created_at, updated_at)
  values (v_source.id, v_source.base_url, 'pending', 0, 100, now(), now());

  perform autoscale_worker();

  return 'OK: «'||p_nome||'» accodato (source '||v_source.id||', '||v_source.domain||') e worker lanciati. Estrazione in corso.';
end;
$func$ language plpgsql;


-- ------------------------------------------------------------
-- 2) aggiungi_comune(nome, url) — registra sorgente nuova + accoda
-- ------------------------------------------------------------
create or replace function aggiungi_comune(p_nome text, p_url text)
returns text as $func$
declare
  v_domain text;
  v_id bigint;
begin
  v_domain := regexp_replace(p_url, '^https?://([^/]+).*$', '\1');

  select id into v_id from crawl_sources where domain = v_domain limit 1;
  if v_id is null then
    insert into crawl_sources(domain, base_url, robots_checked, robots_allowed, min_delay_sec, active, created_at)
    values (v_domain, p_url, false, true, 2, true, now())
    returning id into v_id;
  else
    update crawl_sources set base_url = p_url, active = true where id = v_id;
  end if;

  insert into crawl_queue(source_id, target_url, status, attempts, priority, created_at, updated_at)
  values (v_id, p_url, 'pending', 0, 100, now(), now());

  perform autoscale_worker();

  return 'OK: «'||p_nome||'» registrato (source '||v_id||', '||v_domain||') e accodato. Estrazione in corso.';
end;
$func$ language plpgsql;


-- ------------------------------------------------------------
-- USO
-- ------------------------------------------------------------
-- comune che ha gia' la sorgente:
--   select processa_comune('Terracina');
--
-- comune nuovo (registra fonte + accoda):
--   select aggiungi_comune('Cori', 'https://www.comune.cori.lt.it/it/novita/cultura-eventi-e-manifestazioni');
--
-- VERIFICA (regola: conta la destinazione, non la coda):
--   select count(*) from eventi_staging where fonte_url like '%cori%';
-- ============================================================
