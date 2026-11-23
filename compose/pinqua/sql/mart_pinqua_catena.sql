-- mart_pinqua_catena: il funnel nazionale del PINQuA
-- finanziato (progetti) -> appaltato (gare) -> pagato (pagamenti).
--
-- ATTENZIONE alla semantica: `pnrr_gare` ha CIG duplicati (un contratto che copre
-- piu' CUP/interventi, 157 CIG con lo stesso importo) e righe senza CIG. Sommare le
-- righe gonfia il totale (2.524,9 mln = 99,4%). Qui:
--   - `aggiudicato_cig` = un importo per CIG distinto (5.851 CIG, 2.093,2 mln = 82,4%)
--   - `aggiudicato_senza_cig` = righe con CIG assente (141, 175,2 mln), tenute separate
--     perche' non riconciliabili con ANAC
WITH p AS (
    SELECT cup, codice_locale_progetto, fin_pnrr
    FROM read_parquet({support.progetti.clean})
    WHERE missione = 'M5' AND componente = 'M5C2' AND id_misura = 'M5C2I2.3'
),
g AS (
    SELECT cig, cup, codice_locale_progetto, importo_aggiudicazione
    FROM read_parquet({support.gare.clean})
    WHERE lower(descrizione_submisura) LIKE '%abitare%'
),
g_cig AS (
    -- un importo per CIG: max() protegge dai duplicati identici
    SELECT cig, MAX(importo_aggiudicazione) AS importo
    FROM g
    WHERE cig IS NOT NULL
    GROUP BY 1
),
g_senza AS (
    SELECT SUM(importo_aggiudicazione) AS importo, COUNT(*) AS righe
    FROM g
    WHERE cig IS NULL
),
pagato AS (
    SELECT COALESCE(SUM(pa.pagamento_pnrr), 0) AS pagato
    FROM read_parquet({support.pagamenti.clean}) pa
    JOIN p ON p.cup = pa.cup AND p.codice_locale_progetto = pa.codice_locale_progetto
)
SELECT
    COUNT(DISTINCT p.cup) AS cup,
    COUNT(*) AS interventi,
    ROUND(SUM(p.fin_pnrr)) AS finanziato_pnrr,
    (SELECT COUNT(*) FROM g_cig) AS n_cig,
    ROUND((SELECT SUM(importo) FROM g_cig)) AS aggiudicato_cig,
    ROUND(100.0 * (SELECT SUM(importo) FROM g_cig) / NULLIF(SUM(p.fin_pnrr), 0), 1) AS pct_aggiudicato_cig,
    (SELECT righe FROM g_senza) AS gare_senza_cig,
    ROUND((SELECT importo FROM g_senza)) AS aggiudicato_senza_cig,
    ROUND(100.0 * (SELECT importo FROM g_senza) / NULLIF(SUM(p.fin_pnrr), 0), 1) AS pct_senza_cig,
    ROUND((SELECT pagato FROM pagato)) AS pagato_pnrr,
    ROUND(100.0 * (SELECT pagato FROM pagato) / NULLIF(SUM(p.fin_pnrr), 0), 1) AS pct_pagato
FROM p
