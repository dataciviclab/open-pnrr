SELECT
    CAST("Descrizione Misura" AS VARCHAR) AS descrizione_misura,
    CAST("ID Submisura" AS VARCHAR) AS id_submisura,
    CAST("Codice CID" AS VARCHAR) AS codice_cid,
    CAST("Codice Univoco Submisura" AS VARCHAR) AS codice_univoco_submisura,
    CAST("Descrizione Submisura" AS VARCHAR) AS descrizione_submisura,
    CAST("Tipo Intervento" AS VARCHAR) AS tipo_intervento,
    CAST("Investimento/ Riforma" AS VARCHAR) AS investimento_riforma,
    CAST("Sovvenzione/Prestito" AS VARCHAR) AS sovvenzione_prestito,
    CAST("Amministrazione Titolare" AS VARCHAR) AS amministrazione_titolare,
    CAST("Importo Campo di intervento relativo alla submisura" AS DOUBLE) AS importo_campo_intervento,
    CAST("Campo di intervento Clima" AS VARCHAR) AS campo_intervento_clima,
    CAST("Coefficiente TAG Clima" AS VARCHAR) AS coeff_clima,
    CAST("Campo di intervento Digital" AS VARCHAR) AS campo_intervento_digitale,
    CAST("Coefficiente TAG Digitale" AS VARCHAR) AS coeff_digitale,
    CAST("Importo Contribuzione al Clima" AS DOUBLE) AS importo_clima,
    CAST("Importo Contribuzione al Digitale" AS DOUBLE) AS importo_digitale
FROM raw_input
