from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer


def add_pygments_css(soup):
    tag = soup.new_tag(
        "link",
        attrs={
            "href": "../css/pygments.css",
            "rel": "stylesheet",
        },
    )
    soup.head.append(tag)


def highlight_html(soup):
    add_pygments_css(soup)

    for item in soup.find_all("code", lang="python"):
        code_text = highlight(item.text, PythonLexer(), HtmlFormatter(wrapcode=True))
        s2 = BeautifulSoup(code_text, "html.parser")
        item.parent.replace_with(s2)
