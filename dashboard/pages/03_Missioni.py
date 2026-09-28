"""Missioni — Breakdown per missione e componente PNRR."""

import streamlit as st
import plotly.express as px
from sources import query_progetti, fmt_eur, fmt_num

st.title("🎯 Missioni PNRR")

# ── Dati missione ────────────────────────────────────────────────
miss = query_progetti("""
    SELECT missione, descrizione_missione,
           COUNT(DISTINCT cup) AS n_progetti,
           ROUND(SUM(fin_pnrr)) AS fin_pnrr,
           ROUND(SUM(fin_totale)) AS fin_totale,
           COUNT(DISTINCT soggetto_attuatore) AS n_soggetti
    FROM clean_input GROUP BY 1, 2 ORDER BY 4 DESC
""")

# ── KPI totali ───────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
k1.metric("Missioni", fmt_num(len(miss)))
k2.metric("Progetti totali", fmt_num(int(miss["n_progetti"].sum())))
k3.metric("Fin. PNRR totale", fmt_eur(miss["fin_pnrr"].sum()))

st.divider()

# ── Bar chart missioni ───────────────────────────────────────────
st.subheader("Finanziamento per missione")

# Adatta unità al range dei dati
max_val = miss["fin_pnrr"].max()
if max_val >= 1e9:
    miss_display = miss.copy()
    miss_display["fin_pnrr_display"] = miss_display["fin_pnrr"] / 1e9
    y_col = "fin_pnrr_display"
    y_label = "Fin. PNRR (mld €)"
    text_fmt = "%{y:.1f} mld €"
else:
    miss_display = miss.copy()
    miss_display["fin_pnrr_display"] = miss_display["fin_pnrr"] / 1e6
    y_col = "fin_pnrr_display"
    y_label = "Fin. PNRR (mln €)"
    text_fmt = "%{y:.0f} mln €"

fig = px.bar(miss_display, x="descrizione_missione", y=y_col,
             color="missione",
             hover_data=["n_progetti", "n_soggetti"],
             labels={y_col: y_label, "descrizione_missione": "Missione"})
fig.update_layout(height=450, xaxis_tickangle=-45, xaxis_title="", yaxis_title=y_label)
fig.update_traces(texttemplate=text_fmt, textposition="outside", textfont_size=10)
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Dettaglio missione ───────────────────────────────────────────
st.subheader("Dettaglio missione")
missione_sel = st.selectbox("Seleziona missione", miss["descrizione_missione"].tolist())

comp = query_progetti(f"""
    SELECT componente, descrizione_componente,
           COUNT(DISTINCT cup) AS n_progetti,
           ROUND(SUM(fin_pnrr)) AS fin_pnrr,
           ROUND(SUM(fin_totale)) AS fin_totale,
           COUNT(DISTINCT soggetto_attuatore) AS n_soggetti,
           SUM(CASE WHEN stato_avanzamento = 'Concluso' THEN 1 ELSE 0 END) AS conclusi
    FROM clean_input
    WHERE descrizione_missione = '{missione_sel.replace("'", "''")}'
    GROUP BY 1, 2 ORDER BY 4 DESC
""")

k1, k2, k3 = st.columns(3)
k1.metric("Componenti", fmt_num(len(comp)))
k2.metric("Progetti", fmt_num(int(comp["n_progetti"].sum())))
k3.metric("Fin. PNRR", fmt_eur(comp["fin_pnrr"].sum()))

st.dataframe(
    comp.rename(columns={
        "componente": "Cod.", "descrizione_componente": "Componente",
        "n_progetti": "Progetti", "fin_pnrr": "PNRR (€)",
        "fin_totale": "Totale (€)", "n_soggetti": "Soggetti",
        "conclusi": "Conclusi",
    }),
    width="stretch",
    hide_index=True,
)

st.divider()

# ── Stato avanzamento per missione ────────────────────────────────
st.subheader(f"Stato avanzamento — {missione_sel}")
stato = query_progetti(f"""
    SELECT stato_avanzamento,
           COUNT(DISTINCT cup) AS n_progetti,
           ROUND(SUM(fin_pnrr)) AS fin_pnrr
    FROM clean_input
    WHERE descrizione_missione = '{missione_sel.replace("'", "''")}'
    GROUP BY 1 ORDER BY 3 DESC
""")

col1, col2 = st.columns(2)
with col1:
    fig = px.pie(stato, names="stato_avanzamento", values="n_progetti",
                 title="Per numero progetti")
    fig.update_layout(height=300)
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.pie(stato, names="stato_avanzamento", values="fin_pnrr",
                 title="Per finanziamento PNRR")
    fig.update_layout(height=300)
    st.plotly_chart(fig, width="stretch")

st.caption("Dati: Italia Domani (MEF/SoGeI) · Fonte: open-pnrr")
