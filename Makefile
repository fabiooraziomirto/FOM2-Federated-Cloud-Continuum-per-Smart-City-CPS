.PHONY: validate test paper
validate:
	python3 -I descriptor/validate.py descriptor/example.yaml
test:
	cd orchestrator && python3 -m pytest -q
paper:
	cd paper && latexmk -pdf -interaction=nonstopmode main.tex
