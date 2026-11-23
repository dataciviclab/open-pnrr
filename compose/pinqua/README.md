# PINQuA — finanziato, appaltato, pagato

Compose **mart-only** sul Programma Innovativo Nazionale per la Qualità dell'Abitare
(PNRR **M5C2I2.3**). Nessun raw, nessun clean: quattro support esterni, quattro mart.

## Cosa risponde

Il PINQuA finanzia 909 CUP (924 interventi) in 278 comuni. I tre dataset PNRR permettono di
seguire ogni intervento lungo tutta la catena:

| Passo | Fonte | Valore | Su finanziato |
|---|---|---:|---:|
| finanziato | `pnrr_progetti` | **2.540,8 mln** | — |
| appaltato con CIG | `pnrr_gare` (5.851 CIG) | **2.093,2 mln** | **82,4%** |
| appaltato senza CIG | `pnrr_gare` (141 righe) | 175,2 mln | 6,9% |
| aggiudicazione ANAC | `anac_aggiudicazioni` (3.842 CIG) | 2.075,5 mln | 81,7% |
| avanzamento | `anac_stati_avanzamento` (780 CIG) | 111 SAL in ritardo | — |
| pagato | `pnrr_pagamenti` | **1.516,9 mln** | **59,7%** |

**Il 99,4% che si ottiene sommando le righe di `pnrr_gare` è un artefatto**: 157 CIG sono
duplicati (un contratto che copre più CUP/interventi) con lo stesso importo. La somma corretta
è **un importo per CIG**. Vedi `mart_pinqua_catena`: `aggiudicato_cig` e `aggiudicato_senza_cig`
sono separati proprio per non mescolare le due semantiche.

## Mart

| Tabella | Grano | Contenuto |
|---|---|---|
| `mart_pinqua_interventi` | CUP × intervento | finanziato, aggiudicato, pagato, % pagato, stato, date |
| `mart_pinqua_comuni` | comune | CUP, interventi, quota finanziamento (278 comuni) |
| `mart_pinqua_regioni` | regione | CUP, comuni, interventi, quota (20 regioni) |
| `mart_pinqua_catena` | nazionale | il funnel in una riga, con le due semantiche di appaltato |
| `mart_pinqua_gare` | CIG | importo PNRR e ANAC, ribasso, offerte, SAL, stato avanzamento |
| `mart_pinqua_fisico` | CUP | avanzamento fisico: alloggi ERP/ERS, studentati, mq di spazi pubblici |

## Avanzamento fisico (mart_pinqua_fisico)

`pnrr_indicatori_target` espone `valore_programmato` e `valore_realizzato` per CUP:

| Indicatore | CUP | A zero | Programmato | Realizzato | % |
|---|---:|---:|---:|---:|---:|
| Alloggi ERP | 227 | **165 (73%)** | 9.997 | **3.391** | **33,9%** |
| Alloggi ERS | 150 | 125 (83%) | 2.537 | 250 | 9,9% |
| Posti studentati | 36 | 30 (83%) | 431 | 24 | 5,6% |
| Spazi pubblici (mq) | 765 | 521 (68%) | 7,99 M | 1,62 M | 20,3% |

**272 CUP con un target di alloggi non hanno consegnato un solo alloggio.** La consegna non è
lenta e uniforme: è ferma quasi ovunque e concentrata in pochi CUP (51 hanno raggiunto il
target). Il campo `stato_avanzamento` di `pnrr_progetti` sottostima: a fronte di 100 interventi
"concluso" (2,5% delle risorse), il 34% degli alloggi ERP risulta realizzato.

**Discrepanza sui mq**: la somma dei programmati per CUP è ~8,0 mln, il target di programma è
800.000 mq. Il target è un pavimento, non la somma dei progetti: non confrontare i due numeri.

## Caveat

- **Join sul CUP, non sul codice misura**: la misura è `M5C2I2.3` in `pnrr_progetti` ma
  `M5C2I2.03.01` in `pnrr_gare` e `pnrr_pagamenti`.
- **`aggiudicato` può superare `fin_pnrr`** per un singolo intervento: la gara copre il
  contratto intero, il finanziamento PNRR solo la sua quota. A livello aggregato i due
  coincidono (99,4%).
- **10 CUP su 909 sono multi-comune** (fino a 29): nei mart comunale e regionale i costi
  sono ripartiti in parti uguali, altrimenti la somma gonfia (3,69 vs 3,25 mld). I tre mart
  chiudono sullo stesso totale progetti, verificato nel run.
- **`pnrr_gare` e ANAC non coincidono sullo stesso CIG**: sui 3.842 CIG presenti in entrambe,
  il nostro importo per CIG somma 2.075,5 mln, ANAC 2.112,3 mln (+1,7%). Non è un errore di
  join: i due campi non misurano la stessa cosa (quota PNRR vs importo del contratto). Non
  sommarli e non sceglierne uno in silenzio.
- **ANAC copre il valore, non il numero**: 2.009 CIG su 5.851 non hanno un'aggiudicazione ANAC,
  ma valgono 17,7 mln (0,8%): sono micro-affidamenti. Il 34% dei CIG mancanti è il 2% del valore.
- **Il SAL copre 780 CIG su 5.851 (13%)**: 744 in linea, 36 con almeno un SAL in ritardo (111
  SAL in ritardo in totale). L'assenza di SAL non significa lavori fermi: significa nessun
  avanzamento comunicato ad ANAC.
- **909 CUP qui, 959 nella relazione della Corte dei Conti** (Delib. 58/2024): il 5% di
  differenza è da indagare; non blocca il compose.
- **2.540,8 mln PNRR ≠ 2.161,5 mln "ammessi a finanziamento"** del D.M. 383/2021: il primo è
  il finanziamento monitorato per intervento, il secondo l'importo del decreto.
- È una misura **PNRR, non PNC** (`fin_pnc = 0`).
- Readiness `incomplete (4/8)` è strutturale per un compose mart-only: i check su raw e clean
  non si applicano.
