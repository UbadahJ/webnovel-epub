import argparse

from rich.console import Console

from webnovel.api.downloader import Downloader
from webnovel.api.search import Search
from webnovel.epub.epub import create_epub
from webnovel.epub.models.book import EpubBook
from webnovel.epub.models.chapter import EpubChapter
from webnovel.models.book import Book

console = Console()


def main(link: str) -> None:
    book = Book(link)
    console.print(f'[bold]{book.name}[/bold]')
    console.print(f'by [grey italic]{book.author}[/grey italic]')
    console.print(f'{book.link}')
    console.print(f'[red bold]{book.category}[/red bold]')
    console.print(f'Free: {len([c for c in book.chapters if not c.premium])}; Total: {len(book.chapters)}')


def search(term: str) -> None:
    _search = Search(term)
    console.print('[bold]Search Results[/bold]')
    for i, res in enumerate(_search.results):
        console.print(f'{i}. {res.name} ({res.link}) [{res.rating} / 5.0]')
        if len(res.tags) != 0:
            console.print(*res.tags, sep=', ')
        console.print(f'[bold]Description[/bold]: {res.desc}\n')


def download(link: str) -> None:
    book = Book(link)
    with console.status('Starting ...') as status:
        book.download(lambda chs: Downloader(chs), lambda s: status.update(status=s))

    create_epub(EpubBook(book.name, [
        EpubChapter(c.index, f'Chapter {c.index}: {c.title}', c.contents)
        for c in book.chapters
    ], book.author, book.cover))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='The link to webnovel page or search term', type=str)
    parser.add_argument('-d', '--download', help='Download the book as well', action='store_true')
    parser.add_argument('-s', '--search', help='Search the given query instead of treating as link',
                        action='store_true')
    args = parser.parse_args()

    if not args.search:
        main(args.query)
        if args.download:
            download(args.query)
    else:
        search(args.search)
