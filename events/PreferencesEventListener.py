""" Contains class for handling initial preference event from Ulauncher"""

from typing import TYPE_CHECKING

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import PreferencesEvent

if TYPE_CHECKING:
    from main import WikiSearchExtension


# pylint: disable=too-few-public-methods
class PreferencesEventListener(EventListener):
    """ Handles initial user settings and parses them """

    def on_event(self, event: PreferencesEvent, extension: 'WikiSearchExtension') -> None:
        """
        Handles the preference event
        :param event: Event data
        :param extension: Extension class
        """

        event.preferences["improved_titles"] = event.preferences["improved_titles"] == "True"
        event.preferences["improved_filters"] = event.preferences["improved_filters"] == "True"
        extension.preferences.update(event.preferences)

        extension.parse_wiki_urls(event.preferences.get("wiki_urls"))
