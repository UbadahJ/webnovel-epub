from dataclasses import dataclass


@dataclass
class SearchResult:
    name: str
    link: str
    tags: list[str]
    rating: float
    desc: str
