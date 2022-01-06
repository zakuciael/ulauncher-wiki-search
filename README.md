<!--suppress HtmlDeprecatedAttribute -->
<h1 align="center">
  <a href="https://github.com/zakuciael/ulauncher-wiki-search">
    <img alt="Ulauncher Wiki Search" src="https://raw.githubusercontent.com/zakuciael/ulauncher-wiki-search/main/.github/logo.svg?sanitize=true" width="130">
  </a>
	<br>
  Ulauncher Wiki Search
</h1>

<h6 align="center">Overview</h6>
<h4 align="center">
<a href="https://ulauncher.io/" target="_blank">Ulauncher</a> extension that lets you search and
open <a href="https://www.mediawiki.org/wiki/MediaWiki" target="_blank">MediaWiki</a> pages
</h4>

<p align="center">
  <a href="https://github.com/zakuciael/ulauncher-wiki-search">
    <img src="https://img.shields.io/badge/Ulauncher-Extension-green.svg"
      alt="Ulauncher Extension" />
  </a>
  <a href="https://github.com/zakuciael/ulauncher-wiki-search/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/zakuciael/ulauncher-wiki-search.svg"
      alt="License" />
  </a>
</p>

## Install

### Requirements

#### Programs

- Ulauncher 5
- Python 3

#### Packages

- validators >= 0.18.2
- beautifulsoup4 >= 4.10.0
- requests >= 2.27.1
- dotmap >= 1.3.26

To install this extension:

1. Install required packages
2. Open `Preferences` window
3. Select `Extensions` tab
4. Click `Add extension` button on the sidebar
5. Paste the following url: `https://github.com/zakuciael/ulauncher-wiki-search`

## Usage

1. Open `Preferences` window
2. Select `Extensions` tab
3. Click on `Wiki Search` extension
4. Set the `Wiki URLs` value to the list of wiki URLs separated by the `|` sign

### URL specification

The URL can be either a **hostname** (e.g. `en.wikipedia.org`) or a **full url** (
e.g. `https://en.wikipedia.org/`) and the API endpoint of the wiki needs to be located at one of
those locations `/api.php`, `/w/api.php` or `/wiki/api.php`

## Contributing

Clone this repository and run:

```bash
make link
```

The `make link` command will symlink the project into the ulauncher extensions folder.

To see your changes, stop ulauncher and run it from the command line with: `make dev`.

The output will display something like this:

```
2020-11-15 10:24:16,869 | WARNING | ulauncher.api.server.ExtensionRunner: _run_process() | VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:5054/com.github.zakuciael.ulauncher-wiki-search PYTHONPATH=/usr/lib/python3.10/site-packages /usr/bin/python3 /home/zakku/.local/share/ulauncher/extensions/com.github.zakuciael.ulauncher-wiki-search/main.py
```

In another terminal run `make PORT=<PORT> start` command to run the extension backend.
> Note: The ``<PORT>`` variable refers to the port number found in the ``ULAUNCHER_WS_API`` env located in the above log.

To see your changes, CTRL+C the previous command and run it again to refresh.

## License

MIT © [Krzysztof Saczuk \<zakku@zakku.eu\>](https://github.com/zakuciael)