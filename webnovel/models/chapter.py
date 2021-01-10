from dataclasses import dataclass
from typing import Optional


@dataclass
class Chapter(object):
    """
    A simple chapter object
    """
    title: str
    link: str
    index: Optional[int] = None
    premium: bool = False
    contents: str = ''
