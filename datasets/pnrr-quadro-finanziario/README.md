# PNRR Quadro Finanziario

Anagrafica delle misure e submisure del PNRR con importi di programmazione: finanziamento totale, progetti in essere e progetti nuovi per ogni unità di riferimento.

**304 righe**, **€194,4 mld totali**, **€47,5 mld in essere**, **€146,9 mld nuovi**. ~114 KB.

## Dati

19 colonne:
- **Programma**: PNRR
- **Classificazione**: missione (7), componente, misura, submisura, CID
- **Tipo**: livello (Intervento), investimento/riforma, prestito/sovvenzione
- **Amministrazione**: titolare
- **Importi**: totale, progetti in essere, progetti nuovi (€)

## Fonte

**Italia Domani** — MEF / SoGeI
URL: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/OpenData_PNRR_QuadroFinProgrammazione.csv
Dimensione file: ~114 KB
Download: `preprocess.py` (wget + fallback urllib)

## Mart

| Tabella | Grano | Contenuto |
|---|---|---|
| `mart_per_missione` | missione | n submisure, importi totale/in-essere/nuovi per missione |
| `mart_sintesi` | globale | sintesi finanziaria complessiva del PNRR |
