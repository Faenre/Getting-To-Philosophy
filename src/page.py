"""An object to store and iterate across data within a Wikipedia page."""

from bs4 import BeautifulSoup
import regex as re

from .constants import HOST


class Page:
    """
    An object to store and iterate across data within a Wikipedia page.
    """

    def __init__(self, url, html, parent=None):
        self.url = url
        self.html = html
        self.parent = parent
        self.links = self.__find_links()
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

    def page_title(self):
        return self.url.split('/wiki/')[-1]

    def __find_links(self):
        hrefs = []
        soup = BeautifulSoup(self.html, 'html.parser')
        page_content = soup.find(id='mw-content-text').find(class_='mw-parser-output')

        # We only care about paragraph content, not image links etc.
        for p in page_content.find_all('p', recursive=False):
            # Remove <i>italics</i> and (parentheses)
            paragraph = self.__remove_clarifiers(p)

            # Collect HTTP references from <a> tags and filter for intrawiki links
            hrefs += list(filter(
                    lambda href: href.startswith('/wiki/'),
                    [ a.get('href') for a in paragraph.find_all('a') ]
                ))

        # Append the URL to links
        links = [ HOST + href for href in hrefs ]
        return links

    def __remove_clarifiers(self, node):
        # Convert node to html, then remove parentheses
        text = str(node)
        text, _ = re.subn(r' \(.*?\)', '', text)
        # The above regex matches all characters within a pair of (parentheses),
        # so long as the opening bracket is preceeded with a space. This protects
        # links, such as https://en.wikipedia.org/wiki/Character_(arts).

        # Create new BeautifulSoup node and remove italics
        new_node = BeautifulSoup(text, 'html.parser')
        for italic in new_node.find_all('i'):
            italic.decompose()

        return new_node
