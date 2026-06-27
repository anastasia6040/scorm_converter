from jinja2 import Environment, FileSystemLoader
import uuid


def generate_manifest(
    title: str,
    images: list[str],
    templates_dir: str,
    description: str | None = None,
    author: str | None = None,
    organization: str | None = None,
    language: str = "ru",
    version: str = "1.0",
    keywords: str | None = None,
) -> str:
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("imsmanifest.xml.j2")
    return template.render(
        identifier=f"scorm_{uuid.uuid4().hex[:8]}",
        title=title,
        images=images,
        description=description,
        author=author,
        organization=organization,
        language=language,
        version=version,
        keywords=keywords,
    )
