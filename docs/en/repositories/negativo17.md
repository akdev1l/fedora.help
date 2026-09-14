# negativo17

[negativo17][negativo17] is a personal repository. It overlaps RPM Fusion
rather than complementing it: smaller split packages, more built from source,
closer adherence to Fedora packaging guidelines, and a choice between akmods
and DKMS for kernel modules. It is organised as several separate repositories —
[the NVIDIA one](../nvidia/negativo17.md) is the one most people want.

## Why it exists

The split packaging is the point. RPM Fusion ships the NVIDIA driver as one
large package with subpackages hanging off it; negativo17 breaks it into
smaller pieces, so you can install the CUDA libraries without the display
driver, or the 32-bit libraries on their own. It also tracks NVIDIA's
short-lived branch rather than the production one, which puts it a branch ahead
of RPM Fusion much of the time.

The trade for that is narrower coverage. negativo17 packages only the current
driver branch, so an older card needing 580, 470 or 390 has to use RPM Fusion.

## Who maintains it

Simone Caronni, a Fedora packager based in Zurich who maintains Fedora's Steam
package, among others. He has worked with Fedora developers on getting the
proprietary NVIDIA driver to coexist with the Mesa stack through glvnd, which
is the problem the repository was built around.

This is one person's infrastructure rather than a group project with a
sponsorship process, which is the main structural difference from
[RPM Fusion](rpmfusion.md). It has a long track record, and that is a judgement
about the maintainer, not a change to
[the trust model](index.md#what-you-are-agreeing-to).

## Enabling the NVIDIA repository

```bash
sudo dnf config-manager addrepo \
  --from-repofile=https://negativo17.org/repos/fedora-nvidia.repo
```

That defines `fedora-nvidia` pointing at
`https://negativo17.org/repos/nvidia/fedora-$releasever/$basearch/`, signed with
the repository's own GPG key.

Enabling this repository alongside RPM Fusion is fine. Installing the NVIDIA
driver from both is not — see
[Do not mix them](index.md#do-not-mix-them-for-the-same-software).

## Sources

- [negativo17][negativo17], the repository's own documentation
- [The NVIDIA driver repository][negativo17-nvidia], for the packaging split

[negativo17]: https://negativo17.org/
[negativo17-nvidia]: https://negativo17.org/nvidia-driver/
