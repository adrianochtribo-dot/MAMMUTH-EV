import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
);

const WORKER_ID = `borgovia-${crypto.randomUUID().slice(0, 8)}`;

const SOGLIA_AUTO = 75;
const SOGLIA_ONE_WORKER = 50;
const SOGLIA_TERRITORIALE_AUTO = 75;
const SOGLIA_FUZZY = 0.82;

const ORIGINI_FIDATE = ["MANUAL_LOCKED", "MANUAL_CONFIRM"];

function norm(s: unknown): string {
  return String(s ?? "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9 ]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function tokens(s: unknown): Set<string> {
  return new Set(norm(s).split(" ").filter((t) => t.length > 1));
}

function jaccard(a: Set<string>, b: Set<string>): number {
  if (a.size === 0 || b.size === 0) return 0;
  let inter = 0;
  for (const t of a) if (b.has(t)) inter++;
  return inter / (a.size + b.size - inter);
}

function comuneFromUrl(url: unknown): string | null {
  const m = String(url ?? "").match(/comune\.([a-z]+)\./i);
  return m ? m[1] : null;
}

function giornoISO(d: unknown): string | null {
  if (!d) return null;
  const t = new Date(String(d));
  return isNaN(t.getTime()) ? null : t.toISOString().slice(0, 10);
}

function ontologico(r: Record<string, unknown>, categorieFidate: Set<string>, degradata: boolean) {
  const dett: Record<string, unknown> = {};
  let score = 0;

  const titoloOk = !!r.titolo && String(r.titolo).trim().length > 3;
  if (titoloOk) score += 25;
  dett.titolo_sano = titoloOk;

  const cat = r.categoria ? String(r.categoria).trim() : "";
  const catOk = degradata
    ? (cat.length > 0 && cat !== "da_classificare")
    : (cat.length > 0 && cat !== "da_classificare" && categorieFidate.has(cat));
  if (catOk) score += 40;
  dett.categoria = cat || null;
  dett.categoria_valida = catOk;
  dett.modalita = degradata ? "degradata" : "insieme_fidato";

  const haInizio = !!r.data_inizio;
  let dateOk = haInizio;
  if (haInizio && r.data_fine) {
    dateOk = new Date(String(r.data_fine)).getTime() >= new Date(String(r.data_inizio)).getTime();
  }
  if (dateOk) score += 35;
  dett.date_coerenti = dateOk;

  return { score, dettaglio: dett };
}

function territoriale(r: Record<string, unknown>, mappaTerritori: Map<string, { id: number; nome: string }>) {
  const luogoN = norm(r.luogo);
  const comuneUrl = comuneFromUrl(r.fonte_url);
  const comuneUrlN = comuneUrl ? norm(comuneUrl) : "";

  let match = luogoN ? mappaTerritori.get(luogoN) : undefined;
  if (!match && comuneUrlN) match = mappaTerritori.get(comuneUrlN);

  let score: number;
  let motivo: string;
  if (match) {
    score = 100;
    motivo = `risolto a territorio "${match.nome}" (id ${match.id})`;
  } else if (luogoN) {
    score = 40;
    motivo = `luogo "${r.luogo}" presente ma non corrisponde a nessun territorio noto`;
  } else {
    score = 0;
    motivo = "nessun luogo";
  }

  return { score, territorio_id: match ? match.id : null, territorio_nome: match ? match.nome : null, motivo };
}

function fuzzyDuplicato(r: Record<string, unknown>, esistenti: { titolo: string; giorno: string | null }[]) {
  const tk = tokens(r.titolo);
  const g = giornoISO(r.data_inizio);
  let best = 0;
  let titoloSimile: string | null = null;
  for (const e of esistenti) {
    const sim = jaccard(tk, tokens(e.titolo));
    const stessaData = g && e.giorno ? g === e.giorno : true;
    if (sim > best && stessaData) {
      best = sim;
      titoloSimile = e.titolo;
    }
  }
  return { similarita: Number(best.toFixed(3)), titoloSimile, duplicato: best >= SOGLIA_FUZZY };
}

function auditabilita(r: Record<string, unknown>) {
  return {
    tracciabile: !!r.fonte_url,
    raw_payload: !!r.raw_payload,
    audit_log: true,
  };
}

Deno.serve(async () => {
  const { data: catRows } = await supabase
    .from("eventi").select("categoria").in("validation_origin", ORIGINI_FIDATE);
  const categorieFidate = new Set(
    (catRows || []).map((c: Record<string, unknown>) => String(c.categoria || "").trim()).filter(Boolean)
  );
  const degradata = categorieFidate.size === 0;

  const { data: terrRows } = await supabase.from("territori").select("id, nome");
  const mappaTerritori = new Map<string, { id: number; nome: string }>();
  for (const t of (terrRows || []) as { id: number; nome: string }[]) {
    if (t.nome) mappaTerritori.set(norm(t.nome), { id: t.id, nome: t.nome });
  }

  const { data: eventiEsistenti } = await supabase.from("eventi").select("titolo, data_inizio");
  const esistenti = ((eventiEsistenti || []) as Record<string, unknown>[]).map((e) => ({
    titolo: String(e.titolo || ""),
    giorno: giornoISO(e.data_inizio),
  }));

  const { data: righe, error } = await supabase
    .from("eventi_staging").select("*").eq("stato_validazione", "pending").limit(50);

  if (error) return json({ ok: false, step: "select", error: error.message });
  if (!righe || righe.length === 0) {
    return json({ ok: true, message: "Nessun pending da validare", categorie_fidate: [...categorieFidate] });
  }

  const esito = { approvati: 0, quarantena: 0, rifiutati: 0, errori: 0, dettaglio: [] as unknown[] };

  for (const r of righe) {
    const ont = ontologico(r, categorieFidate, degradata);
    const terr = territoriale(r, mappaTerritori);
    const fuzzy = fuzzyDuplicato(r, esistenti);

    let dupEsatto = false;
    if (r.dna_hash) {
      const { data: dh } = await supabase.from("eventi").select("dna_hash").eq("dna_hash", String(r.dna_hash)).limit(1);
      dupEsatto = !!(dh && dh.length > 0);
    }
    const anti = { dup_esatto: dupEsatto, fuzzy_similarita: fuzzy.similarita, fuzzy_duplicato: fuzzy.duplicato, titolo_simile: fuzzy.titoloSimile };
    const audit = auditabilita(r);

    let lane: string;
    let esitoStr: string;
    let promuovi = false;

    if (dupEsatto) {
      lane = "n/a"; esitoStr = "rejected (dup esatto)";
    } else if (fuzzy.duplicato) {
      lane = "one_worker"; esitoStr = "quarantine (dup fuzzy)";
    } else if (ont.score >= SOGLIA_AUTO && terr.score >= SOGLIA_TERRITORIALE_AUTO) {
      lane = "auto"; esitoStr = "approved"; promuovi = true;
    } else if (ont.score >= SOGLIA_ONE_WORKER) {
      lane = "one_worker"; esitoStr = "approved"; promuovi = true;
    } else {
      lane = "one_worker"; esitoStr = "quarantine (score basso)";
    }

    const verdetto = {
      tcf_versione: "borgovia-v2 (4 pilastri reali)",
      ontologico: ont,
      territoriale: terr,
      antirumore: anti,
      auditabilita: audit,
      lane,
      esito: esitoStr,
    };
    const verdettoStr = JSON.stringify(verdetto);

    await supabase.from("borgovia_audit").insert({
      staging_id: r.staging_id,
      dna_hash: r.dna_hash ?? null,
      titolo: r.titolo ?? null,
      score_ontologico: ont.score,
      score_territoriale: terr.score,
      territorio_id_risolto: terr.territorio_id,
      dup_esatto: dupEsatto,
      fuzzy_similarita: fuzzy.similarita,
      fuzzy_duplicato: fuzzy.duplicato,
      lane,
      esito: esitoStr,
      verdetto,
      worker_id: WORKER_ID,
    });

    if (dupEsatto) {
      await supabase.from("eventi_staging").update({ stato_validazione: "rejected", confidence_score: ont.score, borgovia_verdetto: verdettoStr }).eq("staging_id", r.staging_id);
      esito.rifiutati++;
      esito.dettaglio.push({ staging_id: r.staging_id, titolo: r.titolo, ont: ont.score, terr: terr.score, esito: esitoStr });
      continue;
    }
    if (!promuovi) {
      await supabase.from("eventi_staging").update({ stato_validazione: "quarantine", confidence_score: ont.score, borgovia_verdetto: verdettoStr }).eq("staging_id", r.staging_id);
      esito.quarantena++;
      esito.dettaglio.push({ staging_id: r.staging_id, titolo: r.titolo, ont: ont.score, terr: terr.score, esito: esitoStr });
      continue;
    }

    const { error: insErr } = await supabase.from("eventi").upsert({
      dna_hash: r.dna_hash,
      titolo: r.titolo,
      sottotitolo: r.sottotitolo ?? null,
      descrizione: r.descrizione ?? null,
      categoria: r.categoria,
      sottocategoria: r.sottocategoria ?? null,
      data_inizio: r.data_inizio,
      data_fine: r.data_fine ?? null,
      orario_inizio: r.orario_inizio ?? null,
      orario_fine: r.orario_fine ?? null,
      luogo: r.luogo,
      indirizzo: r.indirizzo ?? null,
      territorio_id: terr.territorio_id ?? r.territorio_id ?? null,
      gratuito: r.gratuito ?? null,
      prezzo_min: r.prezzo_min ?? null,
      prezzo_max: r.prezzo_max ?? null,
      organizzatore: r.organizzatore ?? null,
      fonte_url: r.fonte_url ?? null,
      tags: r.tags ?? null,
      lat: r.lat ?? null,
      lng: r.lng ?? null,
      ricorrenza: r.ricorrenza ?? null,
      da_verificare: true,
      verificato: false,
      in_scope_pilot: false,
      validation_status: "VALIDATED",
      validation_origin: "CRAWLER_AUTO",
      validation_lane: lane,
      reputation_score: ont.score,
      corroboration_count: 1,
    }, { onConflict: "dna_hash", ignoreDuplicates: true });

    if (insErr) {
      await supabase.from("eventi_staging").update({ confidence_score: ont.score, borgovia_verdetto: `errore: ${insErr.message}` }).eq("staging_id", r.staging_id);
      esito.errori++;
      esito.dettaglio.push({ staging_id: r.staging_id, titolo: r.titolo, esito: "errore", error: insErr.message });
      continue;
    }

    await supabase.from("eventi_staging").update({ stato_validazione: "approved", confidence_score: ont.score, borgovia_verdetto: verdettoStr }).eq("staging_id", r.staging_id);
    esito.approvati++;
    esito.dettaglio.push({ staging_id: r.staging_id, titolo: r.titolo, ont: ont.score, terr: terr.score, territorio_id: terr.territorio_id, lane, esito: esitoStr });
  }

  return json({
    ok: true,
    worker: WORKER_ID,
    modalita_categorie: degradata ? "degradata" : "insieme_fidato",
    categorie_fidate: [...categorieFidate],
    territori_caricati: mappaTerritori.size,
    eventi_confronto_fuzzy: esistenti.length,
    processati: righe.length,
    ...esito,
  });
});

function json(obj: unknown) {
  return new Response(JSON.stringify(obj, null, 2), { headers: { "Content-Type": "application/json" } });
}
