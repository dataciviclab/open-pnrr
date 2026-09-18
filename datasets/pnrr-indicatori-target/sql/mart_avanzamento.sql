SELECT
    codice_indicatore,
    descrizione_indicatore,
    COUNT(DISTINCT cup) AS n_cup,
    COUNT(CASE WHEN valore_realizzato IS NOT NULL THEN 1 END) AS n_valori_realizzati,
    ROUND(SUM(valore_realizzato)) AS valore_realizzato_totale,
    ROUND(SUM(valore_programmato)) AS valore_programmato_totale,
    ROUND(SUM(valore_realizzato) / NULLIF(SUM(valore_programmato), 0) * 100, 2) AS pct_realizzazione
FROM clean_input
GROUP BY codice_indicatore, descrizione_indicatore
