# NVIDIA Drivers

Fedora does not ship NVIDIA's driver, so on a fresh install your card runs on
the open stack. For a lot of people that is fine. For gaming, CUDA, NVENC, or
any card newer than the open driver has caught up with, it is not.

This page covers the RPM Fusion packaging, the route most Fedora documentation
and most community troubleshooting assumes.

Everything below was checked against RPM Fusion, NVIDIA and Fedora sources in
**September 2026**, targeting **Fedora 43 and 44**. Driver branch
numbers and legacy cut-offs move. Where a number matters, this page also tells
you how to check it yourself rather than trusting the number.

## What you get without it

Fedora's kernel ships `nouveau`, the reverse-engineered NVIDIA kernel driver,
and — since the Fedora 44 kernel — `nova_core`, the Rust-based successor that
is being built to replace it for GSP-based GPUs. Userspace comes from Mesa:
OpenGL, plus [**NVK**][nvk], Mesa's Vulkan driver for NVIDIA hardware. NVK is a
conformant Vulkan 1.4 implementation covering Kepler (GeForce 600/700) through
Ada (RTX 40) and consumer Blackwell (RTX 50), and since Mesa 25.1 Turing and
newer cards use NVK plus Zink for OpenGL by default.

That stack displays a desktop, plays video, and runs a browser on essentially
any NVIDIA card. What it does not do:

- **Clock the GPU up.** This is the big one. Nouveau [cannot reclock][nouveau-pm]
  Maxwell or
  Pascal GPUs at all — a GTX 1080 runs at its boot clocks, which is a fraction
  of its real performance. Turing and later fare better because the GSP
  firmware handles power management. Kepler reclocking is partial.
- **CUDA, NVENC, or NVDEC.** There is no open implementation. If you need
  hardware encode, video transcoding, or anything that links `libcuda`, you
  need the proprietary driver.
- **Some newest-generation hardware.** Open support lands after release, not
  with it.

The driver is absent because NVIDIA ships it under a licence that forbids the
redistribution Fedora requires — the same reason the codecs are missing. See
the [landing page][index] for the general shape of that.

## Do you need it?

Install it if you want serious 3D performance, CUDA or OpenCL compute, NVENC
encoding, or you have a card too new for Mesa. Do not install it if the machine
is a laptop where you mostly care about battery life, if your card is old
enough that no supported branch covers it, or if the desktop already works and
you have no complaint — the proprietary driver adds an out-of-tree kernel
module that has to be rebuilt on every kernel update, and that is a standing
maintenance cost.

The costs, stated once: the driver is non-free, it is not auditable, it is
built and distributed outside Fedora's trust boundary by a third party, and it
loads as an unsigned kernel module unless you sign it yourself.

## Identify your GPU and pick a branch

NVIDIA splits its driver into a current branch and several frozen legacy
branches. Installing the wrong one gets you a driver that loads and then
refuses to drive your card.

Find the card:

```bash
# Every display-class device, with numeric PCI IDs
lspci -nn | grep -E 'VGA|3D|Display'
```

