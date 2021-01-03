import re
from pathlib import Path

from bs4 import BeautifulSoup, Comment

_vega_pattern = re.compile("vega: (.*?)$")
_vega_added = False


def add_vega_head(soup):
    sources = [
        "https://cdn.jsdelivr.net/npm//vega@5",
        "https://cdn.jsdelivr.net/npm//vega-lite@4.8.1",
        "https://cdn.jsdelivr.net/npm//vega-embed@6",
    ]

    style = soup.new_tag("style")
    style.string = ".error {color: red;}"
    soup.head.append(style)

    for source in sources:
        soup.head.append(
            soup.new_tag("script", attrs={"type": "text/javascript", "src": source})
        )


def add_vega_plots(soup):
    asset_directory = Path("assets")

    vega_comments = soup.find_all(
        string=lambda text: isinstance(text, Comment) and ("vega:" in text)
    )

    for comment in vega_comments:
        if not _vega_added:
            add_vega_head(soup)
        vega_file_name = _vega_pattern.search(comment.string).group(1)
        vega_file = (asset_directory / vega_file_name).with_suffix(".html")

        with open(vega_file) as f:
            vega_soup = BeautifulSoup(f.read(), "html.parser")

        comment.replace_with(vega_soup.body)
