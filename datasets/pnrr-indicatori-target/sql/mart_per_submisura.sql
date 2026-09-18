SELECT
    codice_univoco_submisura,
    descrizione_submisura,
    COUNT(DISTINCT codice_indicatore) AS n_indicatori,
    COUNT(DISTINCT cup) AS n_cup,
    ROUND(AVG(CASE WHEN valore_programmato > 0 THEN valore_realizzato / valore_programmato * 100 END), 2) AS pct_realizzazione_medio
FROM clean_input
GROUP BY codice_univoco_submisura, descrizione_submisura
