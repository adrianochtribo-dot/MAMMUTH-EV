-- KREATIO UNIVERSAL SYSTEM™ - MODULE 3620
-- Tassonomia Globale e Standard di Localizzazione

-- 1. Tassonomia Eventi KWF
CREATE TABLE kwf_event_taxonomy (
    code TEXT PRIMARY KEY, -- es: FEST-REL, SAGR-GAST
    description TEXT NOT NULL,
    unesco_mapping TEXT
);

INSERT INTO kwf_event_taxonomy VALUES 
('FEST-REL', 'Feste Religiose e Processioni', 'Patrimonio Immateriale'),
('SAGR-GAST', 'Sagre Enogastronomiche', 'Tradizione Culinaria'),
('PAL-TRAD', 'Pali e Rievocazioni Storiche', 'Tradizione Storica'),
('FOLK-MUS', 'Musica e Danze Folkloristiche', 'Tradizione Artistica');

-- 2. Supporto Standard Globali (Riferimento)
CREATE TABLE kwf_global_standards (
    standard_name TEXT PRIMARY KEY, -- ISO-3166, ISO-4217, ISO-8601
    usage_context TEXT
);

INSERT INTO kwf_global_standards VALUES 
('ISO-3166', 'Geolocalizzazione e Confini (Alpha-2/3)'),
('ISO-4217', 'Codici Valute per Transazioni'),
('ISO-8601', 'Formato Data/Ora Universale'),
('ISO-639-1', 'Standard Lingue per Internazionalizzazione');
