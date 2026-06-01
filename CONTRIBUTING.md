# Guida alla Collaborazione - MAMMUTH•EVENTS™

Grazie per il tuo interesse nel contribuire a **MAMMUTH•EVENTS™**! Questo progetto si basa sulla trasparenza e sulla partecipazione attiva per costruire un'infrastruttura di verità territoriale.

## Come Contribuire

Ci sono molti modi per supportare l'ecosistema:

### 1. Segnalazione di Bug
Se riscontri malfunzionamenti nel protocollo o nell'infrastruttura, apri una nuova [Issue](https://github.com/adrianochtribo-dot/MAMMUTH-EVENTS-LAZIO/issues). Assicurati di utilizzare il template "Segnalazione Bug" e di includere i passaggi necessari per riprodurre il problema.

### 2. Proposte di Miglioramento
Il protocollo è in costante evoluzione. Se hai idee per migliorare il flusso di partecipazione o l'integrazione dei dati:
*   Apri una Issue descrivendo l'idea.
*   Discutiamone insieme prima di procedere con modifiche sostanziali.

### 3. Contributi al Codice
*   Effettua il fork del repository.
*   Crea un branch dedicato per la tua modifica (`git checkout -b feature/nome-miglioramento`).
*   Apporta le modifiche seguendo lo stile del progetto.
*   Invia una Pull Request descrivendo chiaramente l'impatto della tua modifica sul protocollo.

## Codice di Condotta
Questo progetto promuove un ambiente inclusivo e rispettoso. Ogni contributo deve essere orientato alla costruzione di una "verità territoriale" condivisa e al benessere della community.

---
*KREATIO UNIVERSAL SYSTEM™ - Regional pilot infrastructure for territorial event truth.*
## 3. Aggiungere un Evento Seed

Per contribuire con un nuovo evento del micro-territorio:

1. Copia il file `schema/seeds/eventi-seed/_TEMPLATE.md`
2. Rinominalo come `NNN-nome-evento-comune.md`
3. Compila tutti i campi obbligatori (vedi `territorio/validazione-schema.md`)
4. Verifica il `place_id` nel formato `IT-{REGIONE}-{PROVINCIA}-{CODICE_ISTAT}`
5. Scegli il `micro_territorio` da `eventi-seed/geo/micro-territori.md`
6. Apri una Pull Request con commit message: `feat: add NNN-nome-evento-comune.md seed`

### Campi obbligatori
- `nome_evento`
- `tipo_primario` (da `territorio/tipologie-evento.md`)
- `comune` + `place_id`
- `data_o_periodo`
- `ente_organizzatore`
- `fonte` di livello primaria o secondaria

### Fonti accettate
Consulta `territorio/fonti-dati.md` per i livelli di qualità accettati.

### Seed di riferimento
- `001-valvisciolo.md` → heritage/abbazia
- `002-sagra-porchetta-ariccia.md` → sagra enogastronomica
- `003-palio-ronciglione.md` → palio/rievocazione storica
