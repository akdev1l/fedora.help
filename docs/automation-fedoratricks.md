# Fedora Tricks

The project spells its own name `fedoratricks`, which is also the command and
the package name.

| | |
| --- | --- |
| Home | [github.com/RheaAyase/fedoratricks][fedoratricks] |
| Maintainer | Rhea Gustavsson, with three other contributors |
| Form | Bash, run from a terminal — no TUI, no GUI |
| Distribution | RPM from the [rhea/fedoratricks COPR][fedoratricks-copr] |
| Licence | MIT |
| Version described here | 0.3-1, released 16 July 2026 |
| Builds for | Fedora 43, 44, 45 and Rawhide, x86_64 and aarch64 |

## What it is

`fedoratricks` is a set of Bash modules behind a single command. It came out of
the Fedora Discord server — the COPR's own description says the package is
"provided by the Fedora Discord server to its members to help with 'support'
issues" — and its stated aim is to explain each step while it performs it. It
prints every command it runs before running it.

Development started in June 2026 and the three tagged releases landed over six
weeks. As of September 2026 the last commit is 16 July, two open issues sit
unanswered, and the version number is still 0.x.

## What it automates

Four commands are reachable in 0.3: `rpmfusion`, `multimedia`, `nvidia` and
`logs`.

| Command | What it does | Manual equivalent |
| --- | --- | --- |
| `rpmfusion` | Installs the free and nonfree release RPMs, enables the four repos | [Third-Party Repositories](repositories.md) |
| `multimedia` | Swaps to RPM Fusion's FFmpeg, installs the `multimedia` group, optional codecs and VA-API drivers | [Multimedia and Codecs](multimedia.md) |
| `nvidia` | Installs `akmod-nvidia` and the CUDA package, optionally writes modprobe and dracut config | [NVIDIA Drivers](nvidia.md) |
| `logs` | Collects journal, `dmesg` and `inxi` output for a support request | — |

**`rpmfusion install`** installs the two release packages from
`mirrors.rpmfusion.org` for the release `rpm -E %fedora` reports, then enables
`rpmfusion-free`, `rpmfusion-free-updates`, `rpmfusion-nonfree` and
`rpmfusion-nonfree-updates` explicitly. It does not install
`rpmfusion-free-appstream-data` or its nonfree counterpart, so RPM Fusion
packages still will not appear in GNOME Software or KDE Discover afterwards —
the source comment at that point says AppStream metadata, and the command it
runs is `dnf install -y @core`. `rpmfusion remove` removes the two release
packages. It does not touch the tainted repository at either end.

**`multimedia install`** requires RPM Fusion and offers to run the `rpmfusion`
step for you if it is missing. The base action is
`dnf install -y ffmpeg @multimedia --skip-unavailable --allowerasing`, which is
the FFmpeg swap and the group install from
[Multimedia and Codecs](multimedia.md) rolled together. It sets neither
`install_weak_deps=False` nor the `PackageKit-gstreamer-plugin` exclusion the
manual page uses, so you get the weak dependencies and you keep the codec-prompt
dialogs.

`--with-optional` reads your GPU from `lspci` and adds a fixed package list —
`sox`, `svt-av1`, `rav1e`, `dav1d`, `libheif-freeworld` and others — plus per
vendor: `intel-media-driver` on Skylake and later or `libva-intel-driver`
before it, `mesa-va-drivers-freeworld` and `mesa-vdpau-drivers-freeworld` on
AMD, and on NVIDIA `libva-nvidia-driver` and `libva-utils` alongside a set of
development packages (`freeglut-devel`, `libX11-devel`, `make`,
`mesa-libGLU-devel` and more) that most desktop users have no use for. Every
one of those installs passes `--skip-unavailable`, so packages Fedora has
dropped — `mesa-vdpau-drivers-freeworld` on Fedora 44, for instance — are
skipped in silence and never reported.

`--config` is Intel-only. It writes `/etc/modprobe.d/intel-fedoratricks.conf`
with `enable_guc` and `enable_fbc=1`, then rebuilds the initramfs.

**`nvidia install`** takes the RPM Fusion route only; negativo17 is not
supported. It matches the card's marketing name from `lspci` against a set of
regular expressions to pick a branch — `RTX`, `GTX 16xx` and similar mean the
current branch, `GTX 9xx`/`GTX 10xx` mean 580xx, `GTX 6xx`/`GTX 7xx` mean 470xx
— then installs `akmod-nvidia` and `xorg-x11-drv-nvidia-cuda` from that branch,
enables `nvidia-persistenced`, and tells you to wait five to ten minutes for
akmods to build the module.

That branch detection is the trap [NVIDIA Drivers](nvidia.md) warns about,
mechanised. Laptop part numbers straddle architectures, the marketing name does
not distinguish them, and the PCI ID that would is not consulted. There is no
390xx branch in the mapping at all. When no pattern matches, the error tells
you to pass `--current`, `--legacy-580xx` or `--legacy-470xx`, none of which
the argument parser accepts. The command is a dead end there. Do it by hand.

