TOOLKIT = toolkit
BATCH ?= batch.txt

DATASETS := $(shell find datasets compose -name dataset.yml 2>/dev/null | sort)

.PHONY: check run run-all run-batch clean registry help

check:
	@for f in $(DATASETS); do \
		echo "→ $$f"; \
		$(TOOLKIT) run preflight --config "$$f" > /dev/null 2>&1 || exit 1; \
	done
	@echo "✅ All configs valid"

run:
	$(TOOLKIT) run

run-all:
	@find datasets compose -name dataset.yml | sort > batch.txt; \
	$(TOOLKIT) run --batch "$(BATCH)"

# Batch selettivo: consuma il batch.txt scritto dal workflow (solo dataset cambiati
# nella PR). Non rigenera il file, altrimenti annullerebbe la selezione.
run-batch:
	@if [ ! -s "$(BATCH)" ]; then echo "batch vuoto — niente da eseguire"; exit 0; fi; \
	$(TOOLKIT) run --batch "$(BATCH)"

clean:
	rm -rf out/data/_runs out/data/probe out/data/raw out/data/clean out/data/mart out/data/cross .tmp/

registry-write:
	$(TOOLKIT) registry build --prefix open-pnrr --write

help:
	@grep -E '^[a-zA-Z_-]+:' Makefile | sort
