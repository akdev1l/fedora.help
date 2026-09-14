"""Copy the _redirects rules into the build output.

MkDocs skips files whose names start with an underscore, so `_redirects`
cannot live in `docs/`. Keep it at the repository root and copy it in once
the site is built.
"""

from logging import getLogger
from pathlib import Path
from shutil import copyfile

log = getLogger(f"mkdocs.hooks.{__name__}")

SOURCE = Path(__file__).parent.parent.parent / "_redirects"


def on_post_build(config, **kwargs):
    if not SOURCE.is_file():
        log.warning("no _redirects file at %s, nothing copied", SOURCE)
        return

    destination = Path(config["site_dir"]) / SOURCE.name
    copyfile(SOURCE, destination)
    log.info("copied %s to %s", SOURCE.name, destination)
