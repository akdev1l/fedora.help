# fedora.help

Source for [fedora.help](https://fedora.help), an unofficial guide to the
software Fedora cannot ship: multimedia codecs, the NVIDIA driver, third-party
repositories, and the fixes a fresh install usually needs.

Built with [MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Building

Everything runs in a container, so the only requirement on the host is
[Podman](https://podman.io/).

```bash
./ci/builder-build.sh                                   # build the image, once
./ci/builder-exec.sh poetry install                     # install dependencies
./ci/builder-exec.sh python3 ci/mkdocs.py build --strict
```

To preview while editing, with live reload on http://localhost:8000:

```bash
./ci/builder-exec.sh python3 ci/mkdocs.py serve
```

`ci/mkdocs.py` forwards its arguments to `mkdocs` inside the project's Poetry
environment. Output goes to `site/`, which is not tracked.

Build with `--strict` before opening a pull request. It turns broken internal
links and other warnings into failures.

## Layout

```
docs/en/         English pages, one Markdown file each
docs/<locale>/   translations, mirroring the English tree
docs/stylesheets/extra.css   shared, outside the language folders
mkdocs.yml       nav, plugins, languages
main.py          macros available to pages
ci/              container definition and the mkdocs wrapper
```

`main.py` defines `brandlink()`, which renders the site name as a link built
from `site_url` and `extra.brand`. Pages call `{{ brandlink() }}` rather than
writing the name or the URL by hand.

## Writing

Guides state what a command does and what it costs before the reader runs it —
an unsigned kernel module, a non-free licence, a repository outside Fedora's
trust boundary.

Verify package names, commands and version numbers against the current Fedora
and RPM Fusion repositories rather than from memory. Where something could not
be verified, the page says so instead of guessing. Pages carry a `Sources`
section listing the upstream documentation they were checked against.

Cross-reference other pages instead of repeating them. Each fact has one home:
repository setup lives in `repositories.md`, module signing in
`secure-boot.md`.

The site is Wayland-only. It targets currently supported Fedora releases on
x86_64.

## Translations

Each language has its own folder under `docs/`, mirroring the English tree, so
the French landing page is `docs/fr/index.md`. Locales are configured in
`mkdocs.yml`, where the navigation labels are translated too. Assets shared
across languages, such as the stylesheet, sit outside the language folders.

Pages with no translation yet fall back to English at the translated URL, so a
language can be added one page at a time. Start with `index.md`.

Paths in `nav` are written without the language folder — `nvidia/index.md`, not
`en/nvidia/index.md`.

## Licence

Documentation under `docs/` is [CC BY-SA 4.0][cc]. The code — `main.py`, the
scripts in `ci/`, and the build configuration — is [GPL-3.0-or-later][gpl].
See [LICENSE](LICENSE).

## Not affiliated with the Fedora Project

This is an independent community project, not produced, endorsed, or reviewed
by the Fedora Project or Red Hat. "Fedora" is a trademark of Red Hat, Inc.

[cc]: LICENSES/CC-BY-SA-4.0.txt
[gpl]: LICENSES/GPL-3.0-or-later.txt
