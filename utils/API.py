""" Contains class extending mwclient's Site class to add more functionality """
from typing import Dict

from mwclient import Site

from data.WikiNamespace import WikiNamespace


# noinspection PyAttributeOutsideInit
# pylint: disable=too-many-instance-attributes
class API(Site):
    """ Class extending mwclient's Site class to provide more functionality """

    default_namespaces: Dict[int, WikiNamespace] = {}
    namespaces: Dict[int, WikiNamespace] = {}

    def site_init(self):
        if self.initialized:
            info = self.get(action="query", meta=["userinfo"], uiprop=["groups", "rights"])
            userinfo = info["query"]["userinfo"]
            self.username = userinfo["name"]
            self.groups = userinfo.get("groups", [])
            self.rights = userinfo.get("rights", [])
            self.tokens = {}
            return

        meta = self.get(
            action="query",
            meta=["siteinfo", "userinfo"],
            siprop=["general", "namespaces"],
            uiprop=["groups", "rights"],
            retry_on_error=False
        )

        # Extract site info
        self.site = meta["query"]["general"]
        self.namespaces = {
            namespace["id"]: WikiNamespace(
                namespace["id"],
                "Main" if not namespace["*"] and namespace["id"] == 0 else namespace["*"],
                "content" in namespace
            )
            for namespace in meta["query"]["namespaces"].values()
        }
        self.writeapi = "writeapi" in self.site

        self.version = self.version_tuple_from_generator(self.site["generator"])

        # Require MediaWiki version >= 1.16
        self.require(1, 16)

        # User info
        userinfo = meta["query"]["userinfo"]
        self.username = userinfo["name"]
        self.groups = userinfo.get("groups", [])
        self.rights = userinfo.get("rights", [])
        self.initialized = True

    # pylint: disable=keyword-arg-before-vararg
    def api(self, action, http_method="POST", *args, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, list):
                kwargs[key] = "|".join(map(str, value))
            if isinstance(value, bool):
                kwargs[key] = "true" if value else "false"

        return super().api(action, http_method, *args, **kwargs)
