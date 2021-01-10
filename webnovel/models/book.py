import json
from typing import Callable

from requests_html import Element, HTMLSession, HTML

from webnovel.models.chapter import Chapter
from webnovel.models.downloader import Downloader


class Book:
    link: str
    id: str
    name: str
    author: str
    cover: bytes
    category: str
    description: str
    chapters: list[Chapter]

    def __init__(self, link: str) -> None:
        self.link = link
        self.id = link.rsplit('_', maxsplit=1)[-1]
        self._fetch()

    def download(self,
                 downloader: Callable[[list[Chapter]], Downloader],
                 progress: Callable[[str], None] = lambda s: None):
        self.chapters = downloader(self.chapters).fetch(progress)

    def _fetch(self):
        r: HTML
        doc: dict
        link: str
        with HTMLSession() as session:
            r = session.get(self.link).html
            link = r.url
            doc = session.get(f'https://www.webnovel.com/apiajax/chapter/GetChapterList?'
                              f'_csrfToken={session.cookies["_csrfToken"]}'
                              f'&bookId={self.id}').json()['data']

        self.name = doc['bookInfo']['bookName']
        info = json.loads(r.find('script[type="application/ld+json"]', first=True).text)[0]
        self.author = info['author']['name']
        self.category = info['articleSection']
        self.cover = session.get(f"https:{info['image']['url']}").content
        self.chapters = [
            Chapter(chapter['name'], f'{link}/{chapter["name"]}_{chapter["id"]}', chapter["index"],
                    chapter["isVip"] != 0)
            for volume in doc['volumeItems']
            for chapter in volume['chapterItems']
        ]

    def _extract_toc(self, el: Element) -> None:
        self.chapters = [
            Chapter(a.attrs['title'], list(a.absolute_links)[0], i, len(a.find('svg')) != 0)
            for i, a in enumerate(el.find('a'), start=1)
        ]
