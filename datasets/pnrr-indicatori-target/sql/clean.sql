SELECT
    CAST("Codice Univoco Submisura" AS VARCHAR) AS codice_univoco_submisura,
    CAST("Descrizione Submisura" AS VARCHAR) AS descrizione_submisura,
    TRIM(CAST("CUP" AS VARCHAR)) AS cup,
    CAST("Codice Locale Progetto" AS VARCHAR) AS codice_locale_progetto,
    CAST("Codice Indicatore" AS VARCHAR) AS codice_indicatore,
    CAST("Descrizione Indicatore" AS VARCHAR) AS descrizione_indicatore,
    CAST("Unità di Misura" AS VARCHAR) AS unita_misura,
    CAST("Descrizione Unità di Misura" AS VARCHAR) AS descrizione_unita_misura,
    CAST("Descrizione Tipo indicatore" AS VARCHAR) AS descrizione_tipo_indicatore,
    CAST("Valore Realizzato" AS DOUBLE) AS valore_realizzato,
    CAST("Valore Programmato" AS DOUBLE) AS valore_programmato,
    CAST("Mese" AS VARCHAR) AS mese,
    CAST("Anno" AS INTEGER) AS anno,
    TRY_STRPTIME(CAST("Data di Estrazione" AS VARCHAR), '%d/%m/%Y') AS data_estrazione,
    CAST({year} AS INTEGER) AS anno_estrazione
FROM raw_input
