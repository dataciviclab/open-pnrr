"""Smoke tests: verifica che i parquet clean/mart esistano e siano leggibili."""

import glob
import os

import duckdb
import pytest

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "out", "data")

DATASETS = [
    "pnrr_progetti",
    "pnrr_gare",
    "pnrr_pagamenti",
    "pnrr_indicatori_target",
    "pnrr_avanzamento_indicatori",
    "pnrr_quadro_finanziario",
    "pnrr_tag_clima_digitale",
]


@pytest.mark.parametrize("slug", DATASETS)
def test_clean_parquet_exists(slug):
    """Ogni dataset deve avere almeno un clean parquet per il 2026."""
    pattern = os.path.join(OUT, "clean", slug, "2026", "*_clean.parquet")
    files = glob.glob(pattern)
    assert files, f"Nessun clean parquet trovato per {slug}: {pattern}"


@pytest.mark.parametrize("slug", DATASETS)
def test_clean_parquet_readable(slug):
    """Il clean parquet deve essere leggibile da DuckDB e avere righe > 0."""
    pattern = os.path.join(OUT, "clean", slug, "2026", "*_clean.parquet")
    files = glob.glob(pattern)
    assert files, f"Nessun clean parquet per {slug}"
    con = duckdb.connect()
    df = con.execute(f"SELECT COUNT(*) FROM read_parquet('{files[0]}')").fetchone()
    assert df[0] > 0, f"{slug}: 0 righe nel clean parquet"


@pytest.mark.parametrize("slug", DATASETS)
def test_mart_exists(slug):
    """Ogni dataset deve avere almeno un mart parquet per il 2026."""
    mart_dir = os.path.join(OUT, "mart", slug, "2026")
    if not os.path.isdir(mart_dir):
        pytest.skip(f"Cartella mart non trovata per {slug}")
    files = glob.glob(os.path.join(mart_dir, "*.parquet"))
    assert files, f"Nessun mart parquet trovato per {slug}"


def test_progetti_schema():
    """pnrr_progetti deve avere le colonne fondamentali."""
    pattern = os.path.join(OUT, "clean", "pnrr_progetti", "2026", "*_clean.parquet")
    files = glob.glob(pattern)
    assert files
    con = duckdb.connect()
    cols = [r[0] for r in con.execute(
        f"DESCRIBE SELECT * FROM read_parquet('{files[0]}')"
    ).fetchall()]
    required = {"cup", "missione", "fin_pnrr", "fin_totale", "stato_avanzamento"}
    assert required.issubset(set(cols)), f"Colonne mancanti: {required - set(cols)}"


def test_pagamenti_tasso_assorbimento():
    """Il tasso di assorbimento PNRR deve essere tra 0% e 100%."""
    pattern = os.path.join(OUT, "clean", "pnrr_pagamenti", "2026", "*_clean.parquet")
    files = glob.glob(pattern)
    assert files
    con = duckdb.connect()
    r = con.execute(f"""
        SELECT
            SUM(pagamento_pnrr) / NULLIF(SUM(finanziamento_pnrr), 0) * 100 AS pct
        FROM read_parquet('{files[0]}')
    """).fetchone()
    assert r[0] is not None, "Tasso di assorbimento è NULL"
    assert 0 < r[0] < 100, f"Tasso assorbimento fuori range: {r[0]:.1f}%"
