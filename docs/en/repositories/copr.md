# COPR

[COPR][copr] is Fedora's build service. Anyone with a Fedora account can build
packages there, and the result is a repository you can enable in one command.

## Why it exists

It lowers the cost of publishing an RPM to almost nothing. Getting a package
into Fedora proper means a review, a sponsor and an ongoing commitment; COPR
asks for none of that, so it is where nightly builds, personal backports,
patched forks and software nobody intends to maintain long-term end up.

That openness is also the catch. It runs on Fedora infrastructure, which is the
source of most of the confusion about it: the hosting is Fedora's, the packages
are not. Nothing in COPR is reviewed by Fedora, covered by Fedora QA, or
shipped under Fedora's signing keys. Each project signs with its own.

## Who maintains it

The Fedora Project runs the service. Each project is maintained by whoever
created it, under no common policy — the reason the table on
[Third-Party Repositories](index.md) lists the owner rather than the service as
the party you are trusting.

That makes a COPR project a narrower bet than
[RPM Fusion](rpmfusion.md) or [negativo17](negativo17.md). Those are
maintained repositories with a track record; a COPR project is usually one
person, and it can be abandoned or deleted without warning. `dnf` prints a
disclaimer to that effect the first time you enable one.

## Enabling a project

The `copr` command is in `dnf5-plugins`:

```bash
sudo dnf install dnf5-plugins
sudo dnf copr enable owner/project
```

See what you have enabled, and back one out:

```bash
dnf copr list
sudo dnf copr disable owner/project
```

`disable` leaves the repository configured but inactive. `sudo dnf copr remove
owner/project` deletes the configuration outright. Neither removes packages you
installed from it, which then sit on your system with nothing behind them.

## Before enabling one

Open its page on COPR and check three things: when it last built, which Fedora
releases it builds for, and whether it follows Fedora branching. A project that
does not follow branching stops producing builds for your release the moment
you upgrade, and you are left holding packages that no repository will update.

Check first whether the package is already in Fedora or
[RPM Fusion](rpmfusion.md). COPR is where you go when it is not.

## Notable projects

Projects documented elsewhere on this site. Confirmed in September 2026;
which Fedora releases each one builds for is on its COPR page.

| Project | What it provides | Maintainer | Follows branching |
| --- | --- | --- | --- |
| [`rhea/fedoratricks`][fedoratricks-copr] | [Fedora Tricks](../tooling/fedoratricks.md), a Bash tool that enables RPM Fusion, installs the multimedia stack and sets up the NVIDIA driver | Rhea Gustavsson. The COPR description states the package is provided by the Fedora Discord server to its members | Yes |

[Fedora Tricks](../tooling/fedoratricks.md) covers what the tool does and what
running it costs you.

## Sources

- [COPR][copr], and Fedora's [COPR user documentation][copr-docs]

[copr]: https://copr.fedorainfracloud.org/
[copr-docs]: https://docs.pagure.org/copr.copr/user_documentation.html
[fedoratricks-copr]: https://copr.fedorainfracloud.org/coprs/rhea/fedoratricks/
