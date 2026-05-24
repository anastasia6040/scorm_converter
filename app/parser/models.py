from dataclasses import dataclass, field
from enum import Enum


class ElementType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    IMAGE = "image"
    TABLE = "table"
    LIST_ITEM = "list_item"


class Alignment(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


@dataclass
class RunSegment:
    """Один кусочек текста внутри параграфа со своим форматированием."""
    text: str = ""
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str | None = None        # hex цвет, например "FF0000"
    highlight: bool = False         # жёлтая/зелёная подсветка маркером
    link: str | None = None


@dataclass
class Heading:
    type: ElementType = ElementType.HEADING
    level: int = 1
    text: str = ""


@dataclass
class Paragraph:
    type: ElementType = ElementType.PARAGRAPH
    runs: list[RunSegment] = field(default_factory=list)
    alignment: Alignment = Alignment.LEFT
    background: str | None = None   # hex цвет фона параграфа, например "ffffff"

    @property
    def text(self) -> str:
        """Полный текст параграфа — удобно для быстрой проверки."""
        return "".join(r.text for r in self.runs)


@dataclass
class ListItem:
    type: ElementType = ElementType.LIST_ITEM
    runs: list[RunSegment] = field(default_factory=list)
    ordered: bool = False           # True = нумерованный, False = маркированный

    @property
    def text(self) -> str:
        return "".join(r.text for r in self.runs)


@dataclass
class ImageBlock:
    type: ElementType = ElementType.IMAGE
    filename: str = ""
    caption: str = ""               # подпись под рисунком, если есть


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


DocumentElement = Heading | Paragraph | ListItem | ImageBlock | Table


@dataclass
class Section:
    """Раздел документа — начинается с H1 и содержит все элементы до следующего H1."""
    title: str = ""
    elements: list[DocumentElement] = field(default_factory=list)


@dataclass
class ParsedDocument:
    title: str = ""
    sections: list[Section] = field(default_factory=list)
    elements: list[DocumentElement] = field(default_factory=list)
    images: dict[str, bytes] = field(default_factory=dict)
