import zipfile
import os


def pack_scorm(
    html_content: str,
    manifest_content: str,
    images: dict[str, bytes],
    output_path: str,
    xsd_dir: str,
    js_dir: str,
) -> None:
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("index.html", html_content.encode("utf-8"))
        zf.writestr("imsmanifest.xml", manifest_content.encode("utf-8"))

        for filename, data in images.items():
            zf.writestr(f"images/{filename}", data)

        if os.path.isdir(xsd_dir):
            for xsd_file in os.listdir(xsd_dir):
                if xsd_file.endswith(".xsd"):
                    xsd_path = os.path.join(xsd_dir, xsd_file)
                    with open(xsd_path, "rb") as f:
                        zf.writestr(xsd_file, f.read())

        if os.path.isdir(js_dir):
            for js_file in ["SCORM_API_wrapper.js", "scorm_12_libs.js"]:
                js_path = os.path.join(js_dir, js_file)
                if os.path.exists(js_path):
                    with open(js_path, "rb") as f:
                        zf.writestr(f"js/{js_file}", f.read())
