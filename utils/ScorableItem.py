""" Contains generic type for items that contain score """
from abc import abstractmethod
from typing import Protocol, List


# pylint: disable=too-few-public-methods
class ScorableItem(Protocol):
    """ Generic class representing item that has score """
    _score: int

    @abstractmethod
    def _get_score_fields(self) -> List[str]:
        pass
