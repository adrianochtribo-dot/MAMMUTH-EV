"""
MAMMUTH•EVENTS™ — Safety Engine
Module: supabase_client.py
Supabase client per integrazione ATLAS•EVENTA™
KREATIO UNIVERSAL SYSTEM™ — Code 3620
"""

import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "")


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_URL e SUPABASE_ANON_KEY devono essere configurate "
            "come variabili d'ambiente."
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_events_by_comune(istat_comune: str) -> list[dict]:
    client = get_supabase_client()
    response = (
        client.table("events")
        .select("*")
        .eq("istat_comune", istat_comune)
        .execute()
    )
    return response.data or []


def fetch_event_by_id(event_id: str) -> dict | None:
    client = get_supabase_client()
    response = (
        client.table("events")
        .select("*")
        .eq("id", event_id)
        .single()
        .execute()
    )
    return response.data
