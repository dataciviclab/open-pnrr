"""Query SQL — Interroga direttamente i dati PNRR."""

from pathlib import Path

from lab_connectors.duckdb.sql_page import render_sql_query
from lab_connectors.registry import load_registry

registry = load_registry(
    Path(__file__).parent.parent.parent / "registry" / "registry.json"
)

render_sql_query(
    registry=registry,
    prefix="open-pnrr/",
    default_slug="pnrr_progetti",
    title="🧪 Query SQL PNRR",
    description="Interroga direttamente i dati. Scrivi SQL su ``clean_input``. "
                "Dataset disponibili: pnrr_progetti, pnrr_gare, pnrr_pagamenti.",
)
