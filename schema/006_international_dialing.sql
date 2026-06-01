-- KREATIO UNIVERSAL SYSTEM™ - MODULE 3620
-- Gestione Prefissi Internazionali ITU

CREATE TABLE kwf_international_dialing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone TEXT NOT NULL,
    country_name TEXT NOT NULL,
    country_code TEXT NOT NULL -- Formato '+X'
);

-- Esempio di popolamento (Macro-struttura)
INSERT INTO kwf_international_dialing (zone, country_name, country_code) VALUES 
('Zona 1', 'Stati Uniti, Canada', '+1'),
('Zona 3', 'Italia', '+39'),
('Zona 4', 'Germania', '+49'),
('Zona 8', 'Cina', '+86');
-- (Inserire qui l'elenco completo fornito)
