all: clean build commit push

rebuild: clean build

build:
	@echo "Creating files"
	python scripts/compile.py

clean:
	@echo "Removing old html files."
	rm -f docs/*.html docs/posts/*.html

commit:
	@echo "Committing files"
	git add --all
	git commit -m "automatic commit"

push:
	git push
