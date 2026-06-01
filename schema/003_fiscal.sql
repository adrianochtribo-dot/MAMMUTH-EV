CREATE TABLE kwf_fiscal_registry (
    vat_number TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    fiscal_type TEXT NOT NULL
);

CREATE TABLE kwf_associations (
    vat_number TEXT PRIMARY KEY,
    FOREIGN KEY(vat_number) REFERENCES kwf_fiscal_registry(vat_number)
);

CREATE TABLE kwf_pro_loco (
    vat_number TEXT PRIMARY KEY,
    FOREIGN KEY(vat_number) REFERENCES kwf_fiscal_registry(vat_number)
);

CREATE TABLE kwf_public_bodies (
    vat_number TEXT PRIMARY KEY,
    FOREIGN KEY(vat_number) REFERENCES kwf_fiscal_registry(vat_number)
);
