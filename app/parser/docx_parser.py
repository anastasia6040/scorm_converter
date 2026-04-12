from docx import Document
from docx.oxml.ns import qn
import os

from .models import (
    ParsedDocument, Heading, Paragraph, ImageBlock,
    Table, TableRow, TableCell, ElementType
)


def parse_docx(file_path: str) -> ParsedDocument:
    doc = Document(file_path)
    result = ParsedDocument()
    image_counter = 1

    for para in doc.paragraphs:
        style = para.style.name  # например "Heading 1", "Normal"
        text = para.text.strip()

        # --- Заголовки ---
        if style.startswith("Heading"):
            try:
                level = int(style.split()[-1])  # "Heading 2" → 2
            except ValueError:
                level = 1

            level = min(level, 3)  # ограничиваем до H3

            if not result.title and level == 1:
                result.title = text  # первый H1 становится заголовком документа

            result.elements.append(Heading(level=level, text=text))

        # --- Изображения внутри параграфа ---
        elif _has_image(para):
            for rel in doc.part.rels.values():
                if "image" in rel.reltype:
                    image_data = rel.target_part.blob
                    ext = rel.target_part.content_type.split("/")[-1]  # png, jpeg...
                    if ext == "jpeg":
                        ext = "jpg"
                    filename = f"image{image_counter}.{ext}"
                    image_counter += 1
                    result.images[filename] = image_data
                    result.elements.append(ImageBlock(filename=filename))
                    break  # одно изображение на параграф

        # --- Обычный текст ---
        elif text:
            bold = all(run.bold for run in para.runs if run.text.strip())
            italic = all(run.italic for run in para.runs if run.text.strip())
            result.elements.append(Paragraph(text=text, bold=bold, italic=italic))

    # --- Таблицы ---
    for table in doc.tables:
        parsed_table = Table()
        for row in table.rows:
            parsed_row = TableRow()
            for cell in row.cells:
                parsed_row.cells.append(TableCell(text=cell.text.strip()))
            parsed_table.rows.append(parsed_row)
        result.elements.append(parsed_table)

    if not result.title:
        result.title = "Без названия"

    return result


def _has_image(para) -> bool:
    """Проверяет, содержит ли параграф изображение."""
    return para._p.find(qn("a:blip")) is not None