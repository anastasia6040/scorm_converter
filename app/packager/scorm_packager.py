import zipfile
import os
import io


def pack_scorm(
    html_content: str,
    manifest_content: str,
    images: dict[str, bytes],  # имя → байты
    output_path: str,
) -> None:
    """
    Упаковывает всё в .zip файл по стандарту SCORM 1.2.
    output_path — куда сохранить архив, например /tmp/result.zip
    """
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("index.html", html_content.encode("utf-8"))
        zf.writestr("imsmanifest.xml", manifest_content.encode("utf-8"))

        for filename, data in images.items():
            zf.writestr(f"images/{filename}", data)