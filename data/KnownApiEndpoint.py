""" Contains KnownApiEndpoint type """
from typing import Pattern

from dotmap import DotMap


# pylint: disable=too-few-public-methods
class KnownApiEndpoint(DotMap):
    """ Holds data used to identify known API endpoints """
    regex: Pattern[str]
    path: str
