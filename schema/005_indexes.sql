-- Indici per performance ottimali su query territoriali ed eventi
CREATE INDEX idx_event_instances_event_id ON kwf_event_instances(event_id);
CREATE INDEX idx_event_instances_place_id ON kwf_event_instances(place_id);
CREATE INDEX idx_postal_codes_place_id ON kwf_postal_codes(place_id);
CREATE INDEX idx_belfiore_codes_place_id ON kwf_belfiore_codes(place_id);
CREATE INDEX idx_fiscal_registry_vat ON kwf_fiscal_registry(vat_number);
