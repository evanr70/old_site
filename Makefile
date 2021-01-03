all: clean build commit push

rebuild: clean build

build:
	@echo "Creating files"
	python scripts/compile.py
	ln -s pages/index.html index.html

clean:
	@echo "Removing old html files."
	rm -f pages/*.html posts/*.html index.html

commit:
	@echo "Committing files"
	git add --all
	git commit -m "automatic commit"

push:
	git push
