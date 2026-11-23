-- mart_pinqua_fisico: l'avanzamento FISICO per CUP (alloggi e metri quadri)
-- Fonte: pnrr_indicatori_target, che espone valore_programmato e valore_realizzato
-- per CUP. Quattro indicatori della misura M5C2I2.3:
--   alloggi ERP, alloggi ERS, posti per studentati, mq di spazi pubblici.
--
-- I valori sono un'istantanea per CUP (una riga per indicatore): non sono una serie
-- storica, quindi si sommano tra CUP ma non nel tempo.
--
-- ATTENZIONE agli spazi pubblici: la somma dei programmati per CUP e' ~8,1 mln di mq,
-- dieci volte il target di programma (800.000 mq). Il target e' un pavimento, non la
-- somma dei progetti: non confrontare i due numeri senza questa nota.
WITH i AS (
    SELECT
        cup,
        MAX(CASE WHEN descrizione_indicatore ILIKE '%UNITÀ ABITATIVE ERP%' THEN valore_programmato END) AS erp_prog,
        MAX(CASE WHEN descrizione_indicatore ILIKE '%UNITÀ ABITATIVE ERP%' THEN valore_realizzato END) AS erp_real,
        MAX(CASE WHEN descrizione_indicatore ILIKE '%UNITÀ ABITATIVE ERS%' THEN valore_programmato END) AS ers_prog,
        MAX(CASE WHEN descrizione_indicatore ILIKE '%UNITÀ ABITATIVE ERS%' THEN valore_realizzato END) AS ers_real,
        MAX(CASE WHEN descrizione_indicatore ILIKE '%STUDENTATI%' THEN valore_programmato END) AS studentati_prog,
        MAX(CASE WHEN descrizione_indicatore ILIKE '%STUDENTATI%' THEN valore_realizzato END) AS studentati_real,
        MAX(CASE WHEN descrizione_indicatore ILIKE '%SPAZI PUBBLICI%' THEN valore_programmato END) AS mq_prog,
        MAX(CASE WHEN descrizione_indicatore ILIKE '%SPAZI PUBBLICI%' THEN valore_realizzato END) AS mq_real,
        MAX(data_estrazione) AS data_estrazione
    FROM read_parquet({support.indicatori.clean})
    WHERE lower(descrizione_submisura) LIKE '%abitare%'
    GROUP BY 1
)
SELECT
    cup,
    ROUND(COALESCE(erp_prog, 0)) AS alloggi_erp_programmati,
    ROUND(COALESCE(erp_real, 0)) AS alloggi_erp_realizzati,
    ROUND(100.0 * COALESCE(erp_real, 0) / NULLIF(erp_prog, 0), 1) AS pct_erp,
    ROUND(COALESCE(ers_prog, 0)) AS alloggi_ers_programmati,
    ROUND(COALESCE(ers_real, 0)) AS alloggi_ers_realizzati,
    ROUND(COALESCE(studentati_prog, 0)) AS posti_studentati_programmati,
    ROUND(COALESCE(studentati_real, 0)) AS posti_studentati_realizzati,
    ROUND(COALESCE(mq_prog, 0)) AS mq_spazi_programmati,
    ROUND(COALESCE(mq_real, 0)) AS mq_spazi_realizzati,
    ROUND(100.0 * COALESCE(mq_real, 0) / NULLIF(mq_prog, 0), 1) AS pct_mq,
    -- "fermo" = ha un target di alloggi e non ha consegnato nulla
    (COALESCE(erp_prog, 0) + COALESCE(ers_prog, 0) > 0
        AND COALESCE(erp_real, 0) + COALESCE(ers_real, 0) = 0) AS alloggi_a_zero,
    data_estrazione
FROM i
ORDER BY alloggi_erp_programmati DESC
