-- mart_pinqua_interventi: un intervento PINQuA per riga (CUP × codice locale progetto)
-- Catena per intervento: finanziato (progetti) -> appaltato (gare) -> pagato (pagamenti).
--
-- Deduplica dei CIG: `pnrr_gare` puo' ripetere lo stesso CIG su piu' interventi (un
-- contratto che copre piu' CUP/CLP) con lo stesso importo. Qui il CIG viene tenuto una
-- volta e il suo importo ripartito in parti uguali tra gli interventi che copre;
-- `n_cig` conta i contratti distinti, `aggiudicato` non gonfia.
-- Le gare senza CIG non sono attribuibili a un intervento: restano fuori da questo mart
-- e sono contate in `mart_pinqua_catena` (`aggiudicato_senza_cig`).
WITH p AS (
    SELECT
        cup,
        codice_locale_progetto AS id_intervento,
        titolo_progetto AS titolo,
        soggetto_attuatore,
        amministrazione_titolare,
        fin_pnrr,
        fin_totale,
        stato_avanzamento,
        descrizione_fase_iter AS fase_iter,
        data_inizio_prevista,
        data_fine_prevista,
        data_fine_effettiva
    FROM read_parquet({support.progetti.clean})
    WHERE missione = 'M5'
      AND componente = 'M5C2'
      AND id_misura = 'M5C2I2.3'
),
g0 AS (
    SELECT DISTINCT cig, cup, codice_locale_progetto, importo_aggiudicazione
    FROM read_parquet({support.gare.clean})
    WHERE cig IS NOT NULL
      AND lower(descrizione_submisura) LIKE '%abitare%'
),
g_n AS (
    SELECT cig, COUNT(*) AS n_interventi FROM g0 GROUP BY 1
),
g AS (
    SELECT
        g0.cup,
        g0.codice_locale_progetto,
        COUNT(DISTINCT g0.cig) AS n_cig,
        SUM(g0.importo_aggiudicazione / g_n.n_interventi) AS aggiudicato
    FROM g0
    JOIN g_n USING (cig)
    GROUP BY 1, 2
),
pg AS (
    SELECT
        cup,
        codice_locale_progetto,
        SUM(pagamento_pnrr) AS pagato_pnrr,
        SUM(pagamento_totale) AS pagato_totale
    FROM read_parquet({support.pagamenti.clean})
    GROUP BY 1, 2
)
SELECT
    p.cup,
    p.id_intervento,
    p.titolo,
    p.soggetto_attuatore,
    p.amministrazione_titolare,
    ROUND(p.fin_pnrr) AS fin_pnrr,
    ROUND(p.fin_totale) AS fin_totale,
    COALESCE(g.n_cig, 0) AS n_cig,
    ROUND(COALESCE(g.aggiudicato, 0)) AS aggiudicato,
    ROUND(COALESCE(pg.pagato_pnrr, 0)) AS pagato_pnrr,
    ROUND(COALESCE(pg.pagato_totale, 0)) AS pagato_totale,
    ROUND(100.0 * COALESCE(pg.pagato_pnrr, 0) / NULLIF(p.fin_pnrr, 0), 1) AS pct_pagato_pnrr,
    p.stato_avanzamento,
    p.fase_iter,
    p.data_inizio_prevista,
    p.data_fine_prevista,
    p.data_fine_effettiva
FROM p
LEFT JOIN g ON g.cup = p.cup AND g.codice_locale_progetto = p.id_intervento
LEFT JOIN pg ON pg.cup = p.cup AND pg.codice_locale_progetto = p.id_intervento
ORDER BY p.fin_pnrr DESC
