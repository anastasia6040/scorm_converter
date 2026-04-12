from dataclasses import dataclass, field
from enum import Enum


class ElementType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    IMAGE = "image"
    TABLE = "table"


@dataclass
class Heading:
    type: ElementType = ElementType.HEADING
    level: int = 1       # 1, 2 или 3 — соответствует H1, H2, H3 в HTML
    text: str = ""


@dataclass
class Paragraph:
    type: ElementType = ElementType.PARAGRAPH
    text: str = ""
    bold: bool = False
    italic: bool = False


@dataclass
class ImageBlock:
    type: ElementType = ElementType.IMAGE
    filename: str = ""   # имя файла, например "image1.png"


@dataclass
class TableCell:
    text: str = ""


@dataclass
class TableRow:
    cells: list[TableCell] = field(default_factory=list)


@dataclass
class Table:
    type: ElementType = ElementType.TABLE
    rows: list[TableRow] = field(default_factory=list)


# DocumentElement — это любой из перечисленных типов
DocumentElement = Heading | Paragraph | ImageBlock | Table


@dataclass
class ParsedDocument:
    title: str = ""                              # первый H1 из документа
    elements: list[DocumentElement] = field(default_factory=list)
    images: dict[str, bytes] = field(default_factory=dict)  # имя → байты