""" Contains class for handling keyword events from Ulauncher"""

from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from utils.ResultList import ResultList

if TYPE_CHECKING:
    from main import WikiSearchExtension


# pylint: disable=too-few-public-methods
class KeywordQueryEventListener(EventListener):
    """ Handles users input and searches for results """

    def on_event(self, event: KeywordQueryEvent, extension: 'WikiSearchExtension') -> \
            RenderResultListAction:
        """
        Handles the keyword event
        :param event: Event data
        :param extension: Extension class
        :return: List of actions to render
        """

        query = event.get_argument()
        results = ResultList(query or "", min_score=60, limit=8)

        if query:
            results.extend(extension.search(query))

        items = []
        if len(results) == 0:
            items.append(
                ExtensionResultItem(
                    icon=extension.get_base_icon(),
                    name="No results found",
                    on_enter=HideWindowAction()
                )
            )
            return RenderResultListAction(items)

        for page in results:
            items.append(
                ExtensionResultItem(
                    name=page.title,
                    description=f"{page.wiki.site['sitename']} - {page.description}",
                    icon=extension.get_base_icon(),
                    on_enter=OpenUrlAction(page.to_url())
                )
            )

        return RenderResultListAction(items)
