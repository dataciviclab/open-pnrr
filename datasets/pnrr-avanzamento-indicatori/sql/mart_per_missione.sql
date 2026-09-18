SELECT
    missione,
    descrizione_missione,
    COUNT(DISTINCT codice_indicatore) AS n_indicatori,
    COUNT(CASE WHEN valore_indicatore IS NOT NULL AND valore_indicatore > 0 THEN 1 END) AS n_con_valore,
    COUNT(CASE WHEN valore_non_disponibile = 'Sì' THEN 1 END) AS n_non_disponibile,
    ROUND(COUNT(CASE WHEN valore_indicatore IS NOT NULL AND valore_indicatore > 0 THEN 1 END) * 100.0 / COUNT(*), 2) AS pct_realizzazione
FROM clean_input
GROUP BY missione, descrizione_missione
