""" Contains WikiPage type """

from __future__ import annotations

import re
# noinspection PyPep8Naming
from urllib.parse import ParseResult as URL, quote as encodeURL

# noinspection PyPep8Naming
from mwclient import Site as API

TITLE_SAFE_CHARACTERS = "/ "
SPACE_REPLACEMENT = "_"


# pylint: disable=too-few-public-methods
class WikiPage:
    """ Holds data used to identify wiki pages """
    wiki: API
    page_id: int
    title: str
    display_title: str
    description: str

    _score: int = 0

    # pylint: disable=too-many-arguments
    def __init__(self, wiki: API, page_id: int, title: str, display_title: str,
                 extract: str) -> None:
        super().__init__()
        self.wiki = wiki
        self.page_id = page_id
        self.title = title
        self.display_title = display_title
        self.description = self._escape_formatting(extract)

        if not self.description or self.description == "...":
            self.description = "No description"

    @staticmethod
    def _escape_formatting(text: str):
        return re.sub(r"\s+", " ", text).strip()

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
