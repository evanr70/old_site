from glob import glob
from pathlib import Path
import re
from syntax_highlighting import highlight_html
from bs4 import BeautifulSoup, Comment


def add_vega_plot(soup):
    asset_directory = Path("docs/assets")
  
    head = BeautifulSoup(
        '<style>.error{color:red;}</style><script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega@5"></script><script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-lite@4.8.1"></script><script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-embed@6"></script>',
        "html.parser",
    )

    soup.head.append(head)


    vega_comments = soup.find_all(
        string=lambda text: isinstance(text, Comment) and ("vega:" in text)
    )
    
    for comment in vega_comments:
        vega_file_name = re.match("vega: (.*?)$", comment.strip()).group(1)
        vega_file = (asset_directory / vega_file_name).with_suffix(".html")
        with open(vega_file) as f:
            vega_soup = BeautifulSoup(f.read(), "html.parser")

        comment.replace_with(vega_soup.body)


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

    highlighted = highlight_html(input_data)

    output_data = template_data.replace("{{{CONTENT}}}", highlighted)

    soup = BeautifulSoup(output_data, "html.parser")

    code_css_tag = soup.new_tag("link")
    code_css_tag.attrs["href"] = "css/pygments.css"
    code_css_tag.attrs["rel"] = "stylesheet"
    soup.head.append(code_css_tag)

    add_vega_plot(soup)

    with output_file.open("w") as f:
        f.write(soup.prettify())
