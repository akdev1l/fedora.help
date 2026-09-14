# Third-Party Repositories

Almost everything on this site comes from a repository Fedora does not run.
Set those up once; the other pages assume you have been here first.

| Repository | What it holds | Who runs it | Page |
| --- | --- | --- | --- |
| RPM Fusion | The patent-encumbered and non-free packages Fedora excludes: the full FFmpeg, the restricted GStreamer plugins, the NVIDIA driver, Steam | A volunteer group, most of them Fedora packagers | [RPM Fusion](rpmfusion.md) |
| negativo17 | The same NVIDIA driver as RPM Fusion, packaged differently, plus CUDA and other hardware-adjacent software | Simone Caronni, a Fedora packager, on his own infrastructure | [negativo17](negativo17.md) |
| COPR | Whatever an individual chose to build. One project per owner, no common policy | The builder of each project. Fedora runs the service, not the content | [COPR](copr.md) |

Most people need RPM Fusion and nothing else. negativo17 is an alternative for
the NVIDIA driver, and the two cannot be mixed for it. COPR is where you go for
a package that exists in neither.

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

RPM Fusion and negativo17 are both widely used and well maintained. That is a
judgement about their track record and does not change the trust model.

## Do not mix them for the same software

RPM Fusion and negativo17 package the same NVIDIA driver under different names
with overlapping file ownership, and dnf will install pieces of both without
complaint. Pick one route and stay on it — [NVIDIA Drivers](../nvidia/index.md)
compares them and has the procedure for switching if you already have the wrong
one installed.

Having both repositories enabled is fine in itself, as long as any given piece
of software comes from only one of them.
