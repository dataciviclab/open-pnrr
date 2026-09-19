# open-pnrr — L'Italia racconta il PNRR, riga per riga

**194 miliardi di euro, 285.000 progetti, 7 missioni. I dati ufficiali del Piano Nazionale di Ripresa e Resilienza, puliti e interrogabili.**

open-pnrr raccoglie i dati aperti pubblicati da [Italia Domani](https://www.italiadomani.gov.it) (MEF/SoGeI) e li rende interrogabili con il toolkit del Lab. Dall'idea civica al parquet pronto per l'analisi.

## Cosa contiene

| Dataset | Righe | Cosa risponde |
|---|---|---|
| `pnrr_progetti` | 291.398 | Quali progetti finanzia il PNRR, con chi, quanto, in che stato |
| `pnrr_gare` | 282.655 | Quali gare nascono dai progetti, a chi vanno, a quanto |
| `pnrr_pagamenti` | 211.901 | Quanto è stato pagato realmente (67% di assorbimento) |
| `pnrr_indicatori_target` | 357.183 | Quali target si misurano, e quanti sono stati raggiunti |
| `pnrr_avanzamento_indicatori` | 6.030 | Gli indicatori comuni europei, per missione |
| `pnrr_quadro_finanziario` | 304 | L'anagrafica di ogni misura/submisura con importi |
| `pnrr_tag_clima_digitale` | 375 | Quanto del PNRR è clima (37%) e quanto digitale (26%) |

**Totale: ~1,25 milioni di righe, 7 dataset, €194,4 mld tracciati.**

## Esempi di domande

- **Il tuo comune ha progetti PNRR?** Quanti, di che tipo, in che stato?
- **Quali ministeri gestiscono più fondi PNRR?** (RFI: €22 mld, MIMIT: €21 mld)
- **Quanto del PNRR è già stato pagato?** 67,4% — €101,9 mld su €151,1 mld
- **Le gare PNRR vanno tutte all'aggiudicazione?** 157.699 su 282.655 (56%)
- **Quanto è "verde" il PNRR?** €72 mld di contribuzione al clima
- **Quali indicatori europei sono in ritardo?** M3 (infrastrutture): 4,6% con valore

## Come accedere ai dati

### 1. Via MCP (toolkit del Lab)

```sql
-- Quali progetti PNRR sono "In Corso" in Emilia-Ragna?
SELECT cup, titolo_progetto, fin_pnrr
FROM pnrr_progetti
WHERE stato_avanzamento = 'In Corso'
  AND soggetto_attuatore LIKE '%EMILIA%'
ORDER BY fin_pnrr DESC
```

### 2. File parquet

I clean parquet sono su GCS (`gs://dataciviclab-clean/`) e nel `out/` locale dopo un `make run`.

### 3. Source Italia Domani

I CSV originali sono sul [catalogo open data del MEF](https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data.html).

## Pipeline

```text
Italia Domani (CSV) → preprocess.py (wget) → raw → clean.sql → mart*.sql → GCS
```

```bash
# Esegui tutto
make run

# Esegui un singolo dataset
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run --config datasets/pnrr-progetti/dataset.yml

# Valida
toolkit validate --config datasets/pnrr-progetti/dataset.yml
```

## Cross-dataset

| Join | Chiave | Domanda |
|---|---|---|
| `pnrr_progetti` ↔ `pnrr_gare` | CUP | I progetti diventano gare? |
| `pnrr_progetti` ↔ `pnrr_pagamenti` | CUP | Quanto è stato pagato? |
| `pnrr_indicatori_target` ↔ `pnrr_progetti` | CUP | Quali indicatori monitora ogni progetto? |
| `pnrr_quadro_finanziario` ↔ tutti | codice_univoco_submisura | Anagrafica misure/submisure |

## Fonte

**Italia Domani** — MEF / SoGeI
- [Catalogo open data](https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data.html)
- Licenza: dati pubblici (da verificare)
- Il server AEM/Akamai blocca `python-requests` — i `preprocess.py` usano wget con fallback urllib
