from glob import glob
from pathlib import Path
import re
from syntax_highlighting import highlight_html
from bs4 import BeautifulSoup, Comment
from vega import add_vega_plots

#
#def apply_directives(soup):
#    


pages_directory = Path("_pages")
post_directory = Path("_posts")

# Play nicely with gh-pages
output_directory = Path("docs")

template_directory = Path("templates")
default_template = "home"
template_pattern = re.compile("<!--template: (.*?)-->")

page_files = list(pages_directory.glob("*.html"))
post_files = list(post_directory.glob("*.html"))

page_outputs = [output_directory / file.name for file in page_files]
post_outputs = [output_directory / file.name for file in post_files]

output_files = page_outputs + post_outputs
input_files = page_files + post_files

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

#    highlighted = highlight_html(input_data)

    output_data = template_data.replace("{{{CONTENT}}}", input_data)

    soup = BeautifulSoup(output_data, "html.parser")
    highlight_html(soup)

    code_css_tag = soup.new_tag("link")
    code_css_tag.attrs["href"] = "css/pygments.css"
    code_css_tag.attrs["rel"] = "stylesheet"
    soup.head.append(code_css_tag)

    add_vega_plots(soup)

    with output_file.open("w") as f:
        f.write(soup.prettify())
