-- mart_pinqua_regioni: il PINQuA per regione
-- Stessa ripartizione del mart comunale (CUP multi-comune divisi in parti uguali tra
-- i comuni, poi riaggregati), cosi' il totale regionale chiude sul totale progetti.
WITH p AS (
    SELECT cup, codice_locale_progetto, fin_pnrr, fin_totale
    FROM read_parquet({support.progetti.clean})
    WHERE missione = 'M5' AND componente = 'M5C2' AND id_misura = 'M5C2I2.3'
),
loc AS (
    SELECT DISTINCT cup, codice_comune, regione
    FROM read_parquet({support.localizzazione.clean})
    WHERE codice_comune IS NOT NULL
),
n AS (
    SELECT cup, COUNT(*) AS n_comuni FROM loc GROUP BY 1
)
SELECT
    COALESCE(l.regione, 'non localizzato') AS regione,
    COUNT(DISTINCT p.cup) AS cup,
    COUNT(DISTINCT l.codice_comune) AS comuni,
    COUNT(DISTINCT p.codice_locale_progetto) AS interventi,
    ROUND(SUM(p.fin_pnrr / n.n_comuni)) AS fin_pnrr_quota,
    ROUND(SUM(p.fin_totale / n.n_comuni)) AS fin_totale_quota
FROM p
LEFT JOIN loc l USING (cup)
LEFT JOIN n USING (cup)
GROUP BY 1
ORDER BY fin_pnrr_quota DESC
