""" Contains WikiNamespace type """


# noinspection PyShadowingBuiltins
# pylint: disable=too-few-public-methods,redefined-builtin
class WikiNamespace:
    """ Holds data used to identify wiki namespace """
    id: int
    name: str
    has_content: bool

    def __init__(self, id: int, name: str, has_content: bool) -> None:
        super().__init__()

        self.id = id
        self.name = name
        self.has_content = has_content
