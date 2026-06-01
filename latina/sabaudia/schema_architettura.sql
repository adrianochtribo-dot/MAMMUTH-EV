-- MAMMUTH•EVENTS™: SCHEMA DI ARCHITETTURA CORE 3620™
-- Versione: 1.0.0 (GitHub Managed)

-- 1. HUB GEOGRAFICO E TERRITORIALE NAZIONALE
CREATE TABLE kwf_territory_hub (
    place_id TEXT PRIMARY KEY CHECK(length(place_id) = 6),
    comune_name_normalized TEXT NOT NULL,
    belfiore_code TEXT NOT NULL UNIQUE CHECK(length(belfiore_code) = 4),
    cap TEXT NOT NULL CHECK(length(cap) = 5),
    inps_headquarters_code TEXT NOT NULL,
    asl_regional_code TEXT NOT NULL
);

-- 2. REGISTRO FISCALE E FATTURAZIONE
CREATE TABLE kwf_fiscal_registry (
    vat_number TEXT PRIMARY KEY CHECK(length(vat_number) = 11),
    fiscal_code TEXT NOT NULL UNIQUE CHECK(length(fiscal_code) IN (11, 16)),
    ipa_code TEXT DEFAULT NULL CHECK(length(ipa_code) = 6),
    sdi_code TEXT NOT NULL DEFAULT '0000000' CHECK(length(sdi_code) = 7)
);

-- 3. ATTIVITÀ ECONOMICHE E TRACCIABILITÀ
CREATE TABLE kwf_financial_economic_hub (
    rea_number TEXT PRIMARY KEY,
    vat_number TEXT NOT NULL,
    ateco_code TEXT NOT NULL,
    abi_code TEXT NOT NULL CHECK(length(abi_code) = 5),
    cab_code TEXT NOT NULL CHECK(length(cab_code) = 5),
    FOREIGN KEY (vat_number) REFERENCES kwf_fiscal_registry(vat_number)
);

-- 4. APPALTI E FINANZIAMENTI
CREATE TABLE kwf_public_funding (
    funding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cig_code TEXT DEFAULT NULL CHECK(length(cig_code) = 10),
    cup_code TEXT DEFAULT NULL CHECK(length(cup_code) = 15)
);

-- 5. IL MONOLITO: ISTANZE EVENTO
CREATE TABLE kwf_events_instances (
    instance_id INTEGER PRIMARY KEY,
    place_id TEXT NOT NULL,
    vat_number TEXT NOT NULL,
    funding_id INTEGER DEFAULT NULL,
    event_name_normalized TEXT NOT NULL,
    category TEXT NOT NULL,
    date_start TEXT NOT NULL,
    date_end TEXT NOT NULL,
    FOREIGN KEY (place_id) REFERENCES kwf_territory_hub(place_id),
    FOREIGN KEY (vat_number) REFERENCES kwf_fiscal_registry(vat_number),
    FOREIGN KEY (funding_id) REFERENCES kwf_public_funding(funding_id)
);
