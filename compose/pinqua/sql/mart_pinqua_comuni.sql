-- mart_pinqua_comuni: il PINQuA per comune
-- La geografia non e' nei dataset PNRR: arriva da opencup_localizzazione (stesso CUP).
-- 899 CUP su 909 insistono su un solo comune; i 10 multi-comune (fino a 29) sono
-- ripartiti in parti uguali, altrimenti la somma gonfia (3,69 vs 3,25 mld).
-- "interventi" conta i codice_locale_progetto che toccano il comune: per i CUP
-- multi-comune lo stesso intervento compare in piu' comuni.
WITH p AS (
    SELECT cup, codice_locale_progetto, fin_pnrr, fin_totale
    FROM read_parquet({support.progetti.clean})
    WHERE missione = 'M5' AND componente = 'M5C2' AND id_misura = 'M5C2I2.3'
),
loc AS (
    SELECT DISTINCT cup, codice_comune, comune, provincia, regione
    FROM read_parquet({support.localizzazione.clean})
    WHERE codice_comune IS NOT NULL
),
n AS (
    SELECT cup, COUNT(*) AS n_comuni FROM loc GROUP BY 1
)
SELECT
    l.codice_comune,
    ANY_VALUE(l.comune) AS comune,
    ANY_VALUE(l.provincia) AS provincia,
    ANY_VALUE(l.regione) AS regione,
    COUNT(DISTINCT p.cup) AS cup,
    COUNT(DISTINCT p.codice_locale_progetto) AS interventi,
    ROUND(SUM(p.fin_pnrr / n.n_comuni)) AS fin_pnrr_quota,
    ROUND(SUM(p.fin_totale / n.n_comuni)) AS fin_totale_quota,
    MAX(n.n_comuni) AS comuni_del_cup_max
FROM p
JOIN loc l USING (cup)
JOIN n USING (cup)
GROUP BY 1
ORDER BY fin_pnrr_quota DESC
