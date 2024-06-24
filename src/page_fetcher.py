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

        Rate limiting was considered, but upon review of the Wikipedia guidelines,
        it was found that the suggested guidance is "no more than 200 requests per 
        second", and that sequential rather than synchronous reads do not typically
        hit this limit.

        This outlined here:
        https://www.mediawiki.org/wiki/Wikimedia_REST_API#Terms_and_conditions

        If a future version intends to somehow solve this in parallel processing,
        then implementing rate-limiting would become more relevant.
        """
        url = self.__shape_into_url(link)

        if url not in self.url_to_page:
            html = self.__get(url)
            self.url_to_page[url] = Page(url, html, parent)
        return self.url_to_page[url]

    def __get(self, url):
        """
        Given a possibly-relative page link, returns html content or None
        """
        try :
            api_url = self.__url_to_wiki_api(url)
            response = self.session.get(api_url)
            response.raise_for_status()
            html = response.text
            return html
        except requests.exceptions.HTTPError as err:
            if response.status_code != 404:
                print('Page does not exist!')
            elif 400 <= response.status_code < 500:
                print('Client error encountered. Exiting.')
                raise SystemExit(err) from err
            elif 500 <= response.status_code < 600:
                print('Server error encountered. Exiting.')
                raise SystemExit(err) from err
            return None

    def __shape_into_url(self, possibly_relative_link):
        if possibly_relative_link.startswith('https://en.wikipedia.org/wiki/'):
            return possibly_relative_link
        if possibly_relative_link.startswith('/wiki/'):
            return HOST + possibly_relative_link
        if possibly_relative_link.startswith('./'):
            return f'{HOST}/wiki/{possibly_relative_link[2:]}'
        return f'{HOST}/wiki/{possibly_relative_link}'

    def __url_to_wiki_api(self, url):
        """
        This attempts to convert a human-readable URL into the Wikimedia API url.

        Example: 
            input:  https://en.wikipedia.org/wiki/Arabic
            output: https://en.wikipedia.org/w/rest.php/v1/page/Arabic/html
        """
        page_title = url.split('/wiki/')[-1]
        api_link = f"https://en.wikipedia.org/w/rest.php/v1/page/{page_title}/html"
        return api_link
