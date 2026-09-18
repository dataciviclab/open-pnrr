# Note tecniche — pnrr-quadro-finanziario

## Fonte

**Italia Domani** (MEF / SoGeI)
- Landing page: https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data/quadro-finanziario-pnrr.html
- URL diretto CSV: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/OpenData_PNRR_QuadroFinProgrammazione.csv
- Dimensione: ~114 KB (aggiornato con nuove versioni v08-v12)
- Licenza: da verificare (dati pubblici)

## Download (AEM/Akamai)

Pattern identico ai dataset pnrr_* esistenti.

## Formato

- CSV delim `;`, encoding UTF-8
- Importi in formato italiano (virgola decimale) → `clean.read.decimal: ","`

## Contenuto

Anagrafica delle misure/submisure del PNRR:
- Codici identificativi (missione, componente, misura, submisura, CID)
- Classificazione (intervento/riforma, prestito/sovvenzione)
- Amministrazione titolare
- Importi: totale, progetti in essere, progetti nuovi

## Come support dataset

Questo dataset può essere usato come **support** dagli altri dataset PNRR:
- `pnrr_progetti`: join via `codice_univoco_submisura` per arricchire con anagrafica misure
- `pnrr_indicatori_target`: join per ottenere descrizioni misure/submisure

## Riferimenti

- Dataset complementari: `pnrr_progetti`, `pnrr_pagamenti`, `pnrr_gare`
