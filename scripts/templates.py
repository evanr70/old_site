import re
from pathlib import Path

from bs4 import BeautifulSoup, Comment

_pattern = re.compile("<!--template: (.*?)-->")
_directory = Path("templates")
_default = "home"


def get_template(input_data):
    match = _pattern.search(input_data)

    file_name = _default if match is None else match.group(1)
    file = (_directory / file_name).with_suffix(".html")

    with file.open() as f:
        template = f.read()

    return template


def make_page(input_data):
    template = get_template(input_data)
    output_data = template.replace("{{{CONTENT}}}", input_data)
    return BeautifulSoup(output_data, "html.parser")
