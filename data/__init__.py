""" Contains constants for the project """

import re
from typing import Pattern

from data.KnownApiEndpoint import KnownApiEndpoint

MEDIA_WIKI_DETECTION_REGEXES_CONTENT: list[Pattern[str]] = [
    re.compile(r'<body[^>]{1,250}class="mediawiki"', re.IGNORECASE),
    re.compile(r'<(?:a|img)[^>]{1,250}>Powered by MediaWiki</a>', re.IGNORECASE),
    re.compile(r'<a[^>]{1,250}/Special:WhatLinksHere/', re.IGNORECASE),
]

MEDIA_WIKI_DETECTION_REGEXES_META: dict[str, Pattern[str]] = {
    "generator": re.compile(r'^MediaWiki ?(.{1,250})$', re.IGNORECASE)
}

MEDIA_WIKI_USER_AGENT = \
    "Ulauncher Wiki Search (https://github.com/zakuciael/ulauncher-wiki-search)"

COMMON_API_ENDPOINTS = ["/", "/w/", "/wiki/"]

KNOWN_API_ENDPOINTS: list[KnownApiEndpoint] = [
    KnownApiEndpoint(
        regex=re.compile(r"^(?!www).+\.fandom.com$", re.IGNORECASE),
        path="/"
    ),
    KnownApiEndpoint(
        regex=re.compile(r"^(?!www).+\.wikipedia.org$", re.IGNORECASE),
        path="/w/"
    ),
    KnownApiEndpoint(
        regex=re.compile(r"^.+\.mediawiki.org$", re.IGNORECASE),
        path="/w/"
    )
]
