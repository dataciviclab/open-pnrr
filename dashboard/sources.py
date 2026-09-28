"""Fonti dati per la dashboard PNRR Intelligence.

Multi-dataset: pnrr_progetti, pnrr_gare, pnrr_pagamenti.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from lab_connectors.duckdb.queries import (
    load_mart_table as _load_mart_table,
    query_clean as _query_clean,
)

try:
    from lab_connectors.duckdb.queries import detect_local_root
except ImportError:
    detect_local_root = None  # type: ignore[assignment]

ROOT = Path(__file__).parent.parent
PREFIX = "open-pnrr/"
YEARS = [2026]
LOCAL_ROOT = detect_local_root(repo_root=ROOT) if detect_local_root else None


def _q(slug: str, sql: str, year: int = 2026):
    kwargs = {"prefix": PREFIX}
    if LOCAL_ROOT:
        kwargs["local_root"] = LOCAL_ROOT
    return _query_clean(slug, sql, [year], **kwargs)


@st.cache_data(ttl=3600, show_spinner=False)
def query_progetti(sql: str, year: int = 2026):
    """Query su pnrr_progetti (clean layer)."""
    return _q("pnrr_progetti", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def query_gare(sql: str, year: int = 2026):
    """Query su pnrr_gare (clean layer)."""
    return _q("pnrr_gare", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def query_pagamenti(sql: str, year: int = 2026):
    """Query su pnrr_pagamenti (clean layer)."""
    return _q("pnrr_pagamenti", sql, year)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart(table: str, year: int = 2026):
    """Carica un singolo mart table da pnrr_progetti."""
    kwargs = {"prefix": PREFIX}
    if LOCAL_ROOT:
        kwargs["local_root"] = LOCAL_ROOT
    return _load_mart_table("pnrr_progetti", table, year, **kwargs)


from lab_connectors.formatters import fmt_num, fmt_pct  # noqa: F401,E402  # re-export for pages


def fmt_eur(val: float | int | None) -> str:
    """Formatta importi in euro con abbreviazione: € 4.1 mld, € 571 mln."""
    if val is None or val == 0:
        return "€ 0"
    abs_val = abs(val)
    if abs_val >= 1_000_000_000:
        return f"€ {val / 1_000_000_000:,.1f} mld".replace(",", ".")
    if abs_val >= 1_000_000:
        return f"€ {val / 1_000_000:,.0f} mln".replace(",", ".")
    if abs_val >= 1_000:
        return f"€ {val:,.0f}".replace(",", ".")
    return f"€ {val:,.0f}"
