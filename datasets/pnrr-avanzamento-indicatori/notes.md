# Note tecniche — pnrr-avanzamento-indicatori

## Fonte

**Italia Domani** (MEF / SoGeI)
- Landing page: https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data/avanzamento-degli-indicatori-comuni-europei-per-misura-del-pnrr.html
- URL diretto CSV: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/OpenData_PNRR_avanzamento_indicatori_comuni.csv
- Dimensione: ~2-3 MB
- Licenza: da verificare (dati pubblici)

## Download (AEM/Akamai)

Pattern identico ai dataset pnrr_* esistenti.

## Formato

- CSV delim `;`, encoding UTF-8
- Date `DD/MM/YYYY` → `TRY_STRPTIME(..., '%d/%m/%Y')` in clean.sql
- Campi con spazi iniziali (es. " Valore indicatore ") → trim in clean.sql

## Contenuto

Monitora gli indicatori comuni europei del PNRR:
- Per ogni submisura/misura: l'indicatore europeo associato
- Valore realizzato vs stimato per semestre
- Flag "valore non disponibile" (Sì/No)
- Aggiornamento periodico

## Differenze con pnrr-indicatori-target

- **pnrr-indicatori-target**: granularità per CUP-CLP (progetto singolo), indicatori target
- **pnrr-avanzamento-indicatori**: granularità per submisura/misura, indicatori comuni europei (aggregati)

## Riferimenti

- Dataset complementari: `pnrr_indicatori_target`, `pnrr_progetti`