The mapping is also a hard-coded list of package names, so its idea of which
branch is "current" ages with the release. That word changed meaning between
Fedora 43 and 44 — see [NVIDIA Drivers](nvidia.md).

`--config` writes `/etc/modprobe.d/nvidia-fedoratricks.conf` with
`NVreg_EnableS0ixPowerManagement=1`, `NVreg_PreserveVideoMemoryAllocations=1`
and `NVreg_EnableResizableBar=1`, enables the suspend, hibernate and resume
services, writes a dracut snippet forcing the NVIDIA modules into the initramfs
for early KMS, and rebuilds it.

**Secure Boot is not handled.** A `secureboot` module exists in the source tree
and is documented in both the README's command reference and the man page, but
it is left out of the dispatcher's command list in 0.3, so `fedoratricks
secureboot enable` reports an unknown command. Nothing in the `nvidia` path
checks `mokutil --sb-state` either. On a machine with Secure Boot on, the tool
will install the driver and leave you with the quiet failure
[Secure Boot](secure-boot.md) describes. Sort that out first, by hand.

## How to run it

The COPR is a personal repository, under the same trust model as anything on
[Third-Party Repositories](repositories.md).

```bash
sudo dnf copr enable rhea/fedoratricks
```

```bash
sudo dnf install fedoratricks
```

Then, **as your normal user**:

```bash
fedoratricks rpmfusion install
```

```bash
fedoratricks multimedia install --with-optional
```

```bash
fedoratricks nvidia install --config
```

Running it under `sudo` fails deliberately — the entry point exits if its
effective UID is 0, and escalates individual commands with `sudo` as it reaches
them. The README and the bundled command reference both give their examples as
`sudo fedoratricks ...`, which no longer works.

Every command takes `-h`, and `man fedoratricks` is installed with the package.
`install` and `remove` are the two actions each modifying command accepts; with
no action it prints help and exits non-zero.

## Trade-offs

**It escalates to root.** It does not run wholesale as root, which limits the
blast radius, and it prints each command before executing it — more visible
than a typical curl-to-shell installer. It is still a program with `sudo`
rights making package and kernel-configuration changes on your machine, from a
COPR outside Fedora's trust boundary, at version 0.3.

**The output goes to a log, not your terminal.** Command output is redirected
by default to `/var/log/fedoratricks`, with
`~/.local/share/fedoratricks/fedoratricks.log` as a fallback. You see the
command lines and a task summary; you do not see dnf's transaction list scroll
past, which is the moment you would normally catch an unexpected
`--allowerasing` removal. If it has to create the log file, it creates it mode
666 — world-writable.

**It makes the decisions for you.** The commands it prints are close to what
the manual pages here use. What it decides: which packages go in the optional
set, whether to suppress weak dependencies, which NVIDIA branch your card
wants, what modprobe options are worth setting. If something breaks later — a
release upgrade stalling on a swapped package, a driver that loads but will not
drive the card — you will be debugging choices you did not make. The printed
commands and the log give you a way back to them.

**Undo is built in, and partial.** Every modifying task registers an undo
alongside its action. If a task fails mid-run, the tool rolls back in reverse
order, and for dnf steps it captures the transaction ID beforehand and reverts
with `dnf history undo -y`. After a successful run, `remove` reverses each
module: `nvidia remove` takes out `akmod-nvidia*` and `xorg-x11-drv-nvidia*`,
deletes both config files and rebuilds the initramfs; `multimedia remove`
reinstalls `ffmpeg-free` with `--disablerepo="rpmfusion*"`; `rpmfusion remove`
removes the release packages. What does not come back is the state you had
before — packages `--allowerasing` removed on the way in are not reinstalled on
the way out, and `rpmfusion remove` leaves any RPM Fusion package you installed
in between still on the system with no repository behind it.

**It follows your Fedora release.** The release number comes from
`rpm -E %fedora` at runtime, so the same version works across upgrades; the
COPR follows Fedora branching and currently builds for 43, 44, 45 and Rawhide.
The NVIDIA branch mapping is the exception.

**Not for atomic desktops.** Silverblue, Kinoite and the other rpm-ostree
variants are detected and refused outright. There is no `rpm-ostree` path.

## Sources

Checked in September 2026. The tool's own documentation, authoritative where it
and this page disagree:

- [fedoratricks on GitHub][fedoratricks] — source, README, and the tagged
  releases
- The bundled [command reference][fedoratricks-docs] and
  [developer guide][fedoratricks-dev], which documents the task and rollback
  system
- The [rhea/fedoratricks COPR][fedoratricks-copr] — build chroots, versions,
  and the project description

The behaviour set out here was read out of `fedoratricks.sh` and the files
under `commands/` at tag `0.3-1`. The tool has not been run end to end on a
test machine.

[fedoratricks]: https://github.com/RheaAyase/fedoratricks
[fedoratricks-copr]: https://copr.fedorainfracloud.org/coprs/rhea/fedoratricks/
[fedoratricks-docs]: https://github.com/RheaAyase/fedoratricks/blob/main/docs/docs.md
[fedoratricks-dev]: https://github.com/RheaAyase/fedoratricks/blob/main/docs/developer.md
