import zipfile
import os


def pack_scorm(
    html_content: str,
    manifest_content: str,
    images: dict[str, bytes],
    output_path: str,
    xsd_dir: str,              # ← новый параметр: путь к папке со схемами
) -> None:
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("index.html", html_content.encode("utf-8"))
        zf.writestr("imsmanifest.xml", manifest_content.encode("utf-8"))

        for filename, data in images.items():
            zf.writestr(f"images/{filename}", data)

        # Копируем XSD-схемы в корень архива
        if os.path.isdir(xsd_dir):
            for xsd_file in os.listdir(xsd_dir):
                if xsd_file.endswith(".xsd"):
                    xsd_path = os.path.join(xsd_dir, xsd_file)
                    with open(xsd_path, "rb") as f:
                        zf.writestr(xsd_file, f.read())