#!/usr/bin/env python3
"""PNRR Intelligence · Dashboard Streamlit"""

import streamlit as st
from lab_connectors.branding import apply_branding

st.set_page_config(
    page_title="PNRR Intelligence · Dashboard",
    page_icon="🇮🇹",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_branding(
    repo_name="open-pnrr",
    repo_url="https://github.com/dataciviclab/open-pnrr",
)

pages = {
    "Panoramica": [
        st.Page("pages/01_Panoramica.py", title="Panoramica", icon="📊", default=True),
        st.Page("pages/02_Scadenze.py", title="Scadenze", icon="⏰"),
    ],
    "Analisi": [
        st.Page("pages/03_Missioni.py", title="Missioni", icon="🎯"),
        st.Page("pages/04_Gare.py", title="Gare", icon="📋"),
        st.Page("pages/05_Pagamenti.py", title="Pagamenti", icon="💰"),
    ],
    "Esplorazione": [
        st.Page("pages/06_Scheda_CUP.py", title="Scheda CUP", icon="🔍"),
        st.Page("pages/07_SQL.py", title="Query SQL", icon="🧪"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
