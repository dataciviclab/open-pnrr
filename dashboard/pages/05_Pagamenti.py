"""Pagamenti — Assorbimento fondi PNRR per missione."""

import streamlit as st
import plotly.express as px
from sources import query_pagamenti, fmt_eur, fmt_num

st.title("💰 Pagamenti PNRR")

# ── KPI totali ───────────────────────────────────────────────────
sintesi = query_pagamenti("""
    SELECT
        ROUND(SUM(finanziamento_pnrr)) AS fin_pnrr,
        ROUND(SUM(pagamento_pnrr)) AS pag_pnrr,
        ROUND(SUM(pagamento_pnrr) / NULLIF(SUM(finanziamento_pnrr), 0) * 100, 1) AS tasso_pct,
        COUNT(DISTINCT cup) AS n_progetti
    FROM clean_input
""").iloc[0]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Progetti con pagamenti", fmt_num(int(sintesi["n_progetti"])))
k2.metric("Finanziato PNRR", fmt_eur(sintesi["fin_pnrr"]))
k3.metric("Pagato PNRR", fmt_eur(sintesi["pag_pnrr"]))
k4.metric("Tasso assorbimento", f"{sintesi['tasso_pct']}%",
          delta="target 67%" if sintesi["tasso_pct"] < 67 else "target raggiunto",
          delta_color="inverse" if sintesi["tasso_pct"] < 67 else "normal")

st.divider()

# ── Per submisura (top 15) ───────────────────────────────────────
st.subheader("Per submisura (top 15 per finanziamento)")
sub = query_pagamenti("""
    SELECT codice_univoco_submisura, descrizione_submisura,
           COUNT(DISTINCT cup) AS n_progetti,
           ROUND(SUM(finanziamento_pnrr)) AS fin_pnrr,
           ROUND(SUM(pagamento_pnrr)) AS pag_pnrr,
           ROUND(SUM(pagamento_pnrr) / NULLIF(SUM(finanziamento_pnrr), 0) * 100, 1) AS tasso_pct
    FROM clean_input
    GROUP BY 1, 2
    HAVING SUM(finanziamento_pnrr) > 0
    ORDER BY 4 DESC
    LIMIT 15
""")

# Adatta unità al range dei dati
max_val = sub["fin_pnrr"].max()
if max_val >= 1e9:
    sub_display = sub.copy()
    sub_display["fin_pnrr_display"] = sub_display["fin_pnrr"] / 1e9
    y_col = "fin_pnrr_display"
    y_label = "Fin. PNRR (mld €)"
else:
    sub_display = sub.copy()
    sub_display["fin_pnrr_display"] = sub_display["fin_pnrr"] / 1e6
    y_col = "fin_pnrr_display"
    y_label = "Fin. PNRR (mln €)"

# Trunca nomi lunghi e raggruppa per nome corto
sub_chart = sub_display.copy()
sub_chart["submisura_short"] = sub_chart["descrizione_submisura"].apply(
    lambda x: x[:35] + "..." if len(str(x)) > 35 else x
)
sub_chart = sub_chart.groupby("submisura_short", as_index=False).agg({
    y_col: "sum", "n_progetti": "sum", "tasso_pct": "mean"
})
# Inverti per Plotly (mostra il più alto in alto)
sub_chart = sub_chart.iloc[::-1]

fig = px.bar(sub_chart, x=y_col, y="submisura_short", orientation="h",
             hover_data=["n_progetti", "tasso_pct"],
             labels={y_col: y_label, "submisura_short": "Submisura"})
fig.update_layout(height=max(400, len(sub_chart) * 30), yaxis_title="",
                  xaxis_title=y_label, margin={"l": 350})
fig.update_traces(texttemplate="%{x:.1f} mld €" if "mld" in y_label else "%{x:.0f} mln €",
                  textposition="outside", textfont_size=10)
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Dettaglio submisura ──────────────────────────────────────────
st.subheader("Dettaglio submisura")
sub_sel = st.selectbox("Seleziona submisura", sub["descrizione_submisura"].tolist())

det = query_pagamenti(f"""
    SELECT cup, finanziamento_pnrr, pagamento_pnrr,
           ROUND(pagamento_pnrr / NULLIF(finanziamento_pnrr, 0) * 100, 1) AS tasso_pct
    FROM clean_input
    WHERE descrizione_submisura = '{sub_sel.replace("'", "''")}'
      AND finanziamento_pnrr > 0
    ORDER BY pagamento_pnrr DESC
""")

k1, k2, k3 = st.columns(3)
k1.metric("Progetti", fmt_num(len(det)))
k2.metric("Fin. PNRR", fmt_eur(det["finanziamento_pnrr"].sum()))
k3.metric("Pagato", fmt_eur(det["pagamento_pnrr"].sum()))

st.dataframe(
    det.rename(columns={
        "cup": "CUP", "finanziamento_pnrr": "Fin. PNRR (€)",
        "pagamento_pnrr": "Pagato (€)", "tasso_pct": "Tasso %",
    }),
    width="stretch",
    hide_index=True,
    height=300,
)

st.caption("Dati: Italia Domani (MEF/SoGeI) · Fonte: open-pnrr")
