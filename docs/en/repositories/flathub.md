# Flathub

[Flathub][flathub] is where most Linux desktop applications are published as
Flatpaks. It sits outside the rest of this page's subject matter: a Flatpak
carries its own runtime and libraries, installs per-user or system-wide without
touching the host's packages, and runs sandboxed. Nothing on Flathub can
conflict with an RPM.

Fedora ships a Flathub remote already, but a filtered one, and the filter is
the reason most people end up here.

## Why it exists

Packaging a desktop application once per distribution, per release, is work
nobody wants to repeat. Flatpak lets an upstream ship one build that runs
everywhere, against a runtime it pins itself, so an application can use a newer
toolkit than the host carries. Flathub is the store that distributes those
builds.

For this site, it matters because it is the practical answer for a large part
of the proprietary desktop software Fedora cannot ship. Steam, Discord,
Spotify, Chrome and Zoom are all there. It is also how
[the multimedia guide](../multimedia/index.md#flatpak-apps) recommends handling
codecs on the [atomic desktops](../multimedia/atomic.md), where layering host
packages costs a reboot every time.

## Who maintains it

Flathub describes itself as a grassroots open source community rather than a
foundation-run project, with infrastructure donated by several sponsors.
Applications come from two places: upstream developers publishing their own
software, and volunteers packaging someone else's. The distinction is visible —
an app whose publisher has proved it controls the upstream project carries a
**verified** badge on its Flathub page.

That badge is about provenance, not review. Neither Flathub nor Fedora audits
what an application does once installed. The sandbox is what limits it, and an
application declares its own permissions, so a Flatpak that asks for the whole
filesystem gets it. Flathub shows those permissions on each app's page before
you install.

## What Fedora ships

Fedora preconfigures the `flathub` remote, filtered down to a short list. The
remote's own metadata gives it away:

```bash
flatpak remotes --columns=name,title
```

It reports **Fedora Flathub Selection**, not Flathub. The filter lives at
`/usr/share/flatpak/fedora-flathub.filter`, and it is deny-by-default with a
handful of allowances — the freedesktop runtimes, plus a short list of
applications: Bitwarden, Postman, Teams, Minecraft and Skype at the time of
writing. Everything else on Flathub is invisible to `flatpak search` and to
GNOME Software until the filter is gone.

The filter is maintained in the open, at
[pagure.io/fedora-flathub-filter][filter].

## Enabling the full repository

```bash
sudo flatpak remote-modify --no-filter flathub
```

That drops Fedora's filter and leaves the remote pointing where it already
pointed. GNOME Software offers the same thing as a "Third-Party Repositories"
toggle in its first-run screen and in its settings.

If the remote is missing altogether, add it:

```bash
flatpak remote-add --if-not-exists flathub \
  https://dl.flathub.org/repo/flathub.flatpakrepo
```

Then confirm what you have:

```bash
flatpak remotes --columns=name,title,filter
```

## The trust position

Flathub is a different shape of risk from the repositories above it. It does
not ship anything into `/usr`, it cannot replace a Fedora package, and removing
an application removes it completely. What you are trusting is each publisher
separately, and the sandbox to hold whatever that publisher shipped.

Per application, then: prefer verified publishers, read the permissions on the
Flathub page, and remember that a Flatpak asking for `filesystem=host` has
given up most of what the sandbox was for.

## Sources

- [Flathub][flathub], and its per-application permission listings
- [fedora-flathub-filter][filter], the filter Fedora ships
- The filter file on a Fedora install, `/usr/share/flatpak/fedora-flathub.filter`

[flathub]: https://flathub.org/
[filter]: https://pagure.io/fedora-flathub-filter
