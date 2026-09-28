"""Panoramica — Visione d'insieme del PNRR italiano."""

import streamlit as st
import plotly.express as px
from sources import query_progetti, query_pagamenti, query_gare, fmt_eur, fmt_num

st.title("📊 Panoramica PNRR")

# ── KPI principali ────────────────────────────────────────────────
kpi = query_progetti("""
    SELECT
        COUNT(DISTINCT cup) AS n_progetti,
        ROUND(SUM(fin_pnrr)) AS fin_pnrr,
        ROUND(SUM(fin_totale)) AS fin_totale,
        SUM(CASE WHEN stato_avanzamento = 'Concluso' THEN 1 ELSE 0 END) AS conclusi,
        SUM(CASE WHEN stato_avanzamento = 'In Corso' THEN 1 ELSE 0 END) AS in_corso,
        SUM(CASE WHEN data_fine_prevista IS NOT NULL THEN 1 ELSE 0 END) AS con_scadenza
    FROM clean_input
""").iloc[0]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Progetti totali", fmt_num(int(kpi["n_progetti"])))
k2.metric("Fin. PNRR", fmt_eur(kpi["fin_pnrr"]))
k3.metric("In corso", fmt_num(int(kpi["in_corso"])))
k4.metric("Conclusi", fmt_num(int(kpi["conclusi"])))

st.divider()

# ── Pagamenti ─────────────────────────────────────────────────────
st.subheader("Assorbimento fondi")
pag = query_pagamenti("""
    SELECT
        ROUND(SUM(finanziamento_pnrr)) AS fin_pnrr,
        ROUND(SUM(pagamento_pnrr)) AS pag_pnrr,
        ROUND(SUM(pagamento_pnrr) / NULLIF(SUM(finanziamento_pnrr), 0) * 100, 1) AS tasso_pct
    FROM clean_input
""").iloc[0]

k1, k2, k3 = st.columns(3)
k1.metric("Finanziato PNRR", fmt_eur(pag["fin_pnrr"]))
k2.metric("Pagato PNRR", fmt_eur(pag["pag_pnrr"]))
k3.metric("Tasso assorbimento", f"{pag['tasso_pct']}%",
          delta="target 67%" if pag["tasso_pct"] < 67 else "target raggiunto",
          delta_color="inverse" if pag["tasso_pct"] < 67 else "normal")

st.divider()

# ── Gare ──────────────────────────────────────────────────────────
st.subheader("Gare PNRR")
gare = query_gare("""
    SELECT
        COUNT(*) AS n_gare,
        SUM(CASE WHEN importo_aggiudicazione IS NOT NULL THEN 1 ELSE 0 END) AS aggiudicate,
        ROUND(SUM(COALESCE(importo_aggiudicazione, 0))) AS tot_agg,
        ROUND(SUM(COALESCE(importo_complessivo_gara, 0))) AS tot_gara
    FROM clean_input
""").iloc[0]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Gare pubblicate", fmt_num(int(gare["n_gare"])))
k2.metric("Aggiudicate", fmt_num(int(gare["aggiudicate"])))
k3.metric("Importo gare", fmt_eur(gare["tot_gara"]))
k4.metric("Importo aggiudicato", fmt_eur(gare["tot_agg"]))

st.divider()

# ── Stato avanzamento ─────────────────────────────────────────────
st.subheader("Stato di avanzamento progetti")
stato = query_progetti("""
    SELECT stato_avanzamento, COUNT(DISTINCT cup) AS n_progetti,
           ROUND(SUM(fin_pnrr)) AS fin_pnrr
    FROM clean_input GROUP BY 1 ORDER BY 3 DESC
""")

col1, col2 = st.columns(2)
with col1:
    fig = px.pie(stato, names="stato_avanzamento", values="n_progetti",
                 title="Per numero progetti")
    fig.update_layout(height=350)
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.pie(stato, names="stato_avanzamento", values="fin_pnrr",
                 title="Per finanziamento PNRR")
    fig.update_layout(height=350)
    st.plotly_chart(fig, width="stretch")

st.divider()

# ── Top missioni ──────────────────────────────────────────────────
st.subheader("Top missioni per finanziamento")
miss = query_progetti("""
    SELECT missione, descrizione_missione,
           COUNT(DISTINCT cup) AS n_progetti,
           ROUND(SUM(fin_pnrr)) AS fin_pnrr
    FROM clean_input GROUP BY 1, 2 ORDER BY 4 DESC
""")

# Adatta unità al range dei dati
max_val = miss["fin_pnrr"].max()
if max_val >= 1e9:
    miss_display = miss.copy()
    miss_display["fin_pnrr_display"] = miss_display["fin_pnrr"] / 1e9
    y_col = "fin_pnrr_display"
    y_label = "Fin. PNRR (mld €)"
else:
    miss_display = miss.copy()
    miss_display["fin_pnrr_display"] = miss_display["fin_pnrr"] / 1e6
    y_col = "fin_pnrr_display"
    y_label = "Fin. PNRR (mln €)"

fig = px.bar(miss_display, x="descrizione_missione", y=y_col,
             color="missione",
             labels={y_col: y_label, "descrizione_missione": "Missione"})
fig.update_layout(height=450, xaxis_tickangle=-45, xaxis_title="", yaxis_title=y_label)
fig.update_traces(texttemplate="%{y:.1f} mld €" if "mld" in y_label else "%{y:.0f} mln €",
                  textposition="outside", textfont_size=10)
st.plotly_chart(fig, width="stretch")

st.caption("Dati: Italia Domani (MEF/SoGeI) · Fonte: open-pnrr")
