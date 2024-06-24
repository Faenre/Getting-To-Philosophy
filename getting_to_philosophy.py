"""
This plays Getting To Philosophy, a Wikipedia game first described by
user Mark J in May of 2008.

The rules are available here:
https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy

For more information please view the README.md.
"""

import argparse

from src.philosophy import Philosophy


DEFAULT_MAX_HOPS = 100
DEFAULT_TARGET = 'Philosophy'

DESCRIPTION = """\
Starting from a given article, this script "gets to Philosophy", according to \
the Wikipedia game as described at:

https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy

At present, only the English (en) localization is supported.
"""


def parse_args():
    """Define and parse the command-line options."""
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('-m', '--max-hops', type=int, default=DEFAULT_MAX_HOPS,
        help='The maximum number of hops we should consider before stopping.')
    parser.add_argument('-t', '--target', type=str, default=DEFAULT_TARGET,
        help='The target Wikipedia article to search for. Default is Philosophy.')
    parser.add_argument('article', type=str,
        help='A Wikipedia URL or the name of a valid article to start from')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    game = Philosophy(args.target, args.max_hops)
    result = game.play(args.article)

    print(result.description)
    print(f"{len(game.hops)} hops.")
