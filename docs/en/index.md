# {{ brand }}: Make Fedora Yours

{{ brandlink() }} is an unofficial, community-run guide to the software Fedora
can't ship: [multimedia codecs](multimedia.md),
[the NVIDIA driver](nvidia/index.md), third-party repos like
[RPM Fusion](repositories/rpmfusion.md) and Flathub, and the closed-source
apps most desktops end up wanting. Plus the fixes a fresh install usually
needs.

## Why this site exists

Fedora ships only free and open source software, per the [Fedora Project
mission][mission]. Red Hat's legal position also rules out patent-encumbered
and redistribution-restricted code. So a number of things desktop users expect
can't live inside Fedora:

- Patented multimedia codecs (H.264, HEVC, AAC and friends)
- NVIDIA's proprietary driver
- Proprietary firmware and hardware enablement blobs
- Closed-source applications: Steam, Discord, Chrome, Spotify

That's out of scope for the project, so the documentation has to live elsewhere.

## Target Audience

Desktop Fedora users who want the proprietary pieces working, and who want to
understand what they installed once it is.

The guides assume a reader who:

- can open a terminal and work at a shell prompt
- is unafraid to run commands, including as root
- reads a command before pasting it
- wants to build up their own Fedora knowledge along the way

They target current, supported Fedora releases on x86_64 — Workstation and the
desktop spins. Atomic variants (Silverblue, Kinoite) are called out where the
steps differ.

None of this is required. A stock Fedora install is complete and supported as
shipped; every page here steps outside it.

## Not affiliated with the Fedora Project

{{ brandlink() }} is an independent community project. It is not produced, endorsed,
or reviewed by the Fedora Project or Red Hat, and "Fedora" is a trademark of
Red Hat, Inc. For official documentation, see [docs.fedoraproject.org][docs].

[mission]: https://docs.fedoraproject.org/en-US/project/
[docs]: https://docs.fedoraproject.org/
