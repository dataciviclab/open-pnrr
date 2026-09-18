# Note tecniche — pnrr-tag-clima-digitale

## Fonte

**Italia Domani** (MEF / SoGeI)
- Landing page: https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data/tag-per-il-sostegno-climatico-e-digitale-per-misura-del-pnrr.html
- URL diretto CSV: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/TAG_sostegno_clima_digitale.csv
- Dimensione: ~140 KB (versioni v05-v08)
- Licenza: da verificare (dati pubblici)

## Download (AEM/Akamai)

Pattern identico ai dataset pnrr_* esistenti.

## Formato

- CSV delim `;`, encoding UTF-8
- Importi in formato italiano (virgola decimale) → `clean.read.decimal: ","`
- Coefficienti TAG in formato percentuale (es. "100%", "0%") → lasciati come VARCHAR

## Contenuto

Per ogni submisura del PNRR:
- Campo di intervento UE (Annex VI: Clima, Annex VII: Digital)
- Coefficiente TAG Clima / Digitale (0-100%)
- Importo contribuzione al Clima / Digitale (€)

## Uso

Questo dataset è utile per:
- Analizzare la distribuzione delle risorse PNRR tra clima e digitale
- Calcolare l'impatto "green" e "digital" del Piano
- Support dataset per `pnrr_progetti` (join via codice_univoco_submisura)

## Riferimenti

- Dataset complementari: `pnrr_progetti`, `pnrr_quadro_finanziario`
