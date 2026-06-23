#!/usr/bin/env python3
import os, sys, json, hashlib, re, requests
from datetime import datetime

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}

MESI = {"gennaio":1,"febbraio":2,"marzo":3,"aprile":4,"maggio":5,"giugno":6,
        "luglio":7,"agosto":8,"settembre":9,"ottobre":10,"novembre":11,"dicembre":12}
ANNO_DEFAULT = 2026


def parse_data_iso(periodo_ricorrenza, mese_principale):
    testo = periodo_ricorrenza.strip()
    mese_num = MESI.get(mese_principale.strip().lower())
    if mese_num is None:
        return None, True, periodo_ricorrenza

    m = re.search(r"\b(\d{1,2})\s*-\s*\d{1,2}\s+([a-zàèéìòù]+)", testo, re.IGNORECASE)
    if m:
        try:
            dt = datetime(ANNO_DEFAULT, MESI.get(m.group(2).lower(), mese_num), int(m.group(1)))
            return dt.strftime("%Y-%m-%dT00:00:00+00:00"), False, None
        except ValueError:
            pass

    m = re.search(r"\b(\d{1,2})\s+([a-zàèéìòù]+)\b", testo, re.IGNORECASE)
    if m:
        try:
            dt = datetime(ANNO_DEFAULT, MESI.get(m.group(2).lower(), mese_num), int(m.group(1)))
            return dt.strftime("%Y-%m-%dT00:00:00+00:00"), False, None
        except ValueError:
            pass

    dt = datetime(ANNO_DEFAULT, mese_num, 1)
    return dt.strftime("%Y-%m-%dT00:00:00+00:00"), True, periodo_ricorrenza


def dna_hash(titolo, luogo, data_inizio):
    raw = f"{titolo}|{luogo}|{data_inizio}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def upsert_territorio(comune, provincia, regione, codice_istat):
    payload = {"istat_code": codice_istat, "nome": comune, "provincia": provincia, "regione": regione}
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/territori",
        headers={**HEADERS, "Prefer": "resolution=merge-duplicates,return=representation"},
        json=payload, params={"on_conflict": "istat_code"},
    )
    r.raise_for_status()
    data = r.json()
    if data:
        return data[0]["id"]
    r2 = requests.get(f"{SUPABASE_URL}/rest/v1/territori", headers=HEADERS,
                       params={"istat_code": f"eq.{codice_istat}", "select": "id"})
    r2.raise_for_status()
    return r2.json()[0]["id"]


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 import_territorio.py path/to/eventi.json")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ds = data["___ATLAS_EVENTA_DATASET___"]
    comune = ds["comune"]
    provincia = ds["provincia"]
    codice_istat = ds["istat_code"]
    regione = ds.get("regione", "Lazio")

    print(f"== Import {comune} ({codice_istat}) ==")

    territorio_id = upsert_territorio(comune, provincia, regione, codice_istat)
    print(f"territorio_id = {territorio_id}")

    inserted, skipped = 0, 0

    for ev in data["events"]:
        cert = ev.get("___CERTIFICATION_3620___", {})
        if not cert.get("certificato", False):
            skipped += 1
            continue

        payload_ev = ev["___PAYLOAD___"]
        titolo = payload_ev["nome_evento"]
        venue = payload_ev["venue"]
        categoria = payload_ev["categoria_primaria"]
        periodo = payload_ev.get("periodo_ricorrenza", "")
        mese_principale = payload_ev.get("mese_principale", "")

        data_iso, da_verificare, nota = parse_data_iso(periodo, mese_principale)
        if data_iso is None:
            print(f"  [SKIP] '{titolo}' — impossibile determinare data")
            skipped += 1
            continue

        loc = payload_ev.get("luogo", {})
        lat = loc.get("lat")
        lng = loc.get("lng")

        org = payload_ev.get("organizzatore", {})

        payload = {
            "dna_hash": dna_hash(titolo, venue, data_iso),
            "titolo": titolo,
            "descrizione": payload_ev.get("descrizione"),
            "categoria": categoria,
            "data_inizio": data_iso,
            "luogo": f"{venue}, {comune}",
            "lat": lat,
            "lng": lng,
            "organizzatore": org.get("nome"),
            "fonte_url": org.get("url_fonte"),
            "verificato": cert.get("certificato", False),
            "verificato_at": cert.get("timestamp_certificazione"),
            "status": "attivo",
            "tags": [comune.lower(), categoria.lower()],
            "territorio_id": territorio_id,
            "da_verificare": da_verificare,
            "note_data_originale": nota,
        }

        r = requests.post(
            f"{SUPABASE_URL}/rest/v1/eventi",
            headers={**HEADERS, "Prefer": "resolution=merge-duplicates,return=minimal"},
            json=payload, params={"on_conflict": "dna_hash"},
        )
        if r.status_code in (200, 201, 204):
            inserted += 1
            flag = " [DA VERIFICARE]" if da_verificare else ""
            print(f"  [OK] {titolo}{flag}")
        else:
            print(f"  [ERR] {titolo}: {r.status_code} {r.text}")

    print(f"\nRiepilogo: {inserted} inseriti/aggiornati, {skipped} saltati")


if __name__ == "__main__":
    main()
