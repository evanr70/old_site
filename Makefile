build:
	@echo "Creating files"
	python compile.py
	@echo "Completed"
	
	@echo "Committing files"
	git add --all
	git commit -m "automatic commit"
	git push
	
	@echo "Finished."
