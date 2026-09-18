# open-pnrr

Dataset aperti sul PNRR (Piano Nazionale di Ripresa e Resilienza) da Italia Domani (MEF/SoGeI).

## Dati

7 dataset, ~1.25 milioni di righe, copertura 2021-2026:

| Dataset | Righe | Contenuto |
|---|---|---|
| [pnrr_progetti](datasets/pnrr-progetti) | 291.398 | Anagrafica progetti: CUP, finanziamenti, stato avanzamento |
| [pnrr_gare](datasets/pnrr-gare) | 282.655 | Gare d'appalto: CUP→CIG, importi, procedura, oggetto |
| [pnrr_pagamenti](datasets/pnrr-pagamenti) | 211.901 | Pagamenti effettivi: finanziamento vs erogato per fonte |
| [pnrr_indicatori_target](datasets/pnrr-indicatori-target) | 357.183 | Indicatori target per CUP: valore realizzato vs programmato |
| [pnrr_avanzamento_indicatori](datasets/pnrr-avanzamento-indicatori) | 6.030 | Indicatori comuni europei: valore per submisura/misura |
| [pnrr_quadro_finanziario](datasets/pnrr-quadro-finanziario) | 304 | Anagrafica misure/submisure con importi programmazione |
| [pnrr_tag_clima_digitale](datasets/pnrr-tag-clima-digitale) | 375 | TAG clima/digitale: campi intervento UE, coeff., importi |

### Pipeline

```
Italia Domani (CSV) → preprocess.py (wget) → raw → clean.sql → mart*.sql
```

### Uso rapido

```bash
# Esegui tutti i dataset
make run

# Esegui un singolo dataset
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run --config datasets/pnrr-progetti/dataset.yml

# Validazione
toolkit validate --config datasets/pnrr-progetti/dataset.yml
```

### Join consigliati

| Da | A | Chiave | Domanda |
|---|---|---|---|
| `pnrr_progetti` | `pnrr_gare` | CUP | I progetti diventano gare? |
| `pnrr_progetti` | `pnrr_pagamenti` | CUP | Quanto è stato pagato? |
| `pnrr_indicatori_target` | `pnrr_progetti` | CUP | Quali indicatori monitora ogni progetto? |
| `pnrr_quadro_finanziario` | tutti | codice_univoco_submisura | Anagrafica misure/submisure |
| `pnrr_tag_clima_digitale` | `pnrr_progetti` | codice_univoco_submisura | Quanto è clima/digitale? |

### Fonte

**Italia Domani** — MEF / SoGeI
- Catalogo: https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data.html
- Licenza: dati pubblici (da verificare)

### Note

- Il server AEM/Akamai blocca `python-requests` ma accetta wget (gestito nei `preprocess.py`)
- Per CI serve `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` (guardrail di sicurezza)
- Importi in formato italiano (virgola decimale) → `clean.read.decimal: ","`
