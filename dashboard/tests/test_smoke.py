"""Smoke test — verifica che tutte le pagine siano importabili."""

import py_compile
from pathlib import Path

DASHBOARD = Path(__file__).parent.parent
PAGES = DASHBOARD / "pages"

def test_all_pages_importable():
    """Ogni pagina deve essere sintatticamente valida."""
    for f in sorted(PAGES.glob("*.py")):
        py_compile.compile(str(f), doraise=True)
