from dataclasses import dataclass


@dataclass
class EpubChapter:
    index: int
    title: str
    contents: str
