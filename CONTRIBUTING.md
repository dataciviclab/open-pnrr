# Contribuire a open-pnrr

## Dataset repo

Questo repo contiene dataset aperti sul PNRR con pipeline raw → clean → mart.

### Struttura

```
datasets/<slug>/
├── dataset.yml        # contratto pipeline
├── preprocess.py      # download fonte (wget + fallback urllib)
├── sql/
│   ├── clean.sql      # pulizia/typing (legge da raw_input)
│   └── mart*.sql      # aggregazioni (legge da clean_input)
├── README.md          # documentazione dataset
├── notes.md           # note tecniche
└── .gitignore         # esclude raw_input.csv
```

### Aggiungere un dataset

1. Creare `datasets/<slug>/` con la struttura sopra
2. Seguire `dataset.yml` come template (vedi `standards/pipeline.md`)
3. Testare: `TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run --config datasets/<slug>/dataset.yml`
4. Validare: `toolkit validate --config datasets/<slug>/dataset.yml`
5. Aprire PR

### Modifiche esistenti

1. Creare branch `fix/<descrizione>` o `feat/<descrizione>`
2. Modificare solo i file necessari
3. Testare la pipeline
4. Aprire PR con descrizione chiara

### Naming

- Dataset slug: `snake_case` dal nome fonte (es. `pnrr_progetti`)
- Branch: `feat/<descrizione>`, `fix/<descrizione>`
- Commit: descrittivo, in italiano o inglese

### Dipendenze

- `toolkit` — pipeline runner
- `lab-connectors` — utility condivise
- `duckdb` — motore SQL per parquet

### CI

La workflow `ci.yml` esegue `toolkit run preflight` su ogni PR.

### Regole

- Non committare output pipeline (`out/`, `*.parquet`, `*.csv` generati)
- Non committare `raw_input.csv` (escluso da `.gitignore`)
- Ogni `dataset.yml` deve passare `toolkit validate`
- Ogni `clean.sql` legge solo da `raw_input`
- Ogni `mart*.sql` legge solo da `clean_input`
