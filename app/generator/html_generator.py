from jinja2 import Environment, FileSystemLoader
import os

from app.parser.models import ParsedDocument


def generate_html(doc: ParsedDocument, templates_dir: str) -> str:
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("index.html.j2")
    return template.render(title=doc.title, elements=doc.elements, sections=doc.sections)