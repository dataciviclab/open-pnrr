"""Gare — Funnel e analisi delle gare PNRR."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sources import query_gare, fmt_num

st.title("📋 Gare PNRR")

# ── Funnel ────────────────────────────────────────────────────────
gare = query_gare("""
    SELECT
        COUNT(*) AS totale,
        SUM(CASE WHEN cig IS NOT NULL THEN 1 ELSE 0 END) AS con_cig,
        SUM(CASE WHEN importo_aggiudicazione IS NOT NULL THEN 1 ELSE 0 END) AS aggiudicate,
        ROUND(SUM(COALESCE(importo_complessivo_gara, 0))) AS tot_importo_gara,
        ROUND(SUM(COALESCE(importo_aggiudicazione, 0))) AS tot_importo_agg
    FROM clean_input
""").iloc[0]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Gare totali", fmt_num(int(gare["totale"])))
k2.metric("Con CIG", fmt_num(int(gare["con_cig"])))
k3.metric("Aggiudicate", fmt_num(int(gare["aggiudicate"])))
rapporto = (gare["tot_importo_agg"] / gare["tot_importo_gara"] * 100) if gare["tot_importo_gara"] else 0
k4.metric("Rapporto agg./gara", f"{rapporto:.1f}%")

st.divider()

# ── Funnel chart ──────────────────────────────────────────────────
st.subheader("Funnel gare")
funnel_data = [
    ("Pubblicate", int(gare["totale"])),
    ("Con CIG", int(gare["con_cig"])),
    ("Aggiudicate", int(gare["aggiudicate"])),
]
fig = go.Figure(go.Funnel(
    y=[f[0] for f in funnel_data],
    x=[f[1] for f in funnel_data],
    textinfo="value+percent initial",
    marker_color="#6366f1",
))
fig.update_layout(height=350, margin={"t": 20})
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Per procedura aggiudicazione ──────────────────────────────────
st.subheader("Per procedura di aggiudicazione")
proc = query_gare("""
    SELECT descrizione_procedura_aggiudicazione,
           COUNT(*) AS n_gare,
           ROUND(SUM(COALESCE(importo_aggiudicazione, 0))) AS importo_agg
    FROM clean_input
    GROUP BY 1 HAVING COUNT(*) >= 10
    ORDER BY importo_agg DESC
    LIMIT 10
""")

# Trunca nomi lunghi per il grafico
proc_chart = proc.copy()
proc_chart["procedura_short"] = proc_chart["descrizione_procedura_aggiudicazione"].apply(
    lambda x: x[:40] + "..." if len(str(x)) > 40 else x
)
# Inverti per Plotly (mostra il più alto in alto)
proc_chart = proc_chart.iloc[::-1]

col1, col2 = st.columns(2)
with col1:
    # Adatta unità al range dei dati
    max_val = proc_chart["importo_agg"].max()
    if max_val >= 1e9:
        proc_chart["importo_agg_display"] = proc_chart["importo_agg"] / 1e9
        y_col = "importo_agg_display"
        y_label = "Importo aggiudicato (mld €)"
        text_fmt = "%{y:.1f} mld €"
    else:
        proc_chart["importo_agg_display"] = proc_chart["importo_agg"] / 1e6
        y_col = "importo_agg_display"
        y_label = "Importo aggiudicato (mln €)"
        text_fmt = "%{y:.0f} mln €"

    fig = px.bar(proc_chart, x=y_col, y="procedura_short", orientation="h",
                 labels={y_col: y_label, "procedura_short": "Procedura"})
    fig.update_layout(height=max(400, len(proc_chart) * 35), yaxis_title="",
                      xaxis_title=y_label, margin={"l": 300})
    fig.update_traces(texttemplate="%{x:.1f} mld €" if "mld" in y_label else "%{x:.0f} mln €",
                      textposition="outside", textfont_size=10)
    st.plotly_chart(fig, width="stretch")

with col2:
    st.dataframe(proc.rename(columns={
        "descrizione_procedura_aggiudicazione": "Procedura",
        "n_gare": "Gare", "importo_agg": "Agg. (€)",
    }), width="stretch", hide_index=True)

st.divider()

# ── Top 20 gare per importo ──────────────────────────────────────
st.subheader("Top 20 gare per importo")
top = query_gare("""
    SELECT cup, cig, oggetto_principale_contratto,
           descrizione_procedura_aggiudicazione,
           ROUND(importo_complessivo_gara) AS imp_gara,
           ROUND(importo_aggiudicazione) AS imp_agg,
           data_pubblicazione_cig, data_aggiudicazione_definitiva
    FROM clean_input
    WHERE importo_aggiudicazione IS NOT NULL
    ORDER BY importo_aggiudicazione DESC
    LIMIT 20
""")

st.dataframe(
    top.rename(columns={
        "cup": "CUP", "cig": "CIG", "oggetto_principale_contratto": "Oggetto",
        "descrizione_procedura_aggiudicazione": "Procedura",
        "imp_gara": "Imp. Gara (€)", "imp_agg": "Imp. Agg. (€)",
        "data_pubblicazione_cig": "Pubblicazione", "data_aggiudicazione_definitiva": "Aggiudicazione",
    }),
    width="stretch",
    hide_index=True,
)

st.caption("Dati: Italia Domani (MEF/SoGeI) · Fonte: open-pnrr")
