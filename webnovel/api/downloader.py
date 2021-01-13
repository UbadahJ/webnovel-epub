from typing import Callable

import requests_html
from bs4 import BeautifulSoup

from webnovel.models.chapter import Chapter


class Downloader:
    __chapters: list[Chapter]
    __session: requests_html.AsyncHTMLSession = requests_html.AsyncHTMLSession()
    _progress: Callable[[str], None]
    _counter: int = 0

    def __init__(self, chapters: list[Chapter], ignore_premium=True) -> None:
        if ignore_premium:
            chapters = [c for c in chapters if not c.premium]

        self.__chapters = chapters

    def fetch(self, progress: Callable[[str], None] = lambda _: None) -> list[Chapter]:
        self._progress = progress
        responses = self.__session.run(*[
            self._download(c)
            for c in self.__chapters
        ])
        self._progress('Downloaded')
        self._progress('Cleaning up ...')
        responses.sort(key=lambda t: t[0])

        for chapter, (_, content) in zip(self.__chapters, responses):
            chapter.contents = Downloader._extract(content.text)

        return self.__chapters

    def _download(self, chapter: Chapter) -> Callable[[], tuple[int, str]]:
        async def actual():
            _o = (chapter.index, await self.__session.get(chapter.link))
            self._counter += 1
            self._progress(f'Downloaded {self._counter} / {len(self.__chapters)}')
            return _o

        return actual

    @staticmethod
    def _extract(html: str) -> str:
        doc = BeautifulSoup(html, 'html.parser')
        for pirate in doc.findAll('pirate'):
            pirate.decompose()

        return '\n'.join([
            p.get_text().strip()
            for p in doc.find(class_='cha-content').findAll('p')
        ])
