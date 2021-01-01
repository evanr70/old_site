build:
	echo "Creating files"
	echo "python compile.py"
	python compile.py
	echo "Completed"
	
	echo "Committing files"
	echo "git add --all"
	git add --all
	echo "git commit -m 'automatic commit'"
	git commit -m "automatic commit"
	echo "git push"
	git push
	
	echo "Finished."
