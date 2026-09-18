# PNRR TAG Sostegno Clima/Digitale

TAG per il sostegno climatico e digitale per misura del PNRR: per ogni submisura i campi di intervento UE (Annex VI/VII), i coefficienti e gli importi associati a clima e digitale.

**375 righe**, **€194,4 mld totali**, **37% clima (€72,0 mld)**, **26% digitale (€49,9 mld)**. ~140 KB.

## Dati

16 colonne:
- **Classificazione**: descrizione misura, submisura, CID
- **Tipo**: intervento, investimento/riforma, sovvenzione/prestito
- **Amministrazione**: titolare
- **Importi**: campo intervento submisura (€)
- **TAG Clima**: campo intervento, coefficiente, importo contribuzione
- **TAG Digitale**: campo intervento, coefficiente, importo contribuzione

## Fonte

**Italia Domani** — MEF / SoGeI
URL: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/TAG_sostegno_clima_digitale.csv
Dimensione file: ~140 KB
Download: `preprocess.py` (wget + fallback urllib)

## Mart

| Tabella | Grano | Contenuto |
|---|---|---|
| `mart_sintesi` | globale | n submisure, importi totali clima/digitale, % sul totale |
