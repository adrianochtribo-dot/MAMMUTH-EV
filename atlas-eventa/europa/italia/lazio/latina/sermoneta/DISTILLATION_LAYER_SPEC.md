
# DISTILLATION_LAYER™
## Specifica Ufficiale v1.0
### KREATIO UNIVERSAL SYSTEM™ — Code 3620
### Modulo: ATLAS•EVENTA™ — Data Pipeline

---

## 1. DEFINIZIONE

Il `DISTILLATION_LAYER™` è lo strato di condensazione semantica applicato agli eventi in ingestion nel database ATLAS•EVENTA™.

**Non filtra. Non esclude. Distilla.**

Prende materia grezza — eventi correlati, cluster territoriali, ridondanze visive — e produce un output stratificato che preserva la granularità territoriale nel database eliminando il rumore nel frontend.

---

## 2. STRUTTURA DEL BLOCCO JSON

Ogni record in `eventi.json` contiene obbligatoriamente il blocco `___DISTILLATION_LAYER___` come settimo blocco, dopo `___META___`:

```json
"___DISTILLATION_LAYER___": {
  "dl_flag": "STANDALONE",
  "dl_parent_gsn": null,
  "dl_children_count": 0,
  "dl_children_gsn": [],
  "dl_version": "1.0",
  "dl_trigger": null,
  "dl_notes": null
}
```

### Campi

| Campo | Tipo | Descrizione |
|---|---|---|
| `dl_flag` | string | Flag di classificazione (vedi sezione 3) |
| `dl_parent_gsn` | string \| null | GSN del record parent se CLUSTER_CHILD, null altrimenti |
| `dl_children_count` | integer | Numero di figli se CLUSTER_PARENT, 0 altrimenti |
| `dl_children_gsn` | array | Array dei GSN figli se CLUSTER_PARENT, [] altrimenti |
| `dl_version` | string | Versione della specifica applicata |
| `dl_trigger` | string \| null | Trigger che ha attivato la distillazione |
| `dl_notes` | string \| null | Note operative per developer e T.C.F.™ |

---

## 3. FLAGS

### `STANDALONE`
Evento indipendente. Nessuna relazione parent/child. La maggior parte degli eventi.

```json
"dl_flag": "STANDALONE",
"dl_parent_gsn": null,
"dl_children_count": 0,
"dl_children_gsn": [],
"dl_trigger": null
```

### `CLUSTER_PARENT`
Evento ombrello che raggruppa varianti territoriali dello stesso rito.
Il parent appare **una volta** nelle liste filtrate per categoria.
Sulla mappa mostra badge con conteggio tappe.

```json
"dl_flag": "CLUSTER_PARENT",
"dl_parent_gsn": null,
"dl_children_count": 5,
"dl_children_gsn": ["059026-...-000000024", "..."],
"dl_trigger": "CLUSTER"
```

### `CLUSTER_CHILD`
Variante territoriale di un evento CLUSTER_PARENT.
Visibile sulla mappa come PIN individuale.
Nascosto nelle liste filtrate per categoria (il parent lo rappresenta).

```json
"dl_flag": "CLUSTER_CHILD",
"dl_parent_gsn": "059026-1749216000000000000-000000001",
"dl_children_count": 0,
"dl_children_gsn": [],
"dl_trigger": "CLUSTER"
```

### `MERGED`
Due componenti distinte (es. religiosa + storica) dello stesso evento weekend
unificate in un unico record per evitare duplicazione.

```json
"dl_flag": "MERGED",
"dl_trigger": "MERGE",
"dl_notes": "Componente religiosa (sab) + storica (dom) unificate. Stesso weekend, organizzatore e luogo."
```

### `ABSORBED`
Evento contenuto all'interno di un cartellone più ampio.
L'evento figlio è stato assorbito nel record ombrello.
Non creare record separati per sotto-eventi già descritti nell'ombrello.

```json
"dl_flag": "ABSORBED",
"dl_trigger": "ABSORB",
"dl_notes": "Cartellone ombrello. Non duplicare con evento separato."
```

---

## 4. TRIGGER

