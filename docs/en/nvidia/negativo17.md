# The negativo17 Route

[negativo17](../repositories.md#negativo17) packages the same NVIDIA driver as RPM
Fusion, differently. [NVIDIA Drivers](index.md) documents the RPM Fusion route
and is the one to follow if you have no particular reason to be here. This page
covers the alternative, and how to move between the two.

The two are mutually exclusive. They ship packages with **overlapping file
ownership and different names**, so dnf will install pieces of both without
complaint and leave you with half a driver. negativo17's own documentation
opens its installation section by telling you to remove any RPM Fusion NVIDIA
packages first.

## Which one to use

| | RPM Fusion | negativo17 |
| --- | --- | --- |
| Package names | `xorg-x11-drv-nvidia*`, `akmod-nvidia` | `nvidia-driver*`, `akmod-nvidia`, `dkms-nvidia` |
| Kernel module | akmod (rebuilt locally) | akmod **or** DKMS, your choice |
| Branch on Fedora | production/current | short-lived branch |
| Version, Sept 2026 (F44) | 610.57.04 | 615.71.09 |
| Legacy branches | 580, 470, 390 packaged | none — current only |
| Secure Boot | signs automatically via akmods | akmods signing, or sign by hand |
| Packaging style | one large driver package plus subpackages | split into many small subpackages |

Both work. Neither is "correct".

Take RPM Fusion if you have an older card needing a legacy branch, if you run
[an atomic variant](index.md#atomic-variants-silverblue-kinoite), or if you
want the path with the most community troubleshooting behind it. Take
negativo17 if you want newer driver branches sooner, want DKMS instead of
akmods, or want the finer-grained package split — CUDA libraries without the
display driver, for instance.

negativo17 packages only the current branch. If your card needs 580, 470 or
390, this route is not available to you — see
[Identify your GPU and pick a branch](index.md#identify-your-gpu-and-pick-a-branch).

## Install

Sort out [Secure Boot](../secure-boot.md) first, the same as on
[the RPM Fusion route](index.md#secure-boot-do-this-before-you-install-anything).
Enable the `fedora-nvidia` repository as described in
[Third-Party Repositories](../repositories.md#negativo17), then install with
akmods:

```bash
sudo dnf5 install nvidia-driver akmod-nvidia nvidia-settings
```

Or with DKMS instead:

```bash
sudo dnf5 install nvidia-driver dkms-nvidia nvidia-settings
```

DKMS and akmods solve the same problem — rebuild an out-of-tree module when the
kernel changes — with different plumbing. DKMS hooks kernel package
installation and rebuilds inline; akmods runs as a systemd service. DKMS signs
its modules with its own per-system key at `/var/lib/dkms/mok.pub`, which you
enroll with `mokutil --import` the same way — see
[Secure Boot](../secure-boot.md#if-you-use-dkms-instead). akmods here uses the
same `/etc/pki/akmods` key as the RPM Fusion route.

CUDA and the rest are separate packages, which is the point of this repo:

```bash
# CUDA runtime for the driver, no display components
sudo dnf5 install nvidia-driver-cuda

# 32-bit libraries for Steam and Wine
sudo dnf5 install nvidia-driver-libs.i686
```

Wait for the module to build and verify it before rebooting — the same
`modinfo -F version nvidia` check, and the same reasons, as
[What akmods actually does](index.md#what-akmods-actually-does-and-why-you-must-wait).

> negativo17's own installation page tells you to
> [disable Secure Boot](../secure-boot.md#turning-it-off) rather
> than sign, and points at Red Hat's module-signing guide as the alternative.
> The akmods route above works here too, since the same `akmods` package builds
> and signs it.

## Open and proprietary kernel modules

negativo17's packaging lets you switch between
[the proprietary and open kernel module sources](index.md#open-vs-proprietary-kernel-module)
through `/etc/nvidia/kernel.conf`, rebuilding with `akmods --rebuild` or the
equivalent `dkms build` / `dkms install` pair. Its
documentation carries the exact commands; they reference driver versions in the
545 era, so treat the version strings there as examples rather than as current.

## Switching between the two

Do not layer one on the other. Remove the first completely, then install the
second.

**RPM Fusion → negativo17:**

```bash
sudo dnf5 remove 'xorg-x11-drv-nvidia*' 'akmod-nvidia*'
sudo dnf5 config-manager addrepo \
  --from-repofile=https://negativo17.org/repos/fedora-nvidia.repo
sudo dnf5 install nvidia-driver akmod-nvidia
```

**negativo17 → RPM Fusion:**

```bash
sudo dnf5 remove 'nvidia-driver*' 'dkms-nvidia*' 'akmod-nvidia*' 'nvidia-kmod-common'
sudo dnf5 config-manager setopt fedora-nvidia.enabled=0
sudo dnf5 install akmod-nvidia
```

> Do **not** use `dnf remove '*nvidia*'` for this, even though you will see it
> suggested. That glob matches `nvidia-gpu-firmware`, a Fedora package that
> nouveau and `nova_core` need in order to bring up your card at all. Removing
> it leaves you with no working driver of any kind.

Between the removal and the reinstall your machine has no NVIDIA driver. Run
the whole sequence in one sitting, and verify with `modinfo` before rebooting.
If something goes wrong partway, you can still boot — the removal
[strips the nouveau blacklist from your kernel arguments](index.md#what-the-package-changed-on-your-machine).

## How do I tell which one is installed?

```bash
dnf5 repoquery --installed '*nvidia*' --queryformat '%{name} %{from_repo}\n'
```

If packages come from more than one of `rpmfusion-nonfree*` and
`fedora-nvidia`, start over from a clean removal using the sequence above.

## Sources

- [negativo17][negativo17], the repository's own documentation
- RPM Fusion, [NVIDIA HowTo][rpmfusion-nvidia]

[negativo17]: https://negativo17.org/
[rpmfusion-nvidia]: https://rpmfusion.org/Howto/NVIDIA
