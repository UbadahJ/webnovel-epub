from typing import Optional

from ebooklib import epub

from webnovel.epub.models.book import EpubBook as InnerEpubBook


def create_epub(book: InnerEpubBook, title: Optional[str] = None):
    ebook = epub.EpubBook()
    ebook.set_title(book.title)
    ebook.add_author(book.author)
    ebook.set_language('en')
    if book.image is not None:
        ebook.set_cover('cover.jpg', book.image)

    chapters: list[epub.EpubHtml] = []
    for c in book.chapters:
        html = epub.EpubHtml(title=c.title, file_name=f'c{c.index}.xhtml', lang='en')
        contents = ''.join([
            f'<p>{line}</p>'
            for line in c.contents.split('\n')
        ])
        html.set_content(f'<html><body><h1>{c.title}</h1>{contents}</body></html>')
        chapters.append(html)

    for c in chapters:
        ebook.add_item(c)

    ebook.toc = tuple(chapters)
    ebook.spine = tuple(chapters)
    ebook.add_item(epub.EpubNcx())
    ebook.add_item(epub.EpubNav())

    if title is None:
        title = book.title

    epub.write_epub(f'{title}.epub', ebook)
