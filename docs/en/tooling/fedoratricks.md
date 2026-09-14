# Fedora Tricks

<div class="facts" markdown>

| | |
| --- | --- |
| Home | [github.com/RheaAyase/fedoratricks][fedoratricks] |
| Maintainer | Rhea Gustavsson, with three other contributors |
| Form | Bash, run from a terminal — no TUI, no GUI |
| Distribution | RPM from the [rhea/fedoratricks COPR][fedoratricks-copr] |
| Licence | MIT |
| Version | 0.3-1, released 16 July 2026 |
| Builds for | Fedora 43, 44, 45 and Rawhide, x86_64 and aarch64 |

</div>

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
| `rpmfusion install` | Installs the free and nonfree release packages for the release `rpm -E %fedora` reports, then enables the four repositories explicitly | [Third-Party Repositories](../repositories.md) |
| `rpmfusion remove` | Removes the two release packages. The tainted repository is untouched at both ends | |
| `multimedia install` | Swaps RPM Fusion's FFmpeg in for `ffmpeg-free` and installs the `multimedia` group, offering to run the `rpmfusion` step first if the repositories are missing | [Multimedia and Codecs](../multimedia.md) |
| `multimedia install --with-optional` | Adds codec extras, then reads the GPU from `lspci` and adds the VA-API driver for it | |
| `multimedia install --config` | Intel only. Writes `/etc/modprobe.d/intel-fedoratricks.conf` with `enable_guc` and `enable_fbc=1`, then rebuilds the initramfs | |
| `nvidia install` | Picks a driver branch from the card's marketing name, installs `akmod-nvidia` and the matching CUDA package, and enables `nvidia-persistenced` | [NVIDIA Drivers](../nvidia/index.md) |
| `nvidia install --config` | Writes `/etc/modprobe.d/nvidia-fedoratricks.conf` with the power-management and Resizable BAR options, enables the sleep services, and forces the modules into the initramfs | |
| `logs` | Collects journal, `dmesg` and `inxi` output for a support request | — |

Both `install` commands have a matching `remove`.

## How to run it

The COPR is a personal repository, under the same trust model as anything on
[Third-Party Repositories](../repositories.md#copr).

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
COPR [outside Fedora's trust boundary](../repositories.md#what-you-are-agreeing-to),
at version 0.3.

**The output goes to a log, not your terminal.** Command output is redirected
by default to `/var/log/fedoratricks`, with
`~/.local/share/fedoratricks/fedoratricks.log` as a fallback. You see the
command lines and a task summary; you do not see dnf's transaction list scroll
past, which is the moment you would normally catch an unexpected
`--allowerasing` removal. If it has to create the log file, it creates it mode
666 — world-writable.

**It makes the decisions for you.** The commands it prints are close to what
the manual pages here use. What it decides: which packages go in the optional
set, whether to suppress weak dependencies,
[which NVIDIA branch your card wants](../nvidia/index.md#identify-your-gpu-and-pick-a-branch),
what modprobe options are worth setting. If something breaks later — a
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

**Not for atomic desktops.** Silverblue, Kinoite and the other
[rpm-ostree variants](../repositories.md#on-atomic-desktops) are detected and
refused outright. There is no `rpm-ostree` path.

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
