CREATE TABLE kwf_financial_economic_hub (
    funding_id INTEGER PRIMARY KEY,
    budget_amount REAL,
    currency TEXT DEFAULT 'EUR'
);

CREATE TABLE kwf_public_funding (
    funding_id INTEGER PRIMARY KEY,
    source_name TEXT NOT NULL,
    FOREIGN KEY(funding_id) REFERENCES kwf_financial_economic_hub(funding_id)
);
