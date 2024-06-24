"""Philosophy game-logic orchestration"""

from .exit_code import ExitCode
from .page_fetcher import PageFetcher


class Philosophy:
    """
    This is the main orchestrator for the Getting To Philosophy game.

    On initialization, it begins recording some variables and initializes
    a PageFetcher which handles gathering Wikipedia pages and storing their
    contents and link traversal information.
    """

    def __init__(self, target_article, max_hops):
        self.fetcher = PageFetcher()
        self.hops = []
        self.max_hops = max_hops
        self.target_page = self.fetcher.fetch(target_article)

    def play(self, article_name):
        """
        The entrypoint to playing the game. Feed it an article and it will go!
        """
        first_page = self.fetcher.fetch(article_name)

        return self.get_to_philosophy(first_page)

    def get_to_philosophy(self, current_page):
        """
        If you define your own current_page object, the game can still be played,
        but this may yield undefined results at this time.


        Conditions:
        - Philosophy found --> return success
        - Bad page given   --> indicate to user
        - Loop encountered --> triggered when a page has already been visited.
                               check the 2nd link, then 3rd, ...
        - Dead end         --> return to parent and try again (handled on Page obj)
        """

        # Exit if we've found the target, or if we're out of hops.
        if current_page is self.target_page:
            return ExitCode.SUCCESS
        if len(self.hops) == self.max_hops:
            return ExitCode.TOO_MANY_HOPS
        if current_page is None:
            return ExitCode.NO_CURRENT_PAGE

        try:
            # Increment the hops, and find the next page.
            next_page = self.fetcher.fetch_next(current_page)
            print(next_page.url)
            self.hops.append(next_page)
        except StopIteration:
            return ExitCode.DEAD_END

        return self.get_to_philosophy(next_page)