The `[10de:xxxx]` at the end is the vendor:device PCI ID. `10de` is NVIDIA. If
your NVIDIA card shows up as `3D controller` rather than `VGA compatible
controller`, it is a hybrid-graphics laptop — see
[Hybrid graphics](#hybrid-graphics-optimus-laptops).

Map the card to a branch against NVIDIA's [Unix driver listing][nvidia-unix]. As
of September 2026:

| Architecture | Cards | Branch |
| --- | --- | --- |
| Turing and newer | GTX 16, RTX 20/30/40/50 | current (610 on F44, 580 on F43) |
| Maxwell, Pascal, Volta | GTX 745/750/750 Ti, GTX 900, GTX 10, TITAN V | 580 |
| Kepler | GeForce 600/700 incl. GTX 780 Ti | 470 |
| Fermi | GeForce 400/500 | 390 |
| Tesla and older | GeForce 8/9/200/300 and below | none — nouveau only |

Two traps in that table:

**Laptop part numbers straddle architectures.** The GTX 860M, 920, and much of
the 800M/900M line exist as both Kepler and Maxwell silicon under the same
marketing name. The PCI ID is the only reliable discriminator. Paste yours into
NVIDIA's [supported chips list][chips] for the current driver — if it is in the
"Current NVIDIA GPUs" table you want the current branch, and if it appears
further down under "The 580.xx driver supports the following set of GPUs" you
want that legacy branch instead.

**"Current" depends on your Fedora release.** On Fedora 43 the current branch
*is* 580, so Maxwell and Pascal cards use the plain package. On Fedora 44 the
current branch moved to 610 and 580 became a separate legacy package. The 580
branch is the last to support Maxwell, Pascal and Volta at all; NVIDIA has said
it will get kernel-compatibility fixes but no new features.

Below Fermi there is nothing. The 340 branch that covered GeForce 8/9/200/300
is not packaged for Fedora 43 or 44 by RPM Fusion. Those cards run nouveau or
they do not run.

Rather than trusting the table, ask your own system what exists:

```bash
dnf5 list --available 'akmod-nvidia*'
```

## Packaging

This page documents the RPM Fusion packaging, which is what most Fedora
documentation and most community troubleshooting assumes.

A second repository, negativo17, packages the same driver under different names
with overlapping file ownership. The two cannot be mixed. If you want newer
driver branches sooner, DKMS instead of akmods, or CUDA libraries without the
display driver, see [The negativo17 Route](nvidia-negativo17.md) — it compares
the two and carries the procedure for switching.

## Secure Boot: do this before you install anything

This is the most common way this install goes wrong. With Secure Boot on and
the module unsigned, the kernel refuses to load it and nothing in the
installation output says so.

```bash
mokutil --sb-state
```

If that says `SecureBoot enabled`, work through [Secure Boot](secure-boot.md)
before installing the driver.

## Installing the driver

### Enable the nonfree repository

The driver is in RPM Fusion's **nonfree** repository. Enable `free` and
`nonfree`, then update and reboot, as described in
[Third-Party Repositories](repositories.md#rpm-fusion).

The reboot matters here. Install the driver against a kernel you are not
running and the akmod system will cope, but you have made your own debugging
harder.

### Install

Current branch — Turing and newer:

```bash
sudo dnf5 install akmod-nvidia
```

Legacy branches, if your card needs one:

```bash
# Maxwell / Pascal / Volta, on Fedora 44
sudo dnf5 install akmod-nvidia-580xx xorg-x11-drv-nvidia-580xx

# Kepler
sudo dnf5 install akmod-nvidia-470xx xorg-x11-drv-nvidia-470xx

# Fermi
sudo dnf5 install akmod-nvidia-390xx xorg-x11-drv-nvidia-390xx
```

For CUDA, OpenCL, NVENC and NVDEC, add the CUDA subpackage — this is what
`nvidia-smi`, ffmpeg hardware encoding, and anything linking `libcuda` need:

```bash
sudo dnf5 install xorg-x11-drv-nvidia-cuda
```

Legacy branches have their own, capped at the last CUDA version that branch
supported: `xorg-x11-drv-nvidia-580xx-cuda`, `-470xx-cuda`, `-390xx-cuda`.

For VA-API video decode through NVIDIA's decoder, see
[Multimedia and Codecs](multimedia.md#nvidia) — the bridge package needs
environment variables that page documents.

### What akmods actually does, and why you must wait

`akmod-nvidia` does not contain a kernel module. It contains the *source* for
one, and depends on a compiler toolchain. The `akmods` service builds a real
kmod RPM against your running kernel and installs it locally. Two systemd units
drive this:

- `akmods.service` runs at boot and builds anything missing.
- `akmods@<kernel>.service` runs immediately after a kernel RPM transaction, so
  the module for a newly installed kernel is normally built before you reboot.

This means the dnf transaction finishing is **not** the install finishing. The
build runs afterwards and takes up to five minutes on a slow machine.

> Rebooting before the build completes is the second most common way to land at
> a black screen. Wait, and verify.

Verify:

```bash
modinfo -F version nvidia
```

A version number — `610.57.04` or similar — means the module exists and the
kernel can find it. `modinfo: ERROR: Module nvidia not found` means it does
not, and rebooting now will drop you to nouveau or to nothing.

To check a kernel you are not currently running:

```bash
modinfo -F version nvidia -k 6.19.14-300.fc44.x86_64
```

If it has not appeared, look at the build:

```bash
systemctl status akmods.service
ls -l /var/cache/akmods/nvidia/
```

Successful builds leave `<version>-for-<kernel>.log`. Failures leave
`<version>-for-<kernel>.failed.log`, and the tail of that file is the compiler
error. Force a retry with:

```bash
sudo akmods --force --kernels $(uname -r)
```

### What the package changed on your machine

Installing `xorg-x11-drv-nvidia` runs `grubby` against all your boot entries to
add `rd.driver.blacklist=nouveau,nova_core modprobe.blacklist=nouveau,nova_core`
and to strip any `nomodeset`. Inspect what you ended up with:

```bash
cat /proc/cmdline
```

The package also installs `nvidia-fallback.service`, which fires when nouveau is
blacklisted but `/sys/module/nvidia` does not exist — it loads nouveau anyway
and prints *"NVIDIA kernel module missing. Falling back to nouveau"* on the
Plymouth splash. If you see that message, you have a working desktop and a
broken driver: go back to `modinfo` above.

Uninstalling removes those kernel arguments again, so a clean removal does not
leave you with nouveau blacklisted and nothing to replace it.

Finally, the NVIDIA modules are deliberately kept **out** of the initramfs.
Early boot is handled by `simpledrm` using the firmware's mode. That is why you
do not need to rebuild the initramfs after driver updates.

### Open vs proprietary kernel module

NVIDIA ships two kernel-space implementations: the proprietary one and an
open-source (MIT/GPL) one. Userspace stays proprietary either way. Recent RPM
Fusion packages ship both sources and pick between them at build time based on
your GPU's PCI ID, so the default is normally right and there is nothing to do.

An `akmod-nvidia-open` package exists in RPM Fusion's `tainted` repository for
people who need to patch the open kernel module themselves. It is deliberately
kept out of the default repositories; if you are not modifying the module
source, you do not want it.

### Keep dnf from removing it

akmods packaging lets `dnf autoremove` decide `akmod-nvidia` is an unneeded
leaf and take it, along with the toolchain it depends on. Mark it as
user-installed:

```bash
sudo dnf5 mark user akmod-nvidia
```

## Hybrid graphics (Optimus laptops)

On a laptop with Intel or AMD integrated graphics plus an NVIDIA chip, the
NVIDIA GPU generally has no display wired directly to it — the internal panel
hangs off the iGPU. The NVIDIA card renders, the iGPU displays. That is PRIME
render offload, and on Fedora it is configured automatically by the driver
packages. There is nothing to set up.

To send one application to the NVIDIA GPU:

```bash
# Vulkan applications
__NV_PRIME_RENDER_OFFLOAD=1 vkcube

# GLX applications on Xwayland also need GLVND pointed at the NVIDIA driver
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia glxinfo | grep vendor
```

`__NV_PRIME_RENDER_OFFLOAD` does the work: it loads NVIDIA's Vulkan layer and
applies to GLX and EGL clients as well. `__GLX_VENDOR_LIBRARY_NAME` governs
GLX vendor selection alone, so it matters for applications running through
Xwayland and is ignored by a native Wayland application drawing through EGL.
Setting both is harmless.

That pair of variables is the whole of the `nvidia-offload` wrapper scripts you
will see on other distributions. If you want one, it is two lines:

```bash
printf '#!/bin/sh\nexport __NV_PRIME_RENDER_OFFLOAD=1\nexport __GLX_VENDOR_LIBRARY_NAME=nvidia\nexec "$@"\n' \
  | sudo tee /usr/local/bin/nvidia-offload >/dev/null
sudo chmod +x /usr/local/bin/nvidia-offload
```

Then `nvidia-offload steam`, and so on. GNOME's application menu also offers
"Launch using Discrete Graphics Card" for desktop-file launches.

Two finer controls, both from NVIDIA's PRIME documentation as summarised in
[RPM Fusion's Optimus notes][rpmfusion-optimus]:
`__VK_LAYER_NV_optimus=NVIDIA_only` restricts the GPU list a Vulkan application
sees, and `__NV_PRIME_RENDER_OFFLOAD_PROVIDER=NVIDIA-G0` picks one GPU on a
machine with several. The name it takes is an X RandR provider name, and
`xrandr --listproviders` is what prints those names — an X11 client, so it
reports what the X server it is talking to exposes rather than what the machine
holds. For the machine's own inventory of GPUs and bound drivers, use
`sudo lspci -nnk`.

### Power management

The honest position: with the proprietary driver loaded, an Optimus laptop uses
more power than the same laptop on the open stack, because the open stack can
power the discrete GPU down entirely and the proprietary driver's dynamic power
management is less complete. Where the firmware allows it, disabling Optimus is
the reliable way out of that trade.

Dynamic power management can be opted into:

```bash
sudo tee /etc/modprobe.d/nvidia-dpm.conf >/dev/null <<'EOF'
options nvidia NVreg_DynamicPowerManagement=0x02
EOF
```

`0x02` is the most aggressive setting — the GPU powers down when idle. Reboot
for it to take effect. If you see hangs on wake, remove the file.

### External monitors

On some laptops the HDMI or DisplayPort outputs are wired to the NVIDIA GPU
rather than the iGPU. A dead external monitor there is a question of which GPU
owns the port. Confirm what is present and what is bound to it first:

```bash
sudo lspci -nnk
```

Output routing across two GPUs is then the compositor's decision, and the
behaviour varies between GNOME, KDE and driver versions. The fix RPM Fusion
documents for this — a configuration file that marks the discrete GPU primary —
applies to Xorg sessions and has no Wayland counterpart, so there is no single
configuration change worth reproducing here. Check your compositor's and the
driver's current release notes for the version you are on.

Where the firmware offers the setting, disabling Optimus routes the outputs
through the NVIDIA GPU permanently. That keeps the discrete GPU powered at all
times, so battery life drops.

## Living with kernel updates

Every Fedora kernel update invalidates your NVIDIA module. A module built for
6.19.14 will not load on 6.20.1. The akmod or DKMS machinery exists to rebuild
it, and nearly always does so during the kernel's own dnf transaction.

It fails when the build fails: a kernel too new for the driver branch, a missing
`kernel-devel`, a compiler change, out-of-disk. You find out at the next reboot.

**Before rebooting after any kernel update**, when you care about the machine:

```bash
sudo dnf5 upgrade
modinfo -F version nvidia -k $(rpm -q --last kernel | head -1 | sed 's/^kernel-//;s/ .*//')
```

If that prints a version, you are safe to reboot.

### Recovering from a black screen

You have not lost anything. Work through these in order.

**1. Get a text console.** From the black screen, try Ctrl+Alt+F3. If you get a
login prompt, the kernel is fine and only graphics are broken — skip to step 4.

**2. Boot the previous kernel.** Hold Esc (or Shift on some systems) during
boot to get the GRUB menu, and pick the older kernel entry. Fedora keeps three
installed by default. The old kernel still has its working module, so this
normally gets you straight back to a desktop.

**3. Boot on nouveau instead.** At the GRUB menu, press `e` to edit the entry,
find the `linux` line, and delete
`rd.driver.blacklist=nouveau,nova_core modprobe.blacklist=nouveau,nova_core`.
Ctrl+X boots it. You get a slow but functional desktop with the NVIDIA packages
still installed. This is temporary — the change is not written to disk.

`nomodeset` on the same line is the more drastic version: it disables kernel
modesetting entirely and gives you an unaccelerated framebuffer. Use it only if
removing the blacklist is not enough.

**4. Rebuild the module.** From a TTY or a nouveau session:

```bash
sudo akmods --force --kernels $(uname -r)
modinfo -F version nvidia
```

If the build fails, read the reason:

```bash
sudo tail -50 /var/cache/akmods/nvidia/*.failed.log
```

A failure against a brand-new kernel usually means the driver branch has not
caught up. Staying on the older kernel until the driver updates is a legitimate
answer.

## Suspend and resume

Corrupted windows, a hung desktop, or a black screen after resume is usually
video memory not being preserved across the suspend. The fix is the power
management subpackage:

```bash
sudo dnf5 install xorg-x11-drv-nvidia-power
sudo systemctl enable nvidia-suspend.service nvidia-resume.service nvidia-hibernate.service
```

That package installs `/usr/lib/modprobe.d/nvidia-power-management.conf` with
the relevant options present but commented out. To turn them on, override it —
never edit files under `/usr/lib`:

```bash
sudo tee /etc/modprobe.d/nvidia-power-management.conf >/dev/null <<'EOF'
options nvidia NVreg_PreserveVideoMemoryAllocations=1
options nvidia NVreg_TemporaryFilePath=/var/tmp
EOF
```

The first preserves the full contents of video memory across suspend. The
second sends that dump to `/var/tmp` rather than `/tmp`, which on Fedora is
tmpfs — writing a GPU's worth of video memory into RAM defeats the purpose and
can fail outright. Reboot to apply.

## Atomic variants (Silverblue, Kinoite)

The outline matches the classic install. Every mechanical step differs.

Add RPM Fusion and reboot so the repositories exist — see
[Third-Party Repositories](repositories.md#on-atomic-desktops).

Layer the driver:

```bash
rpm-ostree install akmod-nvidia xorg-x11-drv-nvidia
# add xorg-x11-drv-nvidia-cuda too if you need nvidia-smi or CUDA
```

Set the kernel arguments by hand. On classic Fedora the RPM does this for you
with `grubby`; on ostree the package cannot modify the boot configuration, so
this step is yours:

```bash
rpm-ostree kargs \
  --append=rd.driver.blacklist=nouveau,nova_core \
  --append=modprobe.blacklist=nouveau,nova_core
```

Then reboot into the new deployment.

What differs from the classic workflow:

- **The module is built during the layering transaction, not at boot.**
  `akmods.service` refuses to run on an ostree system (its unit carries
  `ConditionPathExists=!/run/ostree-booted`). This is why `rpm-ostree install
  akmod-nvidia` takes several minutes.
- **Every kernel update means a new deployment**, with the module rebuilt as
  part of composing it. The upside is that a failed build gives you a failed
  deployment rather than a broken boot, and the previous deployment is still in
  the GRUB menu.
- **Major version upgrades need the release packages re-layered** in the same
  transaction as the rebase — see
  [Third-Party Repositories](repositories.md#on-atomic-desktops).
- **Secure Boot is genuinely awkward.** The signing key has to be available
  during the compose, which means packaging it rather than leaving it in
  `/etc` — see [Secure Boot](secure-boot.md#on-atomic-desktops).

### The prebuilt route

Universal Blue publishes Fedora Atomic images — Bazzite, Bluefin, Aurora — with
NVIDIA variants where the driver is already built into the image and signed
with the project's key. Nothing is layered and nothing is compiled on your
machine; kernel updates arrive as a new image with a matching module already in
it.

You still have to enroll their signing key once, which those images wrap in
`ujust enroll-secure-boot-key`. The password is set by the image rather than by
you — Bluefin documents `universalblue`, and community threads mention
`ublue-os` for other images. See [Secure Boot](secure-boot.md#on-atomic-desktops)
for the enrollment mechanics.

The trade is the usual one for prebuilt images: you get someone else's
integration testing and no local build step, and you give up control over which
driver branch and which packages you run.

## Removing it and going back to nouveau

```bash
sudo dnf5 remove 'xorg-x11-drv-nvidia*'
sudo systemctl reboot
```

RPM Fusion's uninstall scriptlet strips the nouveau blacklist from your kernel
arguments, so the machine comes back on nouveau. Confirm before rebooting:

```bash
cat /proc/cmdline    # should no longer mention rd.driver.blacklist=nouveau
```

If you installed from negativo17 instead, its removal sequence is on
[The negativo17 Route](nvidia-negativo17.md#switching-between-the-two).

> Again: not `dnf remove '*nvidia*'`. That takes `nvidia-gpu-firmware` with it,
> which nouveau and `nova_core` require.

After reboot, nothing NVIDIA should be loaded:

```bash
lsmod | grep -E 'nvidia|nouveau'
```

If you ever ran NVIDIA's own `.run` installer on this machine, it overwrote
distribution libraries outside of RPM's knowledge and a package removal will not
undo that. RPM Fusion documents a [recovery procedure][rpmfusion-nvidia] for
that case. Do not run it otherwise — it deletes system libraries.

## Troubleshooting

### Why is there a black screen after the first reboot?

Work through it in order. Was the module built (`modinfo -F version nvidia`
from a TTY or a rescue boot), is Secure Boot on (`mokutil --sb-state`), and was
the key enrolled (`sudo mokutil --test-key
/etc/pki/akmods/certs/public_key.der`).

A module that built fine but is refused at load time is almost always a
signature problem:

```bash
sudo dmesg | grep -iE 'nvidia|lockdown|module verification'
```

[Recovering from a black screen](#recovering-from-a-black-screen) has the full
sequence.

### What does "NVIDIA kernel module missing. Falling back to nouveau" mean?

`nvidia-fallback.service` doing its job. Your desktop works, the driver does
not. See [Recovering from a black screen](#recovering-from-a-black-screen) for
the rebuild.

### Why is the display stuck at 1024x768?

The NVIDIA driver is not in use. Either it fell back to nouveau, in which case
see the previous entry, or `nomodeset` is on the kernel command line:

```bash
cat /proc/cmdline
sudo grubby --update-kernel=ALL --remove-args='nomodeset'
```

### Why did the module stop loading after a kernel update?

The build failed or has not run. See
[Living with kernel updates](#living-with-kernel-updates). If the driver branch
does not support the new kernel yet, wait for the driver update rather than
forcing anything.

### Should I add `nvidia-drm.modeset=1` to the kernel command line?

No. RPM Fusion's module enables kernel modesetting by default, and RPM Fusion
warns against setting the parameter by hand — it interacts badly with the
Fedora kernel's `simpledrm` early-boot handling. Old forum posts and blog
articles still tell you to set it; they are describing a configuration from
several years ago.

Turning modesetting off is a debugging step, and reversible:

```bash
sudo grubby --update-kernel=ALL --args='nvidia-drm.modeset=0'
sudo grubby --update-kernel=ALL --remove-args='nvidia-drm.modeset=0'
```

### Why doesn't the LUKS passphrase prompt appear?

On full-disk encryption with the NVIDIA card as the only GPU, the prompt is
drawn before the driver initialises:

```bash
sudo grubby --update-kernel=ALL --args='plymouth.use-simpledrm=1'
```

### Why is the external monitor dead on my laptop?

Check first whether the port is wired to the NVIDIA GPU at all —
`sudo lspci -nnk` shows which GPU has which driver bound. Then see
[External monitors](#external-monitors).

### Why does suspend and resume break the display?

See [Suspend and resume](#suspend-and-resume). If it still fails with video
memory preservation enabled, check that `/var/tmp` has room for the dump.

### Why did `dnf autoremove` remove the driver?

It considers `akmod-nvidia` a leaf package:

```bash
sudo dnf5 mark user akmod-nvidia
```

Then reinstall.

### How do I report a bug?

NVIDIA and RPM Fusion both want the same log bundle:

```bash
sudo nvidia-bug-report.sh
```

[index]: index.md
[rpmfusion-nvidia]: https://rpmfusion.org/Howto/NVIDIA
[rpmfusion-optimus]: https://rpmfusion.org/Howto/Optimus
[chips]: https://download.nvidia.com/XFree86/Linux-x86_64/615.71.09/README/supportedchips.html
[nvidia-unix]: https://www.nvidia.com/en-us/drivers/unix/
[nvk]: https://docs.mesa3d.org/drivers/nvk.html
[nouveau-pm]: https://nouveau.freedesktop.org/PowerManagement.html
