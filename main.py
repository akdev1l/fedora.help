"""Macros for mkdocs-macros-plugin.

Keeps the site's identity defined in one place: `extra.brand` and `site_url`
in mkdocs.yml. Pages call `{{ brandlink() }}` rather than hardcoding either.
"""


def define_env(env):
    @env.macro
    def brandlink():
        """The site name as a styled link to its canonical URL."""
        brand = env.conf["extra"]["brand"]
        url = env.conf["site_url"]
        return f"[{brand}]({url}){{ .brand }}"
