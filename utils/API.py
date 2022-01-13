""" Contains class extending mwclient's Site class to add more functionality """

from mwclient import Site


# noinspection PyAttributeOutsideInit
# pylint: disable=too-many-instance-attributes
class API(Site):
    """ Class extending mwclient's Site class to provide more functionality """

    default_namespaces: dict = {}

    def site_init(self):
        if self.initialized:
            info = self.get('query', meta='userinfo', uiprop='groups|rights')
            userinfo = info['query']['userinfo']
            self.username = userinfo['name']
            self.groups = userinfo.get('groups', [])
            self.rights = userinfo.get('rights', [])
            self.tokens = {}
            return

        meta = self.get('query', meta='siteinfo|userinfo',
                        siprop='general|namespaces', uiprop='groups|rights',
                        retry_on_error=False)

        # Extract site info
        self.site = meta['query']['general']
        self.namespaces = meta['query']['namespaces']
        self.writeapi = 'writeapi' in self.site

        self.version = self.version_tuple_from_generator(self.site['generator'])

        # Require MediaWiki version >= 1.16
        self.require(1, 16)

        # User info
        userinfo = meta['query']['userinfo']
        self.username = userinfo['name']
        self.groups = userinfo.get('groups', [])
        self.rights = userinfo.get('rights', [])
        self.initialized = True
