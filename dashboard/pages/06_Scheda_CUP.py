"""Scheda CUP — Lookup singolo progetto PNRR."""

import streamlit as st
from sources import query_progetti, query_gare, query_pagamenti, fmt_eur, fmt_num

st.title("🔍 Scheda CUP")

# ── Ricerca ──────────────────────────────────────────────────────
cup_input = st.text_input("Inserisci CUP", placeholder="es. B83C22000160006")
search = st.button("Cerca")

if search and cup_input:
    cup = cup_input.strip()

    # ── Anagrafe progetto ────────────────────────────────────────
    progetto = query_progetti(f"SELECT * FROM clean_input WHERE cup = '{cup.replace(chr(39), chr(39)*2)}' LIMIT 1")

    if progetto.empty:
        st.warning(f"Nessun progetto trovato per CUP: {cup}")
    else:
        p = progetto.iloc[0]

        st.subheader(f"`{p['cup']}`")
        st.caption(str(p.get("titolo_progetto", "N/A")))

        # ── Info generali ────────────────────────────────────────
        st.markdown("**Informazioni progetto**")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Missione", str(p.get("missione", "N/A")))
        c2.metric("Stato", str(p.get("stato_avanzamento", "N/A")))
        c3.metric("Fin. PNRR", fmt_eur(p.get("fin_pnrr", 0)))
        c4.metric("Fin. Totale", fmt_eur(p.get("fin_totale", 0)))

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Soggetto", str(p.get("soggetto_attuatore", "N/A"))[:40])
        c2.metric("Amministrazione", str(p.get("amministrazione_titolare", "N/A"))[:40])
        c3.metric("Inizio previsto", str(p.get("data_inizio_prevista", "N/A")))
        c4.metric("Fine prevista", str(p.get("data_fine_prevista", "N/A")))

        if p.get("data_fine_effettiva"):
            st.info(f"Progetto concluso il {p['data_fine_effettiva']}")

        st.divider()

        # ── Descrizione ──────────────────────────────────────────
        with st.expander("Descrizione progetto"):
            st.write(p.get("sintesi_progetto", "Nessuna descrizione disponibile."))

        # ── Finanziamento ────────────────────────────────────────
        st.markdown("**Finanziamento**")
        fin_cols = st.columns(4)
        fin_cols[0].metric("PNRR", fmt_eur(p.get("fin_pnrr", 0)))
        fin_cols[1].metric("Totale", fmt_eur(p.get("fin_totale", 0)))
        fin_cols[2].metric("Stato", fmt_eur(p.get("fin_stato", 0)))
        fin_cols[3].metric("UE", fmt_eur(p.get("fin_ue", 0)))

        st.divider()

        # ── Gare associate ───────────────────────────────────────
        st.markdown("**Gare associate**")
        gare = query_gare(f"""
            SELECT cig, oggetto_principale_contratto,
                   descrizione_procedura_aggiudicazione,
                   ROUND(importo_complessivo_gara) AS imp_gara,
                   ROUND(importo_aggiudicazione) AS imp_agg,
                   data_pubblicazione_cig, data_aggiudicazione_definitiva
            FROM clean_input WHERE cup = '{cup.replace(chr(39), chr(39)*2)}'
            ORDER BY data_pubblicazione_cig DESC
        """)

        if gare.empty:
            st.info("Nessuna gara associata.")
        else:
            k1, k2, k3 = st.columns(3)
            k1.metric("Gare", fmt_num(len(gare)))
            k2.metric("Importo gare", fmt_eur(gare["imp_gara"].sum()))
            k3.metric("Importo aggiudicato", fmt_eur(gare["imp_agg"].sum()))

            st.dataframe(
                gare.rename(columns={
                    "cig": "CIG", "oggetto_principale_contratto": "Oggetto",
                    "descrizione_procedura_aggiudicazione": "Procedura",
                    "imp_gara": "Imp. Gara", "imp_agg": "Imp. Agg.",
                    "data_pubblicazione_cig": "Pubblicazione",
                    "data_aggiudicazione_definitiva": "Aggiudicazione",
                }),
                width="stretch",
                hide_index=True,
            )

        st.divider()

        # ── Pagamenti ────────────────────────────────────────────
        st.markdown("**Pagamenti**")
        pag = query_pagamenti(f"""
            SELECT ROUND(SUM(finanziamento_pnrr)) AS fin_pnrr,
                   ROUND(SUM(pagamento_pnrr)) AS pag_pnrr,
                   ROUND(SUM(pagamento_totale)) AS pag_totale
            FROM clean_input WHERE cup = '{cup.replace(chr(39), chr(39)*2)}'
        """)

        if pag.empty or pag.iloc[0]["fin_pnrr"] is None:
            st.info("Nessun dato pagamento disponibile.")
        else:
            pgl = pag.iloc[0]
            k1, k2, k3 = st.columns(3)
            k1.metric("Finanziamento PNRR", fmt_eur(pgl["fin_pnrr"]))
            k2.metric("Pagato PNRR", fmt_eur(pgl["pag_pnrr"]))
            tasso = (pgl["pag_pnrr"] / pgl["fin_pnrr"] * 100) if pgl["fin_pnrr"] else 0
            k3.metric("Tasso assorbimento", f"{tasso:.1f}%")

st.caption("Dati: Italia Domani (MEF/SoGeI) · Fonte: open-pnrr")
