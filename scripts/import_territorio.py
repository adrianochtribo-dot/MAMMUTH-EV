#!/usr/bin/env python3
"""
KREATIO UNIVERSAL SYSTEM™ — Code 3620
Import automatico di un JSON Worker Territoriale (formato standard)
nelle tabelle Supabase: territori + eventi.

Solo record con stato_verifica in (verified, certified) vengono importati.
Idempotente: usa upsert su dna_hash (eventi) e istat_code (territori).

Uso:
    python3 import_territorio.py path/to/comune.json

Richiede variabili d'ambiente:
    SUPABASE_URL
    SUPABASE_SERVICE_KEY
"""

import os
import sys
import json
import hashlib
import requests

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}


def dna_hash(titolo, luogo, data_inizio):
    raw = f"{titolo}|{luogo}|{data_inizio}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def upsert_territorio(comune, provincia, regione, codice_istat):
    payload = {
        "istat_code": codice_istat,
        "nome": comune,
        "provincia": provincia,
        "regione": regione,
    }
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/territori",
        headers={**HEADERS, "Prefer": "resolution=merge-duplicates,return=representation"},
        json=payload,
        params={"on_conflict": "istat_code"},
    )
    r.raise_for_status()
    data = r.json()
    if data:
        return data[0]["id"]
    # fallback: fetch existing
    r2 = requests.get(
        f"{SUPABASE_URL}/rest/v1/territori",
        headers=HEADERS,
        params={"istat_code": f"eq.{codice_istat}", "select": "id"},
    )
    r2.raise_for_status()
    return r2.json()[0]["id"]


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 import_territorio.py path/to/comune.json")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    comune = data["comune"]
    provincia = data["provincia"]
    codice_istat = data["codice_istat"]
    regione = data.get("regione", "Lazio")

    print(f"== Import {comune} ({codice_istat}) ==")

    territorio_id = upsert_territorio(comune, provincia, regione, codice_istat)
    print(f"territorio_id = {territorio_id}")

    inserted, skipped = 0, 0

    for mese, eventi in data["calendario_ciclico_12_mesi"].items():
        for ev in eventi:
            stato = ev.get("stato_verifica", "unverified")
            if stato not in ("verified", "certified"):
                skipped += 1
                continue

            # periodo -> data stimata: richiede campo esplicito 'data_iso' nel JSON
            data_iso = ev.get("data_iso")
            if not data_iso:
                print(f"  [SKIP] '{ev['evento_nome']}' — manca 'data_iso' (richiesto per import)")
                skipped += 1
                continue

            lat, lng = (ev["coordinate"].split(",") if "coordinate" in ev
                         else (ev.get("lat"), ev.get("lng")))

            titolo = ev["evento_nome"]
            luogo = ev["anchor_luogo"]

            payload = {
                "dna_hash": dna_hash(titolo, luogo, data_iso),
                "titolo": titolo,
                "categoria": ev["tipo"],
                "data_inizio": data_iso,
                "orario_inizio": ev.get("orario", "00:00-00:00").split("-")[0] or None,
                "orario_fine": ev.get("orario", "00:00-00:00").split("-")[-1] or None,
                "luogo": f"{luogo}, {comune}",
                "lat": float(lat),
                "lng": float(lng),
                "fonte_url": ev.get("fonte_verifica"),
                "verificato": True,
                "verificato_da": ev.get("verificato_da"),
                "verificato_at": ev.get("data_verifica"),
                "status": "attivo",
                "tags": [comune.lower(), ev["tipo"].lower(), stato],
                "territorio_id": territorio_id,
            }

            r = requests.post(
                f"{SUPABASE_URL}/rest/v1/eventi",
                headers={**HEADERS, "Prefer": "resolution=merge-duplicates,return=minimal"},
                json=payload,
                params={"on_conflict": "dna_hash"},
            )
            if r.status_code in (200, 201, 204):
                inserted += 1
                print(f"  [OK] {titolo}")
            else:
                print(f"  [ERR] {titolo}: {r.status_code} {r.text}")

    print(f"\nRiepilogo: {inserted} inseriti/aggiornati, {skipped} saltati (unverified o senza data_iso)")


if __name__ == "__main__":
    main()
