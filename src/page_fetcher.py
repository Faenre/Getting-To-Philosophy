"""Get pages from Wikipedia and make them available."""

import requests
from .page import Page
from .constants import HOST, USER_AGENT


HEADERS = {
    'User-Agent': USER_AGENT
}


class PageFetcher:
    """
    This class uses the Requests module to get webpages from Wikipedia
    and convert them into Page objects which form an indirect linked-list.
    """
    def __init__(self, session=None):
        self.url_to_page = {}
        self.session = session or requests.Session()
        self.session.headers = HEADERS

    def fetch_next(self, page):
        """This finds the next page and returns it."""
        return self.fetch(page.next_link(), page)

    def fetch(self, link, parent=None):
        """
        Given a page name, shortlink, or full URL, we either create
        or reuse a Page object and return it.
        """
        url = self.__shape_into_url(link)

        if url not in self.url_to_page:
            try :
                response = self.session.get(url)
                response.raise_for_status()
                html = response.text
                self.url_to_page[url] = Page(url, html, parent)
            except requests.exceptions.HTTPError as err:
                if response.status_code != 404:
                    print('Page does not exist!')
                    self.url_to_page[url] = None
                elif 400 <= response.status_code < 500:
                    print('Client error encountered. Exiting.')
                    raise SystemExit(err) from err
                elif 500 <= response.status_code < 600:
                    print('Server error encountered. Exiting.')
                    raise SystemExit(err) from err

        return self.url_to_page[url]

    def __shape_into_url(self, link):
        # link = link.replace(' ', '_')
        if link.startswith('https://') :
            return link
        if link.startswith('/wiki/') :
            return HOST + link
        return f'{HOST}/wiki/{link}'
