## Descrizione

<!-- Breve descrizione della modifica -->

## Tipo

- [ ] Nuovo dataset
- [ ] Modifica pipeline esistente
- [ ] Fix bug
- [ ] Aggiornamento documentazione

## Checklist

- [ ] `dataset.yml` valido (`toolkit validate --config <file>`)
- [ ] `clean.sql` legge solo da `raw_input`
- [ ] `mart*.sql` legge solo da `clean_input`
- [ ] Nessun file dati committato in `out/` o `*.parquet`
- [ ] `.gitignore` aggiornato se necessario
- [ ] README/notes.md aggiornati
