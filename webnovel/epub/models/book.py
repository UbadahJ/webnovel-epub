from dataclasses import dataclass
from typing import Optional

from webnovel.epub.models.chapter import EpubChapter


@dataclass
class EpubBook:
    title: str
    chapters: list[EpubChapter]

    author: str = ''
    image: Optional[bytes] = None
