"""An object to store and iterate across data within a Wikipedia page."""

from bs4 import BeautifulSoup
import regex as re


class Page:
    """
    An object to store and iterate across data within a Wikipedia page.
    """

    def __init__(self, url, html, parent=None):
        self.url = url
        self.html = html
        self.parent = parent
        self.links = self.__find_links()
        self.title = self.url.split('/')[-1]
        self.__index = 0

    def next_link(self):
        """
        Starting at index 0, return the next link and increment the counter.
        Successive page calls should return the next link instead of looping endlessly.
        """

        if self.__index < len(self.links):
            link = self.links[self.__index]
            self.__index += 1
            return link

        # If we run out of links on the page, we've hit a dead-end.
        # Return the parent if it exists.
        if self.parent:
            return self.parent

        # No parent and no remaining children means the iteration must end.
        raise StopIteration

    def __find_links(self):
        # Example: https://en.wikipedia.org/w/rest.php/v1/page/Jupiter/html
        links = []
        page_content = self.__wiki_page_content_as_soup(self.html)

        # We only care about the article's paragraph content,
        # not image links, table contents, or anything else.
        for p in page_content.find_all('p', recursive=True):
            # Remove <i>italics</i> and (parentheses)
            paragraph = self.__remove_clarifiers(p)

            # Collect HTTP references from <a> tags and filter for intrawiki links
            links += self.__parse_paragraph(paragraph)

        return links

    def __wiki_page_content_as_soup(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        page_content = soup.find(class_='mw-parser-output')
        if not page_content:
            page_content = soup.find('body')

        for table in page_content.find_all('table'):
            table.decompose()

        return page_content


    def __remove_clarifiers(self, node):
        # Convert node to html, then remove parentheses
        text = str(node)
        text, _ = re.subn(r'\s\(.*?\)', '', text)
        # The above regex matches all characters within a pair of (parentheses),
        # so long as the opening bracket is preceeded with whitespace. This protects
        # links, such as https://en.wikipedia.org/wiki/Character_(arts).

        # Create new BeautifulSoup node and remove spans and italics
        new_node = BeautifulSoup(text, 'html.parser')
        tags_to_ignore = ['i', 'span', 'table']
        for tag in tags_to_ignore:
            for ignorable in new_node.find_all(tag):
                ignorable.decompose()

        return new_node

    def __parse_paragraph(self, paragraph):
        # Collect HTTP references from <a> tags and filter for intrawiki links

        # The web API tags wiki links, so we'll rely on those.
        links = [ a.get('href') for a in paragraph.find_all('a', rel="mw:WikiLink") ]

        # If the result brings nothing, the page might not have them tagged (such
        # as if we're visiting the page directly.)
        #
        # In this case, we'll try scanning for intrawiki links. These links are
        # always root-relative, rather than page-relative.
        if not links:
            links = list(filter(
                    lambda href: href.startswith('/wiki/') if href else None,
                    [ a.get('href') for a in paragraph.find_all('a') ]
                ))

        return links
