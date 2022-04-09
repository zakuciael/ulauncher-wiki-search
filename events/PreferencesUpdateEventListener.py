""" Contains class for handling preference update events from Ulauncher"""

from typing import TYPE_CHECKING

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import PreferencesUpdateEvent

if TYPE_CHECKING:
    from main import WikiSearchExtension


# pylint: disable=too-few-public-methods
class PreferencesUpdateEventListener(EventListener):
    """ Handles updates to user settings and parses them """

    def on_event(self, event: PreferencesUpdateEvent, extension: 'WikiSearchExtension') -> \
            None:
        """
        Handles the preference update event
        :param event: Event data
        :param extension: Extension class
        """

        if event.id == "wiki_urls":
            extension.parse_wiki_urls(event.new_value)

        if event.id == "improved_titles":
            event.new_value = event.new_value == "True"

        if event.id == "improved_filters":
            event.new_value = event.new_value == "True"

        extension.preferences[event.id] = event.new_value
