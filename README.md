# Getting To Philosophy

This script plays the _[Getting To Philosophy](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy)_ game, recording the steps (or "hops") necessary to get from the beginning article towards the end.

The goal of the game is to "get to Philosophy" by following the first link of each page (with some exclusions), and counting how many "hops" it takes to get to the "Philosophy" page.

# Setup

This uses the [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/), [Regex](https://pypi.org/project/regex/), and [Requests](https://pypi.org/project/requests/) libraries, which you can install manually or via the requirements.txt file:

```sh
pip install -r requirements.txt
```

# Usage

Call the `getting_to_philosophy.py` script from the command line by specifying either an article name or a page URL. Quotes are necessary if there are any spaces or special characters.

```sh
python3.9 ./getting_to_philosophy.py villain
python3.9 ./getting_to_philosophy.py "https://en.wikipedia.org/wiki/Villain"
python3.9 ./getting_to_philosophy.py "Elizabeth I"
```

The script will crawl according to the rules specified in the game above:

```sh
❯ python3.9 ./getting_to_philosophy.py "Villain"
https://en.wikipedia.org/wiki/Stock_character
https://en.wikipedia.org/wiki/Character_(arts)
https://en.wikipedia.org/wiki/Fiction
https://en.wikipedia.org/wiki/Creative_work
...
https://en.wikipedia.org/wiki/Rule_of_inference
https://en.wikipedia.org/wiki/Philosophy_of_logic
https://en.wikipedia.org/wiki/Philosophy
Target found successfully!
31 hops.
```

Note that because Wikipedia is an evergreen project that constantly has contributions, it is possible that pages change even throughout the day. For example, the article about Thought [changed while I wrote this project](https://en.wikipedia.org/w/index.php?title=Thought&oldid=1230577918), then [reverted again overnight!](https://en.wikipedia.org/w/index.php?title=Thought&diff=1230692892&oldid=1230577918)

Also, an additional important call-out is that disambiguation pages **are not supported** in this version. For example, if you are interested in following Python, you need to supply either `"Python (programming language"` or `"Pythonidae"`.