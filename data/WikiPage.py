""" Contains WikiPage type """

from __future__ import annotations

import re
# noinspection PyPep8Naming
from urllib.parse import ParseResult as URL, quote as encodeURL

# noinspection PyPep8Naming
from mwclient import Site as API

from utils.ScorableItem import ScorableItem

TITLE_SAFE_CHARACTERS = "/ "
SPACE_REPLACEMENT = "_"


# noinspection PyShadowingBuiltins
# pylint: disable=too-few-public-methods,redefined-builtin
class WikiPage(ScorableItem):
    """ Holds data used to identify wiki pages """
    wiki: API
    id: int
    title: str
    display_title: str
    namespace: str

    _score: int = 0

    # pylint: disable=too-many-arguments
    def __init__(self, wiki: API, id: int, title: str, display_title: str, namespace: str) -> None:
        super().__init__()
        self.wiki = wiki
        self.id = id
        self.title = title
        self.display_title = display_title
        self.namespace = namespace

    def _get_score_fields(self) -> list[str]:
        return [self.title]

    def to_url(self) -> str:
        """
        Converts WikiPage object into URL
        :return: URL to the wiki page
        """

        safe_title = re.sub(r" ", SPACE_REPLACEMENT, encodeURL(self.title, safe="/ "))

        return URL(
            scheme=self.wiki.scheme,
            netloc=self.wiki.host,
            path=re.sub(r"\$1", safe_title, self.wiki.site["articlepath"]),
            query="",
            params="",
            fragment=""
        ).geturl()
