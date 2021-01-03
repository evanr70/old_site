import re
from glob import glob
from pathlib import Path

from bs4 import BeautifulSoup, Comment
from syntax_highlighting import highlight_html
from vega import add_vega_plots

from templates import make_page

_pages_directory = Path("_pages")
_post_directory = Path("_posts")
_page_output = Path("docs")
_post_output = Path("docs/posts")
_anchor_directory = Path().joinpath(*_post_output.parts[1:])

_page_output.mkdir(parents=True, exist_ok=True)
_post_output.mkdir(parents=True, exist_ok=True)


def apply_directives(soup):
    highlight_html(soup)
    add_vega_plots(soup)


def compile_page(input_file, output_directory):
    output_file = output_directory / input_file.name
    print(f"{str(input_file)} ----> {str(output_file)}")
    with input_file.open() as f:
        input_data = f.read()

    soup = make_page(input_data)
    apply_directives(soup)

    with output_file.open("w") as f:
        f.write(soup.prettify())


def make_pages():
    page_files = _pages_directory.glob("*.html")
    for page in page_files:
        compile_page(page, _page_output)


def make_posts():
    post_file = _page_output / "posts.html"
    with post_file.open() as f:
        post_soup = BeautifulSoup(f, "html.parser")
    div = post_soup.find("div", id="content")
    container = post_soup.new_tag("div", class_="container")
    div.append(container)
    ul = post_soup.new_tag("ul")
    container.append(ul)

    post_files = _post_directory.glob("*.html")
    for post in post_files:
        compile_page(post, _post_output)
        a_tag = post_soup.new_tag(
            "a",
            attrs={
                "href": str(_anchor_directory / post.name),
                "class": "text-decoration-none",
            },
        )
        a_tag.string = post.name.replace(".html", "").replace("_", " ")
        li = post_soup.new_tag("li")
        li.append(a_tag)
        ul.append(li)

    with post_file.open("w") as f:
        f.write(post_soup.prettify())


if __name__ == "__main__":
    make_pages()
    make_posts()
