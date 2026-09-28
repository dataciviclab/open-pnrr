"""Scadenze — Maturity wall dei progetti PNRR."""

import streamlit as st
import plotly.graph_objects as go
from sources import query_progetti, fmt_eur, fmt_num

st.title("⏰ Scadenze PNRR")

# ── Filtri ────────────────────────────────────────────────────────
HORIZON_MAP = {
    "30 giorni": 30,
    "60 giorni": 60,
    "90 giorni": 90,
}

col1, col2 = st.columns(2)
with col1:
    horizon_label = st.selectbox("Orizzonte", list(HORIZON_MAP.keys()), index=0)
with col2:
    missione_filter = st.multiselect(
        "Missione",
        ["M1", "M2", "M3", "M4", "M5", "M6", "M7"],
        default=["M1", "M2", "M3", "M4", "M5", "M6", "M7"],
    )

days = HORIZON_MAP[horizon_label]

# ── Query scadenze ───────────────────────────────────────────────
scadenze = query_progetti(f"""
    SELECT
        cup, titolo_progetto, missione, descrizione_missione,
        stato_avanzamento, data_fine_prevista, data_fine_effettiva,
        ROUND(fin_pnrr) AS fin_pnrr, ROUND(fin_totale) AS fin_totale,
        soggetto_attuatore
    FROM clean_input
    WHERE data_fine_prevista IS NOT NULL
      AND data_fine_prevista >= CURRENT_DATE
      AND data_fine_prevista <= CURRENT_DATE + INTERVAL '{days}' DAY
      AND missione IN ({','.join(repr(m) for m in missione_filter)})
    ORDER BY data_fine_prevista
""")

if scadenze.empty:
    st.warning("Nessun progetto in scadenza nel periodo selezionato.")
    st.stop()

# ── KPI ───────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Progetti in scadenza", fmt_num(len(scadenze)))
k2.metric("Fin. PNRR", fmt_eur(scadenze["fin_pnrr"].sum()))
k3.metric("Già completati", fmt_num(int((scadenze["data_fine_effettiva"].notna()).sum())))
k4.metric("In corso", fmt_num(int((scadenze["data_fine_effettiva"].isna()).sum())))

st.divider()

# ── Maturity wall ─────────────────────────────────────────────────
st.subheader(f"Maturity Wall — Prossimi {days} giorni")

# Raggruppa per settimana
scadenze["settimana"] = scadenze["data_fine_prevista"].dt.to_period("W").apply(lambda r: r.start_time)
wall = scadenze.groupby("settimana").agg(
    n_progetti=("cup", "count"),
    fin_pnrr=("fin_pnrr", "sum"),
).reset_index().sort_values("settimana")

fig = go.Figure()
fig.add_trace(go.Bar(
    x=wall["settimana"].dt.strftime("%d/%m"),
    y=wall["fin_pnrr"] / 1e6,
    name="Fin. PNRR (mln €)",
    marker_color="#6366f1",
    text=wall["n_progetti"],
    textposition="auto",
    hovertemplate="Settimana: %{x}<br>Progetti: %{text}<br>PNRR: %{y:.1f} mln €<extra></extra>",
))
fig.update_layout(
    xaxis_title="Settimana",
    yaxis_title="Finanziamento PNRR (mln €)",
    height=400,
    margin={"t": 30},
    showlegend=False,
)
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Per missione ──────────────────────────────────────────────────
st.subheader("Per missione")
miss = scadenze.groupby(["missione", "descrizione_missione"]).agg(
    n_progetti=("cup", "count"),
    fin_pnrr=("fin_pnrr", "sum"),
).reset_index().sort_values("fin_pnrr", ascending=False)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=miss["descrizione_missione"],
    y=miss["fin_pnrr"] / 1e6,
    name="Fin. PNRR",
    marker_color="#6366f1",
    text=miss["n_progetti"],
    textposition="auto",
))
fig.update_layout(
    xaxis_title="",
    yaxis_title="Fin. PNRR (mln €)",
    height=400,
    xaxis_tickangle=-45,
    margin={"t": 20, "b": 100},
)
st.plotly_chart(fig, width="stretch")

st.divider()

# ── Tabella dettaglio ────────────────────────────────────────────
st.subheader(f"Dettaglio progetti ({len(scadenze)})")

st.dataframe(
    scadenze[[
        "cup", "titolo_progetto", "missione", "stato_avanzamento",
        "data_fine_prevista", "data_fine_effettiva", "fin_pnrr",
    ]].rename(columns={
        "cup": "CUP", "titolo_progetto": "Titolo", "missione": "Miss.",
        "stato_avanzamento": "Stato", "data_fine_prevista": "Scadenza",
        "data_fine_effettiva": "Fine eff.", "fin_pnrr": "PNRR (€)",
    }),
    width="stretch",
    hide_index=True,
    height=400,
)

st.caption("Dati: Italia Domani (MEF/SoGeI) · Fonte: open-pnrr")