| Trigger | Attivazione |
|---|---|
| `CLUSTER` | Stesso rito replicato in location/date diverse nel territorio comunale |
| `MERGE` | Due componenti (religiosa + storica, religiosa + gastronomica) dello stesso weekend |
| `ABSORB` | Evento contenuto in cartellone più ampio già presente come record |
| `null` | Nessuna distillazione applicata (STANDALONE) |

---

## 5. COMPORTAMENTO FRONTEND

### Vista mappa (PIN)
- `CLUSTER_PARENT` → PIN con badge numerico (es. "6 tappe")
- `CLUSTER_CHILD` → PIN individuale nel territorio
- `STANDALONE` → PIN standard
- `MERGED` → PIN standard
- `ABSORBED` → PIN del parent che lo contiene

### Vista lista / filtro categoria
- `CLUSTER_PARENT` → appare **1 volta** con badge espandibile
- `CLUSTER_CHILD` → **nascosto** (rappresentato dal parent)
- `STANDALONE` → appare normalmente
- `MERGED` → appare normalmente
- `ABSORBED` → **nascosto** (rappresentato dall'ombrello)

### MAMMUTH•KeySLIDE™
- Click su PIN `CLUSTER_CHILD` → apre KeySLIDE con dati del figlio (location e data specifici)
- Click su PIN `CLUSTER_PARENT` → apre KeySLIDE con lista tappe espandibile

---

## 6. REGOLE T.C.F.™ DI VALIDAZIONE

Il T.C.F.™ (Total Coherence Framework) valida i seguenti vincoli prima di ogni ingestion:

1. **Ogni record DEVE avere `___DISTILLATION_LAYER___`** — schema_version >= 2.0.0
2. **`CLUSTER_CHILD` DEVE avere `dl_parent_gsn` non null** — punta a un record esistente
3. **`CLUSTER_PARENT` DEVE avere `dl_children_count` > 0 e `dl_children_gsn` non vuoto**
4. **`dl_children_gsn` DEVE contenere GSN validi** — formato `059026-NANOSECONDS-SEQUENCE`
5. **`ABSORBED` non duplica** — verificare che il record ombrello esista nel dataset
6. **`dl_version` DEVE corrispondere alla versione corrente della spec**

---

## 7. DATASET SERMONETA — STATO ATTUALE

**File:** `atlas-eventa/europa/italia/lazio/latina/sermoneta/eventi.json`
**Schema version:** 2.0.0
**Dataset ID:** DS-SERM-059026-2026-002
**Total events:** 34
**DISTILLATION_LAYER version:** 1.0

### Distribuzione flags

| Flag | Count | Note |
|---|---|---|
| STANDALONE | 26 | Eventi indipendenti |
| CLUSTER_PARENT | 1 | Ciclo Polenta Sant'Antonio Abate |
| CLUSTER_CHILD | 5 | Polenta: Doganella, Scalo, Tufette, Pontenuovo, Monticchio |
| MERGED | 1 | Rievocazione Lepanto + Madonna della Vittoria |
| ABSORBED | 1 | Favole di Natale (assorbe apertura 8 dicembre) |

### Cluster attivi

| GSN Parent | Nome | Children |
|---|---|---|
| `059026-1749216000000000000-000000001` | Ciclo Polenta Sant'Antonio Abate | 5 borgate |

---

## 8. ESTENSIONE AD ALTRI COMUNI

Quando ATLAS•EVENTA™ si espande a nuovi comuni, applicare:

1. Identificare cluster territoriali (stesso rito, date diverse, borgate diverse)
2. Creare 1 record CLUSTER_PARENT + N record CLUSTER_CHILD
3. Verificare eventi composti (religiosi + storici) → MERGED
4. Verificare cartelloni ombrello → ABSORBED
5. Tutti gli altri → STANDALONE
6. Validare con T.C.F.™ prima del commit

---

## 9. VERSIONING

| Versione | Data | Autore | Note |
|---|---|---|---|
| 1.0 | 2026-06-11 | op_adriano_001 | Prima release. Applicata a DS-SERM-059026-2026-002 |

---

*DISTILLATION_LAYER™ è un componente proprietario di KREATIO UNIVERSAL SYSTEM™ — Code 3620*
*© MAMMUTH•EVENTS™ — All rights reserved*
