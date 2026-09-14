# RPM Fusion

[RPM Fusion][rpmfusion] is the de facto standard third-party repository for
Fedora, and what most of this site assumes. It comes in three parts:

- **free** — open source software Fedora excludes for patent reasons.
  [The full FFmpeg](../multimedia.md#swap-to-the-full-ffmpeg),
  `libavcodec-freeworld`, x264/x265, `mesa-va-drivers-freeworld`,
  [the restricted GStreamer plugins](../multimedia.md#gstreamer-plugins).
- **nonfree** — redistributable but not open source.
  [The NVIDIA driver](../nvidia/index.md),
  [Intel's full media driver](../multimedia.md#intel), Steam.
- **tainted** — a separate opt-in repository for packages with a worse legal
  position still, notably `libdvdcss`. Not enabled by installing the other two.

## Why it exists

Fedora's exclusions have two different causes, and RPM Fusion's split mirrors
them. Some software is free and open source but covered by software patents, or
otherwise risky for Red Hat to distribute at scale from the United States;
that is what `free` holds. Other software is redistributable but not open
source, which puts it outside Fedora's licensing policy whatever the patent
position; that is `nonfree`. In both cases the code is legal to run and the
packaging is uncontroversial. Fedora's own guidelines are what keep it out.

## Who maintains it

A group of volunteers, most of whom are also active Fedora packagers. RPM
Fusion follows the Fedora packaging guidelines, and its sponsorship model runs
through Fedora's: only Fedora sponsors can sponsor a new RPM Fusion packager.
What differs is policy on what may be shipped, not who is doing the shipping or
how carefully.

The project dates to a merger. Three separate add-on repositories — Livna,
Dribble and Freshrpms — announced in November 2007 that they would combine, and
completed the merge in November 2008. Before that, a Fedora desktop needed
packages from several mutually inconsistent sources; consolidating them is the
reason a single third-party repository became the norm.

## Enabling free and nonfree

The release packages are per-Fedora-release. `$(rpm -E %fedora)` expands to the
running release number, so this is the same command RPM Fusion's own
[configuration page][rpmfusion-config] publishes and it needs no editing:

```bash
sudo dnf install \
  https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

Install both even if you only came for one of them. The NVIDIA driver is in
`nonfree`, the multimedia packages are mostly in `free`, and several `nonfree`
packages depend on `free`.

Then refresh and reboot before installing anything that
[builds a kernel module](../secure-boot.md):

```bash
sudo dnf upgrade --refresh
sudo systemctl reboot
```

## AppStream metadata

Since dnf5, the metadata that makes RPM Fusion packages show up in GNOME
Software and KDE Discover is not pulled in automatically:

```bash
sudo dnf install rpmfusion-free-appstream-data rpmfusion-nonfree-appstream-data
```

## Tainted

A deliberate second opt-in, needed for encrypted DVD playback:

```bash
sudo dnf install rpmfusion-free-release-tainted
```

What it holds is covered where it is used — see
[Multimedia and Codecs](../multimedia.md#optional-extras) for `libdvdcss`.

## On atomic desktops

Silverblue and Kinoite layer the release packages instead, and need a reboot
before the repositories are usable:

```bash
sudo rpm-ostree install \
  https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

At a major release upgrade the release packages have to be replaced in the same
transaction as the rebase, or the upgrade will not resolve. RPM Fusion
documents that as:

```bash
sudo rpm-ostree update \
  --uninstall rpmfusion-free-release --uninstall rpmfusion-nonfree-release \
  --install rpmfusion-free-release --install rpmfusion-nonfree-release
```

RPM Fusion documents the atomic case in full on its [OSTree page][rpmfusion-ostree].

## Sources

- RPM Fusion, [repository configuration][rpmfusion-config],
  [OSTree / atomic desktops][rpmfusion-ostree] and the
  [contributor documentation][rpmfusion-contributors]
- The merger dates are from the [Wikipedia article][rpmfusion-wikipedia], which
  cites the 2007 announcement and the 2008 completion

[rpmfusion]: https://rpmfusion.org/
[rpmfusion-config]: https://rpmfusion.org/Configuration
[rpmfusion-ostree]: https://rpmfusion.org/Howto/OSTree
[rpmfusion-contributors]: https://rpmfusion.org/Contributors
[rpmfusion-wikipedia]: https://en.wikipedia.org/wiki/RPM_Fusion
