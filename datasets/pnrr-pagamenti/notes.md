# Note tecniche — pnrr-pagamenti

## Fonte

**Italia Domani** (MEF / SoGeI), fonte dati ReGiS.
- Landing page: https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data/pagamenti-dei-progetti-del-pnrr.html
- URL diretto CSV: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Pagamenti_di_Progetto.csv
- Licenza: da verificare (dati pubblici — stessa fonte di pnrr-progetti/pnrr-gare)

## Download (AEM/Akamai)

Il server AEM/Akamai richiede UA browser e, in CI, il fallback proxy.
- `dataset.yml` con `type: http_file` + `client.user_agent` browser.
- In CI: `BLOCKED_SOURCE_PROXY` per il fallback proxy.
- **HEAD risponde 404** su questo endpoint: il preflight usa il Range GET.
- `clean.read.decimal: ","` — gli importi sono in formato italiano.

## Formato

- CSV delim `;`, encoding UTF-8 con BOM (`utf-8-sig`)
- Importi sia interi sia con virgola decimale (es. `13950000000` e `2738869489,5`)
  → `clean.read.decimal: ","` gestisce entrambi
- Date `DD/MM/YYYY` → `TRY_STRPTIME(..., '%d/%m/%Y')` in clean.sql
- 2 CUP anomali con valore "N/A" → normalizzati a NULL in clean

## Deroga primary_key (clean)

Nessuna chiave naturale unica: un CUP può avere più righe (più submisure o
estrazioni per lo stesso progetto). `not_null` solo su `cup`.

## Volumi (dati estratti 2026-08-05)

| Metrica | Valore |
|---|---|
| Righe | 211.901 |
| Pagamenti PNRR totali | €101,9 mld |
| Data estrazione | 13/06/2026 |

## Relazioni con il filone PNRR

Chiude il cerchio finanziario PNRR: `pnrr_progetti` (stanziamento) +
`pnrr_gare` (contrattualizzazione) + `pnrr_pagamenti` (erogazione effettiva).
Join via CUP/CLP con `pnrr_progetti`.

## Riferimenti

- Issue intake: nessuna (da aprire, filone PNRR avviato con #517/#518)
- Dataset complementari: `pnrr_progetti` (candidate), `pnrr_gare` (candidate)
