from jinja2 import Environment, FileSystemLoader
import uuid


def generate_manifest(title: str, images: list[str], templates_dir: str) -> str:
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("imsmanifest.xml.j2")
    return template.render(
        identifier=f"scorm_{uuid.uuid4().hex[:8]}",
        title=title,
        images=images,
    )