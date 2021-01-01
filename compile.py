from glob import glob
from pathlib import Path

input_directory = Path("_pages")
output_directory = Path("static")
template = Path("_pages/_template.html")

for old_output in output_directory.glob("*"):
    old_output.unlink()

with template.open() as f:
    template = f.read()

input_files = list(input_directory.glob("[!_]*.html"))
output_files = [output_directory / file.name for file in input_files]

for input_file, output_file in zip(input_files, output_files):
    print(f"{str(input_file)} ----> {str(output_file)}")
    with input_file.open() as f:
        input_data = f.read()
        
    output_data = template.replace("{{{CONTENT}}}", input_data)
    
    with output_file.open("w") as f:
        f.write(output_data)
