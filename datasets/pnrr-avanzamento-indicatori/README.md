# PNRR Avanzamento Indicatori Comuni Europei

Avanzamento degli indicatori comuni europei per misura del PNRR: per ogni submisura e indicatore, il valore realizzato, se disponibile, e il semestre di riferimento.

**6.030 righe**, **47 indicatori**, **39% con valore**. ~2-3 MB.

## Dati

21 colonne:
- **Classificazione**: missione (7), componente, misura, submisura, CID
- **Amministrazione**: denominazione
- **Indicatore**: codice, descrizione, unità di misura
- **Periodo**: anno, semestre
- **Valori**: valore indicatore, valore stimato, valore non disponibile (flag)

## Fonte

**Italia Domani** — MEF / SoGeI
URL: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/OpenData_PNRR_avanzamento_indicatori_comuni.csv
Dimensione file: ~2-3 MB
Download: `preprocess.py` (wget + fallback urllib)

## Mart

| Tabella | Grano | Contenuto |
|---|---|---|
| `mart_per_missione` | missione | n indicatori, n con valore, n non disponibili, % realizzazione |
| `mart_per_submisura` | submisura | n indicatori, n con valore, % realizzazione per submisura |
