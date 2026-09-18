SELECT
    COUNT(*) AS n_submisure,
    ROUND(SUM(importo_totale)) AS importo_totale,
    ROUND(SUM(importo_progetti_in_essere)) AS importo_progetti_in_essere,
    ROUND(SUM(importo_progetti_nuovi)) AS importo_progetti_nuovi,
    ROUND(SUM(importo_progetti_in_essere) / NULLIF(SUM(importo_totale), 0) * 100, 2) AS pct_in_essere
FROM clean_input
