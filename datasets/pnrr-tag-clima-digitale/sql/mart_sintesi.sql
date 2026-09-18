SELECT
    COUNT(*) AS n_submisure,
    ROUND(SUM(importo_campo_intervento)) AS tot_importo,
    ROUND(SUM(importo_clima)) AS tot_clima,
    ROUND(SUM(importo_digitale)) AS tot_digitale,
    ROUND(SUM(importo_clima) / NULLIF(SUM(importo_campo_intervento), 0) * 100, 2) AS pct_clima,
    ROUND(SUM(importo_digitale) / NULLIF(SUM(importo_campo_intervento), 0) * 100, 2) AS pct_digitale
FROM clean_input
