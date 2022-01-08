""" Contains WikiPage type """

from __future__ import annotations

import re
# noinspection PyPep8Naming
from typing import Optional, cast
from urllib.parse import ParseResult as URL, quote as encodeURL

from bs4 import BeautifulSoup
# noinspection PyPep8Naming
from mwclient import Site as API

IMAGE_REGEX = re.compile(r"\.(?:png|jpg|jpeg|gif)(?:/|\?|$)", re.IGNORECASE)
TITLE_SAFE_CHARACTERS = "/ "
SPACE_REPLACEMENT = "_"

IMAGE_SELECTORS: list[str] = [
    "tr img",
    "div.images img",
    "figure.pi-image img",
    "div.infobox-imagearea img"
]

INFOBOX_CLASS_NAMES: list[str] = [
    ".infobox",
    ".portable-infobox",
    ".infoboxtable",
    ".notaninfobox",
    ".tpl-infobox"
]


# pylint: disable=too-few-public-methods
class WikiPage:
    """ Holds data used to identify wiki pages """
    wiki: API
    page_id: int
    title: str
    display_title: str
    description: str
    icon: Optional[str]

    # pylint: disable=too-many-arguments
    def __init__(self, wiki: API, page_id: int, title: str, display_title: str,
                 extract: str) -> None:
        super().__init__()
        self.wiki = wiki
        self.page_id = page_id
        self.title = title
        self.display_title = display_title
        self.description = self._escape_formatting(extract)
        self.icon = None

    @staticmethod
    def _escape_formatting(text: str):
        # re.sub(r"\t", "", text)
        return re.sub(r"\s+", " ", text).strip()

    def to_advanced(self) -> WikiPage:
        """
        Super-charges this object with better description and icon
        :return: Super-charged wiki page object
        """

        result = self.wiki.get(
            action="parse",
            pageid=self.page_id,
            prop="text",
            section=0,
            disablelimitreport=True,
            disableeditsection=True,
            disabletoc=True,
            sectionpreview=True
        )

        if not result["parse"] or not result["parse"]["text"] or not result["parse"]["text"]["*"]:
            return self

        soup = BeautifulSoup(result["parse"]["text"]["*"], "html.parser")
        infobox = soup.select_one(", ".join(INFOBOX_CLASS_NAMES))

        if not infobox:
            return self

        image = next(
            (cast(str, ele.attrs["src"]) for ele in soup.select(", ".join(IMAGE_SELECTORS))
             if ele.attrs and ele.attrs["src"] and IMAGE_REGEX.findall(ele.attrs["src"])), None)

        if not image:
            return self

        self.icon = image

        infobox.extract()
        self.description = self._escape_formatting(soup.get_text())

        return self

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
