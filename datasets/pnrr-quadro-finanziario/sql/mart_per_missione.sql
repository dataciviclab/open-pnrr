SELECT
    missione,
    descrizione_missione,
    COUNT(*) AS n_submisure,
    ROUND(SUM(importo_totale)) AS importo_totale,
    ROUND(SUM(importo_progetti_in_essere)) AS importo_progetti_in_essere,
    ROUND(SUM(importo_progetti_nuovi)) AS importo_progetti_nuovi
FROM clean_input
GROUP BY missione, descrizione_missione
