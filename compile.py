from glob import glob
from pathlib import Path
import re


input_directory = Path("_pages")

# Play nicely with gh-pages
output_directory = Path("docs")

template_directory = Path("templates")
default_template = "home"
template_pattern = re.compile("<!--template: (.*?)-->")

input_files = list(input_directory.glob("[!_]*.html"))
output_files = [output_directory / file.name for file in input_files]

for input_file, output_file in zip(input_files, output_files):
    print(f"{str(input_file)} ----> {str(output_file)}")
    with input_file.open() as f:
        input_data = f.read()
    
    template = template_pattern.match(input_data)
    template = default_template if template is None else template.group(1)
    template_file = (template_directory / template).with_suffix(".html")
    print(f"Using template: {template}.")
    
    with template_file.open() as f:
      template_data = f.read()
        
    output_data = template_data.replace("{{{CONTENT}}}", input_data)
    
    with output_file.open("w") as f:
        f.write(output_data)
