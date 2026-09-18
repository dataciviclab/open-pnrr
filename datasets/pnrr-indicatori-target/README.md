# PNRR Indicatori Target

Indicatori target dei progetti del PNRR: per ogni CUP-CLP, l'indicatore monitorato, il valore realizzato, il valore programmato, il periodo (mese/anno) e la data di estrazione.

**357.183 righe**, **240.558 CUP**, **322 indicatori**, **74% con valore realizzato**. ~77 MB raw.

## Dati

14 colonne:
- **Classificazione**: codice univoco submisura, descrizione submisura
- **Progetto**: CUP, codice locale progetto
- **Indicatore**: codice, descrizione, unità di misura, tipo (Target/Base)
- **Valori**: valore realizzato, valore programmato
- **Periodo**: mese, anno
- **Metadati**: data estrazione

## Fonte

**Italia Domani** — MEF / SoGeI
URL: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Indicatori_Target.csv
Dimensione file: ~77-84 MB (aggiornato periodicamente)
Download: `preprocess.py` (wget + fallback urllib)

## Mart

| Tabella | Grano | Contenuto |
|---|---|---|
| `mart_avanzamento` | indicatore | n CUP, valori realizzati/sommatorie, % realizzazione per indicatore |
| `mart_per_submisura` | submisura | n indicatori, n CUP, % realizzazione medio per submisura |
