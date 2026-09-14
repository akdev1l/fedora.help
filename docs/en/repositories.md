# Third-Party Repositories

Almost everything on this site comes from a repository Fedora does not run.
This page sets those up once; the other pages assume you have been here first.

## What you are agreeing to

A third-party repository is outside Fedora's trust boundary. It has its own
maintainers, its own build system, and its own signing keys, and `dnf` runs its
package scriptlets as root exactly like a Fedora package. Enabling one is a
decision about who you trust to run code on your machine.

Two further consequences are worth knowing before you start:

- **Fedora does not support systems with these repos enabled.** Bug reports
  against Fedora packages that have been replaced by third-party versions will
  be closed.
- **Release upgrades get harder.** Release packages are versioned per Fedora
  release, and any swapped package has to resolve against the new one. An
  upgrade that would have been clean can stall on a third-party package that
  has not been rebuilt yet.

Both repositories below are widely used and well maintained. That is a
judgement about their track record and does not change the trust model.

## RPM Fusion

[RPM Fusion][rpmfusion] is a volunteer-run repository that packages what Fedora
will not. It is the de facto standard third-party repo for Fedora and what most
of this site assumes. It comes in three parts:

- **free** — open source software Fedora excludes for patent reasons.
  [The full FFmpeg](multimedia.md#swap-to-the-full-ffmpeg),
  `libavcodec-freeworld`, x264/x265, `mesa-va-drivers-freeworld`,
  [the restricted GStreamer plugins](multimedia.md#gstreamer-plugins).
- **nonfree** — redistributable but not open source.
  [The NVIDIA driver](nvidia/index.md),
  [Intel's full media driver](multimedia.md#intel), Steam.
- **tainted** — a separate opt-in repository for packages with a worse legal
  position still, notably `libdvdcss`. Not enabled by installing the other two.

### Enabling free and nonfree

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
[builds a kernel module](secure-boot.md):

```bash
sudo dnf upgrade --refresh
sudo systemctl reboot
```

### AppStream metadata

Since dnf5, the metadata that makes RPM Fusion packages show up in GNOME
Software and KDE Discover is not pulled in automatically:

```bash
sudo dnf install rpmfusion-free-appstream-data rpmfusion-nonfree-appstream-data
```

### Tainted

A deliberate second opt-in, needed for encrypted DVD playback:

```bash
sudo dnf install rpmfusion-free-release-tainted
```

What it holds is covered where it is used — see
[Multimedia and Codecs](multimedia.md#optional-extras) for `libdvdcss`.

### On atomic desktops

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

## negativo17

[negativo17][negativo17] is a personal repository maintained by Simone Caronni.
It overlaps RPM Fusion rather than complementing it: smaller split packages,
more built from source, closer adherence to Fedora packaging guidelines, and a
choice between akmods and DKMS for kernel modules. It is organised as several
separate repositories — [the NVIDIA one](nvidia/negativo17.md) is the one most
people want.

Enable the NVIDIA repository:

```bash
sudo dnf config-manager addrepo \
  --from-repofile=https://negativo17.org/repos/fedora-nvidia.repo
```

That defines `fedora-nvidia` pointing at
`https://negativo17.org/repos/nvidia/fedora-$releasever/$basearch/`, signed with
the repository's own GPG key.

## Do not mix them for the same software

The two package the same NVIDIA driver under different names with overlapping
file ownership, and dnf will install pieces of both without complaint. Pick one
route and stay on it — [NVIDIA Drivers](nvidia/index.md) compares them and has the
procedure for switching if you already have the wrong one installed.

Having both repositories enabled is fine in itself, as long as any given piece
of software comes from only one of them.

## COPR

[COPR][copr] is Fedora's build service. Anyone with a Fedora account can build
packages there, and the result is a repository you can enable in one command.
It runs on Fedora infrastructure, which is the source of most of the confusion
about it: the hosting is Fedora's, the packages are not. Nothing in COPR is
reviewed by Fedora, covered by Fedora QA, or shipped under Fedora's signing
keys. Each project signs with its own.

That makes a COPR project a narrower bet than RPM Fusion or negativo17. Those
are maintained repositories with a track record; a COPR project is usually one
person, and it can be abandoned or deleted without warning. `dnf` prints a
disclaimer to that effect the first time you enable one.

Enabling a project needs the `copr` command, in `dnf5-plugins`:

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

**Before enabling one**, open its page on COPR and check three things: when it
last built, which Fedora releases it builds for, and whether it follows Fedora
branching. A project that does not follow branching stops producing builds for
your release the moment you upgrade, and you are left holding packages that no
repository will update.

Check first whether the package is already in Fedora or RPM Fusion. COPR is
where you go when it is not.

One tool documented on this site,
[Fedora Tricks](tooling/fedoratricks.md), is distributed this way.

## Sources

- RPM Fusion, [repository configuration][rpmfusion-config] and
  [OSTree / atomic desktops][rpmfusion-ostree]
- [negativo17 repository documentation][negativo17]
- [COPR][copr], and Fedora's [COPR user documentation][copr-docs]

[rpmfusion]: https://rpmfusion.org/
[rpmfusion-config]: https://rpmfusion.org/Configuration
[rpmfusion-ostree]: https://rpmfusion.org/Howto/OSTree
[negativo17]: https://negativo17.org/
[copr]: https://copr.fedorainfracloud.org/
[copr-docs]: https://docs.pagure.org/copr.copr/user_documentation.html
