from requests_html import HTMLSession, HTML, Element

from webnovel.models.searchres import SearchResult


class Search:
    query: str
    results: list[SearchResult]

    def __init__(self, query: str) -> None:
        self.query = query
        self.results = []

        self._get_results()

    def _get_results(self):
        r: HTML
        with HTMLSession() as session:
            r = session.get('https://www.webnovel.com/search', params={'keywords': self.query}).html

        container = r.find('.search-result-container', first=True)
        for li in container.find('li'):
            a = li.find('a', first=True)
            self.results.append(SearchResult(
                name=a.attrs['title'],
                link=f'https:{a.attrs["href"]}',
                tags=self._get_tags(li),
                rating=self._get_rating(li),
                desc=li.find('p.fs16.c_000', first=True).text
            ))

    @staticmethod
    def _get_tags(element: Element):
        try:
            return [a.text for a in element.find('.g_tags', first=True).find('a')]
        except AttributeError:
            return []

    @staticmethod
    def _get_rating(element: Element) -> float:
        try:
            return float(element.find('.g_star_num').find('small').text)
        except AttributeError:
            return 0
