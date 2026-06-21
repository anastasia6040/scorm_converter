import re
import unicodedata


def safe_download_filename(title: str, suffix: str = "_package", ext: str = "zip") -> str:
    if not title:
        title = "scorm"

    title = unicodedata.normalize("NFC", title)

    forbidden = r'[\\/:*?"<>|\r\n\t]'
    cleaned = re.sub(forbidden, "", title)
    cleaned = "".join(ch for ch in cleaned if ch.isprintable())

    cleaned = re.sub(r"\s+", "_", cleaned.strip())
    cleaned = re.sub(r"_+", "_", cleaned)
    cleaned = cleaned.strip("._")

    if not cleaned:
        cleaned = "scorm"

    max_title_len = 120
    if len(cleaned) > max_title_len:
        cleaned = cleaned[:max_title_len].rstrip("._")

    return f"{cleaned}{suffix}.{ext}"