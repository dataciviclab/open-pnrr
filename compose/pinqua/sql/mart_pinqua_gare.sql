-- mart_pinqua_gare: un contratto PINQuA per CIG, con l'aggiudicazione ANAC e i SAL
-- Grana: CIG (un contratto puo' coprire piu' interventi: `n_interventi` lo dice).
--
-- Due fonti sullo stesso CIG non coincidono e non vanno sommate:
--   - `importo_gara_pnrr` = importo dichiarato nel monitoraggio PNRR (quota finanziata)
--   - `importo_aggiudicazione_anac` = importo dell'aggiudicazione per ANAC (contratto)
-- La differenza e' strutturale, non un errore: vedi la nota in README.
--
-- Il SAL copre solo una parte dei CIG (chi comunica): `senza_sal` non significa lavori
-- fermi, significa nessun avanzamento tracciato in ANAC.
WITH g AS (
    SELECT
        cig,
        ANY_VALUE(cup) AS cup,
        COUNT(DISTINCT codice_locale_progetto) AS n_interventi,
        MAX(importo_aggiudicazione) AS importo_gara_pnrr,
        MAX(importo_complessivo_gara) AS importo_complessivo_gara,
        MIN(data_aggiudicazione_definitiva) AS data_aggiudicazione
    FROM read_parquet({support.gare.clean})
    WHERE lower(descrizione_submisura) LIKE '%abitare%'
      AND cig IS NOT NULL
    GROUP BY 1
),
a AS (
    SELECT
        cig,
        MAX(importo_aggiudicazione) AS importo_aggiudicazione_anac,
        MAX(ribasso_aggiudicazione) AS ribasso_pct,
        MAX(numero_offerte_ammesse) AS offerte_ammesse,
        MAX(numero_offerte_escluse) AS offerte_escluse,
        MAX(data_aggiudicazione_definitiva) AS data_aggiudicazione_anac
    FROM read_parquet({support.anac_aggiudicazioni.clean})
    WHERE cig IS NOT NULL
    GROUP BY 1
),
s AS (
    SELECT
        cig,
        COUNT(*) AS n_sal,
        SUM(importo_sal) AS importo_sal,
        COUNT(*) FILTER (WHERE flag_ritardo = 'IN RITARDO') AS sal_in_ritardo,
        MAX(data_emissione_sal) AS ultimo_sal
    FROM read_parquet({support.anac_sal.clean})
    WHERE cig IS NOT NULL
    GROUP BY 1
)
SELECT
    g.cig,
    g.cup,
    g.n_interventi,
    ROUND(g.importo_gara_pnrr) AS importo_gara_pnrr,
    ROUND(g.importo_complessivo_gara) AS importo_complessivo_gara,
    ROUND(a.importo_aggiudicazione_anac) AS importo_aggiudicazione_anac,
    a.ribasso_pct,
    a.offerte_ammesse,
    a.offerte_escluse,
    COALESCE(g.data_aggiudicazione, a.data_aggiudicazione_anac) AS data_aggiudicazione,
    CASE WHEN a.cig IS NULL THEN 'non in ANAC' ELSE 'in ANAC' END AS copertura_anac,
    COALESCE(s.n_sal, 0) AS n_sal,
    ROUND(s.importo_sal) AS importo_sal,
    COALESCE(s.sal_in_ritardo, 0) AS sal_in_ritardo,
    s.ultimo_sal,
    CASE
        WHEN s.cig IS NULL THEN 'senza SAL'
        WHEN s.sal_in_ritardo > 0 THEN 'con SAL in ritardo'
        ELSE 'con SAL in linea'
    END AS stato_sal
FROM g
LEFT JOIN a USING (cig)
LEFT JOIN s USING (cig)
ORDER BY g.importo_gara_pnrr DESC
