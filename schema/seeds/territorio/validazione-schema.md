# Validazione Schema Evento

Prima di inserire un evento in `eventi-seed/`, deve superare questi controlli.

## Checklist obbligatoria

- [ ] `nome_evento` presente e non duplicato
- [ ] `tipo_primario` corrisponde a tassonomia in `tipologie-evento.md`
- [ ] `comune` presente e verificato in `comuni_istat.csv`
- [ ] `place_id` presente nel formato IT-{REGIONE}-{PROVINCIA}-{CODICE_ISTAT}
- [ ] `place_id` verificabile in `kwf_territory_hub`
- [ ] `codice_istat` presente e corretto
- [ ] `data_o_periodo` specificata (anche generica: "terza domenica di agosto")
- [ ] `ente_organizzatore` identificato
- [ ] `fonte` di livello Primaria o Secondaria

## Campi facoltativi ma raccomandati

- `codice_belfiore` (da `codici_belfiore.csv`)
- `cap` (da `cap.csv`)
- `provincia` (da `province.csv`)
- `link_sito_ufficiale`
- `connessione_liturgica` (per feste religiose)
- `micro_territorio` (cluster culturale di appartenenza)

## Regola sui duplicati

Se un evento esiste già in altra forma (es. sagra + processione stesso giorno):
→ creare un seed unico con `tipo_secondario` invece di due file separati.

## Formato file seed

Nome file: `NNN-nome-evento-comune.md`
Esempio: `003-sagra-porchetta-ariccia.md`
