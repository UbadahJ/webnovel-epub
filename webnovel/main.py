import sys

from rich.console import Console

from webnovel.epub.epub import create_epub
from webnovel.epub.models.book import EpubBook
from webnovel.epub.models.chapter import EpubChapter
from webnovel.models.book import Book
from webnovel.api.downloader import Downloader

console = Console()


def main(link: str) -> None:
    book = Book(link)
    with console.status('Starting ...') as status:
        book.download(lambda chs: Downloader(chs), lambda s: status.update(status=s))

    create_epub(EpubBook(book.name, [
        EpubChapter(c.index, f'Chapter {c.index}: {c.title}', c.contents)
        for c in book.chapters
    ], book.author, book.cover))


if __name__ == '__main__':
    main(sys.argv[1])