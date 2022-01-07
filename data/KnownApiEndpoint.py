""" Contains KnownApiEndpoint type """
from typing import Pattern


# pylint: disable=too-few-public-methods
class KnownApiEndpoint:
    """ Holds data used to identify known API endpoints """
    regex: Pattern[str]
    path: str

    def __init__(self, regex: Pattern[str], path: str) -> None:
        super().__init__()
        self.regex = regex
        self.path = path
