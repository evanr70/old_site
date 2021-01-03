from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from bs4 import BeautifulSoup


def highlight_html(soup):
    for item in soup.find_all("code", lang="python"):
        code_text = highlight(item.text, PythonLexer(), HtmlFormatter(wrapcode=True))
        s2 = BeautifulSoup(code_text, "html.parser")
        item.parent.replace_with(s2)
    