""" Contains custom implementation of SortedList found in Ulauncher's code """
from typing import Iterator, TypeVar, Generic

from ulauncher.utils.SortedCollection import SortedCollection  # type: ignore
from ulauncher.utils.fuzzy_search import get_score  # type: ignore

from utils.ScorableItem import ScorableItem

T = TypeVar("T", bound=ScorableItem)


# noinspection PyProtectedMember
# pylint: disable=protected-access
class SortedList(Generic[T]):
    """
    List maintains items in a sorted order
    (sorted by a score, which is a similarity between item's name and a query)
    and limited to a number `limit` passed into the constructor
    """

    _query: str
    _min_score: int
    _limit: int
    _items: SortedCollection

    def __init__(self, query: str, min_score: int = 30, limit: int = 9) -> None:
        self._query = query.lower().strip()
        self._min_score = min_score
        self._limit = limit
        self._items = SortedCollection(key=lambda item: item._score)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, i: int) -> T:
        return self._items[i]

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __reversed__(self) -> Iterator[T]:
        return reversed(self._items)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" + \
               f"({self._items}, min_score={self._min_score}, limit={self._limit})"

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def extend(self, items: list[T]) -> None:
        """
        Merges all provided items into this list
        :param items: A list of items to merge
        """
        for item in items:
            self.append(item)

    def append(self, item: T) -> None:
        """
        Adds item to the list
        :param item: Item to add
        """

        score = max((get_score(self._query, value) for value in item._get_score_fields()))

        if score >= self._min_score:
            # use negative to sort by score in desc. order
            item._score = -score

            self._items.insert(item)
            while len(self._items) > self._limit:
                # remove items with the lowest score to maintain limited number of items
                self._items.pop()
