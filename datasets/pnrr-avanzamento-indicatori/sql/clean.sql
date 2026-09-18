SELECT
    CAST("Missione" AS VARCHAR) AS missione,
    CAST("Descrizione Missione" AS VARCHAR) AS descrizione_missione,
    CAST("Componente" AS VARCHAR) AS componente,
    CAST("Descrizione Componente" AS VARCHAR) AS descrizione_componente,
    CAST("ID Misura" AS VARCHAR) AS id_misura,
    CAST("Codice Univoco Misura" AS VARCHAR) AS codice_univoco_misura,
    CAST("Descrizione Misura" AS VARCHAR) AS descrizione_misura,
    CAST("Codice Univoco Submisura" AS VARCHAR) AS codice_univoco_submisura,
    CAST("ID Submisura" AS VARCHAR) AS id_submisura,
    CAST("Codice CID" AS VARCHAR) AS codice_cid,
    CAST("Descrizione submisura" AS VARCHAR) AS descrizione_submisura,
    CAST("Amministr." AS VARCHAR) AS amministrazione,
    CAST("Codice Indicatore" AS VARCHAR) AS codice_indicatore,
    CAST("Descrizione Indicatore" AS VARCHAR) AS descrizione_indicatore,
    CAST("Unità di misura" AS VARCHAR) AS unita_misura,
    CAST("Anno" AS INTEGER) AS anno,
    CAST("Semestre" AS VARCHAR) AS semestre,
    CAST("Valore indicatore" AS DOUBLE) AS valore_indicatore,
    CAST("Valore stimato" AS VARCHAR) AS valore_stimato,
    CAST("Valore non disponibile" AS VARCHAR) AS valore_non_disponibile,
    TRY_STRPTIME(CAST("Data di estrazione" AS VARCHAR), '%d/%m/%Y') AS data_estrazione,
    CAST({year} AS INTEGER) AS anno_estrazione
FROM raw_input
WHERE TRIM("Codice Indicatore") != ''
  AND TRIM("Missione") != ''
