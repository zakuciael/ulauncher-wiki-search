""" Ulauncher extension that lets you search and open MediaWiki pages """
import os
import re
from typing import cast
# noinspection PyPep8Naming
from urllib.parse import ParseResult as URL, urlparse

import requests
import validators
from bs4 import BeautifulSoup
# noinspection PyPep8Naming
from mwclient import Site as API
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent

from data import MEDIA_WIKI_DETECTION_REGEXES_META, MEDIA_WIKI_DETECTION_REGEXES_CONTENT, \
    COMMON_API_ENDPOINTS, KNOWN_API_ENDPOINTS, MEDIA_WIKI_USER_AGENT
from events.KeywordQueryEventListener import KeywordQueryEventListener


class WikiSearchExtension(Extension):
    """ Main Extension Class  """

    def __init__(self):
        """ Initializes the extension """
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    @staticmethod
    def get_base_icon():
        """
        Returns the base (project) icon
        :return: None
        """

        path = os.path.join(os.path.dirname(__file__), "images", "icon.svg")
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError("Cant find base icon")

        return path

    @staticmethod
    def _parse_url(raw_url: str) -> URL | None:
        """
        Validates and parses provided URL
        :param raw_url: URL to parse
        :return: Parsed URL or None if invalid
        """

        # Add dummy "http" schema in front of the URL if it starts with "//" to support RFC 1808
        if validators.url("http:" + raw_url if re.match(r"^//", raw_url) else raw_url):
            return urlparse(raw_url)
        if validators.domain(raw_url):
            return urlparse("//" + raw_url)

        return None

    @staticmethod
    def _url_to_api(url: URL) -> API:
        """
        Converts URL into MediaWiki API object
        :param url: URL to convert
        :return: MediaWiki API object
        """

        return API(
            host=url.netloc,
            scheme=url.scheme,
            path=url.path,
            clients_useragent=MEDIA_WIKI_USER_AGENT,
            force_login=False
        )

    @staticmethod
    def _request(url: str, params=None, **kwargs):
        r"""
        Wrapper for the `requests.get` method
        that automatically adds proper user agent to the request
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
        :param kwargs: \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return requests.get(url, params=params, **kwargs,
                            headers={"user-agent": MEDIA_WIKI_USER_AGENT})

    # noinspection PyProtectedMember
    def _get_api(self, url: URL) -> API | None:
        """
        Resolves MediaWiki API from the provided url
        :param url: URL pointing to the MediaWiki site
        :return: MediaWiki API or None if not resolved
        """

        # If there is no scheme specified set it as "http" and relay on the https redirect
        if not url.scheme:
            url = url._replace(scheme="http")

        res = self._request(url.geturl())

        # Maybe the site doesn't support https redirects? Let's try doing that manually
        if not res.ok:
            url = url._replace(scheme="https")
            res = self._request(url.geturl())

        # Either the response was unsuccessful or the returned response type was not HTML
        content_type = res.headers.get("content-type")
        if not res.ok or "text/html" not in (content_type or ""):
            return None

        new_url = urlparse(res.url)
        url = url._replace(scheme=new_url.scheme)

        # Let's check if the site is running MediaWiki
        media_wiki: bool = any(
            regex.findall(res.text) for regex in MEDIA_WIKI_DETECTION_REGEXES_CONTENT)

        if not media_wiki:
            soup = BeautifulSoup(res.text, 'html.parser')
            media_wiki = any(regex.match(
                (soup.find("meta", attrs={'name': key}) or {}).get("content") or ""
            ) for key, regex in MEDIA_WIKI_DETECTION_REGEXES_META.items())

        if not media_wiki:
            return None

        # Final part, let's resolve the actual API endpoint

        # First let's check common websites
        known_api_endpoint = next(endpoint_data for endpoint_data in KNOWN_API_ENDPOINTS if
                                  endpoint_data.regex.match(cast(str, url.hostname)))

        if known_api_endpoint:
            url = url._replace(path=known_api_endpoint.path)
            return self._url_to_api(url)

        # Otherwise, check common API endpoints and try to determine the valid one
        for common_endpoint in COMMON_API_ENDPOINTS:
            url = url._replace(path=common_endpoint)
            res = self._request(url.geturl() + "api.php", params={
                "format": "json",
                "action": "query",
                "meta": "siteinfo",
                "siprop": "general"
            })

            content_type = res.headers.get("content-type")
            if res.ok and "application/json" in (content_type or "") and \
                    not res.json().get("error"):
                return self._url_to_api(url)

        return None


if __name__ == "__main__":
    extension = WikiSearchExtension()
    extension.run()
