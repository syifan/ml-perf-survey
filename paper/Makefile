# Makefile for ML Performance Models Survey Paper (MICRO 2026)

MAIN = main
LATEX = pdflatex
BIBTEX = bibtex

.PHONY: all clean view

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex references.bib acmart.cls ACM-Reference-Format.bst
	$(LATEX) $(MAIN)
	$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

clean:
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log $(MAIN).out $(MAIN).pdf $(MAIN).toc $(MAIN).lof $(MAIN).lot

view: $(MAIN).pdf
	open $(MAIN).pdf

# Quick build without bibliography
quick:
	$(LATEX) $(MAIN)
