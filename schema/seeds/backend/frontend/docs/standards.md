# KREATIO UNIVERSAL SYSTEM™ - STANDARDS
# CODE: 3620
# SUBJECT: Guida Operativa KWF (K•Word•Festival)

## 1. Geolocalizzazione
Ogni istanza di evento (INSTANCE_ID) DEVE includere obbligatoriamente:
- `plus_code` (TEXT): Codice standard per geolocalizzazione in aree prive di indirizzo.
- `lat_long` (DECIMAL/POINT): Coordinate geografiche WGS 84.

## 2. Finanza
Per ogni evento che prevede oneri o costi, è obbligatorio:
- `currency_code` (ISO-4217): Codice valuta a 3 lettere (es. EUR).

## 3. Tempo e Calendario
Gestione rigorosa della temporalità:
- `date_time` (ISO-8601): Formato YYYY-MM-DDTHH:MM:SSZ.
- `tz_database_name` (TEXT): Identificativo fuso orario (es. Europe/Rome).

## 4. Internazionalizzazione
Per la gestione multilingua dei metadati evento:
- `lang_code` (ISO-639-1): Codice lingua a due lettere (es. it, en, es).

───────────────
Leonardo Adriano Chelariu Founder & Author (KREATIO UNIVERSAL SYSTEM™ • Code 3620) K•Word•Festival (KWF) Ð I ⅅΓ•ⅅΛΞ•Ƨ⊥ⅅΛΞ ───────────────
