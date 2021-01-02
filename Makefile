all: clean build commit push

build:
	@echo "Creating files"
	python compile.py

clean:
	@echo "Removing old html files."
	rm -f docs/*.html

commit:
	@echo "Committing files"
	git add --all
	git commit -m "automatic commit"

push:
	git push
