# Atomic Desktops

On Silverblue, Kinoite and the other atomic variants, `dnf` is not the tool;
`rpm-ostree` layers packages onto the base image, and every change costs a
reboot, slows every subsequent update, and is one more thing that can block a
rebase. That is why the usual answer on atomic is Flatpak-first: install VLC,
mpv, Firefox and the rest from Flathub and let
[their runtimes bring their own codecs](index.md#flatpak-apps), which sidesteps this
entire page.

If you do want the host stack layered, layer the RPM Fusion release packages
first and reboot — see
[Third-Party Repositories](../repositories/rpmfusion.md#on-atomic-desktops).

The FFmpeg swap has no `rpm-ostree` equivalent, so it is expressed as an override
that removes the whole `-free` family and installs the replacement in one
transaction:

```bash
sudo rpm-ostree override remove \
  ffmpeg-free libavcodec-free libavdevice-free libavfilter-free \
  libavformat-free libavutil-free libpostproc-free libswresample-free \
  libswscale-free fdk-aac-free \
  --install ffmpeg
```

The hardware driver packages layer normally — `mesa-va-drivers-freeworld`,
`intel-media-driver` or `libva-nvidia-driver`,
[same choice as above](index.md#hardware-video-acceleration).

One atomic-specific trap: at a major release upgrade the RPM Fusion release
packages have to be replaced in the same transaction as the rebase — see
[Third-Party Repositories](../repositories/rpmfusion.md#on-atomic-desktops).
