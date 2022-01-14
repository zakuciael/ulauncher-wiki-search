""" Contains WikiPage type """

from __future__ import annotations

# noinspection PyPep8Naming
from mwclient import Site as API

from utils.ScorableItem import ScorableItem

# noinspection PyPep8Naming

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
    url: str

    _score: int = 0

    # pylint: disable=too-many-arguments
    def __init__(self, wiki: API, id: int, title: str,
                 display_title: str, namespace: str, url: str) -> None:
        super().__init__()
        self.wiki = wiki
        self.id = id
        self.title = title
        self.display_title = display_title
        self.namespace = namespace
        self.url = url

    def _get_score_fields(self) -> list[str]:
        return [self.title]
