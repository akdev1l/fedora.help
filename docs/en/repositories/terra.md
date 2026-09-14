# Terra

[Terra][terra] is a community repository for Fedora run by [Fyra Labs][fyra],
the team behind Ultramarine Linux. It carries roughly three thousand packages
Fedora does not ship, and it is rolling: packages track upstream releases
rather than being frozen for the life of a Fedora release.

## Why it exists

Fedora's packaging process is deliberately slow. A package needs a review, a
sponsor, and a maintainer willing to keep it building for years, and stable
releases hold versions still. That is the right trade for a distribution and
the wrong one for software that moves weekly.

Terra takes the opposite position. Updates are automated from upstream through
its own tooling, the whole package set lives in one public repository, and
every build runs in public CI. Its maintainers are explicit that this is the
difference they care about: they call
[RPM Fusion](rpmfusion.md) "a great repository" and say what Terra adds is
transparency and a rolling model, rather than a different legal position.

In practice it is where you look for desktop software that is young, moves
fast, or nobody has packaged for Fedora — terminal emulators, editors, shell
tooling, Wayland compositors and the like. `ghostty`, `zed`, `zen-browser`,
`cursor`, `starship`, `zellij`, `lact` and `topgrade` are all there.

## Who maintains it

Fyra Labs, a company rather than a volunteer group, which is unusual among the
repositories on this page. Packaging is open to contributors through the
`terrapkg` organisation on GitHub, and submissions are vetted, but the
infrastructure is not community-run: Terra states that only trusted Fyra Labs
employees hold access to the build systems and the signing keys.

The build chain is its own work rather than Fedora's. Packages are built with
**Andaman**, a Rust build toolchain that drives Mock and `rpmbuild`; delivered
by **Subatomic**, which generates the repository metadata; and located through
**Tetsudou**, a metalink generator that points `dnf` at a mirror. Specs and
update scripts live in a monorepo, and GitHub Actions builds on push.

Six downstream distributions use it, among them Ultramarine, Bazzite and
Nobara — so a Bazzite system already has Terra whether or not its user went
looking for it.

## Enabling it

```bash
sudo dnf install --nogpgcheck --repofrompath 'terra,https://repos.fyralabs.com/terra$releasever' terra-release terra-gpg-keys
```

`--nogpgcheck` applies to that one transaction, which is how the signing key
gets onto the system in the first place: `terra-gpg-keys` carries it, and
everything afterwards is checked against it.

Terra publishes for Fedora 42 through 45.

### On atomic desktops

```bash
curl -fsSL https://raw.githubusercontent.com/terrapkg/packages/f$(rpm --eval '%{fedora}')/anda/terra/release/terra.repo | pkexec tee /etc/yum.repos.d/terra.repo
rpm-ostree install terra-release terra-gpg-keys
```

On secureblue, `run0` replaces `pkexec`.

### Optional sub-repositories

The base repository is deliberately conservative. Four more are shipped as
separate packages, each enabling a channel of its own:

```bash
sudo dnf install terra-release-extras
sudo dnf install terra-release-mesa
sudo dnf install terra-release-nvidia
sudo dnf install terra-release-multimedia
```

`terra-release-multimedia` needs Fedora 43 or newer.

## Overlap with RPM Fusion

The `mesa`, `nvidia` and `multimedia` channels cover the same ground as
[RPM Fusion](rpmfusion.md), and the same warning applies as for
[negativo17](negativo17.md): a graphics driver or a media stack should come
from one repository, not from two competing for the same file names. The base
Terra repository does not overlap, so enabling it alongside RPM Fusion is
fine — the sub-repositories are where you have to choose.

## Sources

- [Terra][terra] and its [documentation][terra-docs], including the
  [infrastructure overview][terra-infra] and the [FAQ][terra-faq]
- The enable commands are quoted from Terra's own
  [installation instructions][terra-install]
- Package names and the Fedora releases published were checked against
  `https://repos.fyralabs.com/terra44` in September 2026

[terra]: https://terrapkg.com/
[terra-docs]: https://docs.terrapkg.com/
[terra-infra]: https://docs.terrapkg.com/general/infrastructure
[terra-faq]: https://docs.terrapkg.com/general/faq
[terra-install]: https://docs.terrapkg.com/usage/installing
[fyra]: https://fyralabs.com/
