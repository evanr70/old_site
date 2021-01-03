"""py-static

Usage:
    py-static.py
    py-static.py pages
    py-static.py posts
    py-static.py page <file>
    py-static.py post <file>
    py-static.py update-index
"""


import re
from glob import glob
from pathlib import Path
from docopt import docopt

from bs4 import BeautifulSoup, Comment
from syntax_highlighting import highlight_html
from vega import add_vega_plots

from templates import make_page_from_template

_pages_directory = Path("_pages")
_post_directory = Path("_posts")
_page_output = Path("pages")
_post_output = Path("posts")
_anchor_directory = Path("/") / _post_output

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

    soup = make_page_from_template(input_data)
    apply_directives(soup)

    with output_file.open("w") as f:
        f.write(soup.prettify())


def make_page(file_name):
    page_file = Path(file_name)
    compile_page(page_file, _page_output)


def make_pages():
    page_files = _pages_directory.glob("*.html")
    for page in page_files:
        compile_page(page, _page_output)


def make_post(file_name):
    post_file = Path(file_name)
    compile_page(post_file, _post_output)


def make_posts():
    post_files = _post_directory.glob("*.html")
    for post in post_files:
        compile_page(post, _post_output)


def update_post_index():
    post_file = _page_output / "posts.html"
    with post_file.open() as f:
        post_soup = BeautifulSoup(f, "html.parser")

    div = post_soup.find("div", id="content")
    container = post_soup.new_tag("div", attrs={"class": "container"})
    div.append(container)
    ul = post_soup.new_tag("ul")
    container.append(ul)

    post_files = _post_output.glob("*.html")
    for post in post_files:
        a_tag = post_soup.new_tag(
            "a",
            attrs={
                "href": str(Path("/") / post),
                "class": "text-decoration-none",
            },
        )
        a_tag.string = post.name.replace(".html", "").replace("_", " ")
        li = post_soup.new_tag("li")
        li.append(a_tag)
        ul.append(li)

    with post_file.open("w") as f:
        f.write(post_soup.prettify())


def make_all():
    make_pages()
    make_posts()
    update_post_index()


if __name__ == "__main__":
    args = docopt(__doc__, version="0.0.0")
  
    if args["posts"]:
        make_posts()
        update_post_index()
    elif args["pages"]:
       make_pages()
    elif args["page"]:
        make_page(args["<file>"])
    elif args["post"]:
        make_post(args["<file>"])
    elif args["update-index"]:
        update_post_index()
    else:
        make_all()
      
