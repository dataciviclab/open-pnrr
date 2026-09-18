# Note tecniche — pnrr-indicatori-target

## Fonte

**Italia Domani** (MEF / SoGeI), fonte dati ReGiS.
- Landing page: https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data/indicatori-target-dei-progetti-del-pnrr.html
- URL diretto CSV: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Indicatori_Target.csv
- Dimensione: ~77-84 MB (versioni v5-v7)
- Licenza: da verificare (dati pubblici)

## Download (AEM/Akamai)

Il server AEM/Akamai blocca python-requests ma **accetta wget** (pattern
verificato per pnrr-progetti/pnrr-gare/pnrr-pagamenti).
- `preprocess.py`: wget con User-Agent browser, fallback su urllib.
- Per CI: `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` (guardrail di sicurezza).

## Formato

- CSV delim `;`, encoding UTF-8
- Importi in formato italiano (virgola decimale) → `clean.read.decimal: ","`
- Date `DD/MM/YYYY` → `TRY_STRPTIME(..., '%d/%m/%Y')` in clean.sql
- Mese in italiano (es. "Dicembre") → lasciato come VARCHAR

## Contenuto

Per ogni CUP-CLP del PNRR, gli indicatori target associati:
- Codice indicatore (es. T0081, C7)
- Descrizione indicatore
- Unità di misura
- Tipo (Target / Base)
- Valore realizzato vs programmato
- Periodo (mese + anno)

## Deroga primary_key

Nessuna chiave naturale unica: un CUP può avere più righe (più indicatori,
più periodi). `not_null` su `cup` e `codice_indicatore`.

## Riferimenti

- Dataset complementari: `pnrr_progetti`, `pnrr_pagamenti`
- Aggiornamento: il file CSV viene aggiornato periodicamente da SoGeI
