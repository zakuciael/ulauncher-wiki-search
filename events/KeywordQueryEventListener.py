""" Contains class for handling keyword events from Ulauncher"""

from typing_extensions import TYPE_CHECKING
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

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

        return RenderResultListAction([
            ExtensionResultItem(
                name="Query",
                description=query,
                icon=extension.get_base_icon(),
                on_enter=HideWindowAction()
            )
        ])
