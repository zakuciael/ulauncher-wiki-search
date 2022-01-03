""" Ulauncher extension that lets you search and open MediaWiki pages """

from ulauncher.api.client.Extension import Extension


class WikiSearchExtension(Extension):
    """ Main Extension Class  """

    def __init__(self):
        """ Initializes the extension """
        super().__init__()


if __name__ == "__main__":
    WikiSearchExtension().run()
