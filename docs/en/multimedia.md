# Multimedia and Codecs

A fresh Fedora install plays AV1 and WebM perfectly and chokes on a plain MP4.
That is the first thing most people hit, and it is the one post-install problem
where the fix genuinely requires software Fedora cannot ship.

This page covers the codec situation end to end: what already works, what RPM
Fusion adds, how to get hardware video decoding actually running, and why none
of it applies to your Flatpak apps.

## Why the multimedia stack is limited

The constraint is legal, not technical. H.264, HEVC/H.265, VC-1 and several
older MPEG formats are covered by patent pools that license per-unit, and
shipping decoders for them would mean paying those pools or accepting the
liability. See the [landing page](index.md) for the general shape of that
argument.

Two specific things are missing, and both follow from the same decision:

- **Fedora's FFmpeg is a reduced build.** The package is called `ffmpeg-free`,
  and it is compiled with the patent-encumbered decoders and encoders switched
  off. Everything that links `libavcodec` inherits that — mpv, VLC, Chromium,
  Firefox, GStreamer's libav plugin.
- **Mesa gets the same treatment.** Fedora 44 does not ship `mesa-va-drivers` at
  all, so on AMD and on Intel-via-Mesa there is no VA-API driver for the
  restricted formats to begin with.

Everything below is a way of putting those two pieces back.

## What already works

None of this needs a third-party repository:

- **AV1** — dav1d for decode, libaom / rav1e / SVT-AV1 for encode
- **VP8 and VP9**, Theora, and the whole WebM path
- **Opus, Vorbis, FLAC**, MP3 decode and encode (LAME), AAC decode
  (`fdk-aac-free`)
- **Matroska, WebM, Ogg, MP4** containers — the container is not the problem,
  the video track inside it is
- **H.264 via OpenH264**, from the `fedora-cisco-openh264` repository

OpenH264 deserves its own paragraph, because it is the source of a lot of
confusion. It is built in Fedora's infrastructure but distributed by Cisco,
which pays the licence fees for the binary. The repository has been enabled by
default since Fedora 33. It is **Constrained Baseline profile only and software
only**, which means it covers WebRTC video calls and little else — a 1080p High
profile MP4, which is essentially every video file you will encounter, is not
something OpenH264 can decode.

If the repository is disabled on your install:

```bash
sudo dnf config-manager setopt fedora-cisco-openh264.enabled=1
```

```bash
sudo dnf install openh264 mozilla-openh264 gstreamer1-plugin-openh264
```

What does *not* work on a stock install: H.264 High profile, HEVC/H.265, VC-1,
and hardware-accelerated decode of any of them on any GPU.

The list for your own machine, which is the only one that matters:

```bash
ffmpeg -hide_banner -decoders | grep -iE 'h264|hevc'
```

The exact set of disabled decoders shifts between releases as patents lapse, so
treat that output as the authority rather than any list written down elsewhere.

## RPM Fusion

The codecs on this page come from [RPM Fusion](repositories.md#rpm-fusion): the
`free` side for the patent-encumbered open source packages, `nonfree` for
Intel's full media driver. That page covers enabling it, what it costs you in
trust and support, and the atomic-desktop variant.

Everything below assumes `free` and `nonfree` are enabled.

## Installing the codecs

### Swap to the full FFmpeg

This is the single step that fixes most things:

```bash
sudo dnf swap ffmpeg-free ffmpeg --allowerasing
```

RPM Fusion's `ffmpeg` declares a conflict with `ffmpeg-free`, and
`--allowerasing` is genuinely required here because the whole `libav*-free`
family has to come out with it.

What that one command unlocks, because all of these link or `dlopen`
`libavcodec`: mpv, VLC (through `vlc-plugin-ffmpeg`), Fedora's Chromium,
Firefox, and GStreamer's `libav` plugin. It also switches on the VA-API decode
paths inside FFmpeg itself — the hardware side still needs a driver, covered
below.

**The lighter alternative.** `libavcodec-freeworld` keeps Fedora's `ffmpeg-free`
installed and drops a fuller `libavcodec` into `/usr/lib64/ffmpeg`, ahead of the
Fedora one on the linker path. It exists for people who want to stay on Fedora's
FFmpeg build and only add the missing decoders:

```bash
sudo dnf install libavcodec-freeworld
```

Pick one or the other. If you have done the `ffmpeg` swap, `libavcodec-freeworld`
has nothing left to complement and you do not need it.

### GStreamer plugins

GStreamer is a separate decode stack from FFmpeg, and it is what GNOME Videos
(Totem), GNOME Music, Rhythmbox, Cheese and most GTK/Qt media apps use. Fedora's
`multimedia` group covers the free plugins; RPM Fusion extends the same group
with the restricted ones, and dnf5 merges the two definitions:

```bash
sudo dnf group install multimedia --setopt=install_weak_deps=False --exclude=PackageKit-gstreamer-plugin
```

`install_weak_deps=False` keeps it from dragging in recommended extras you did
not ask for. `PackageKit-gstreamer-plugin` is excluded because it is the piece
that pops up "additional software is required to play this file" dialogs, which
are unhelpful once you have installed the codecs by hand.

If you would rather name the packages than trust a group:

```bash
sudo dnf install gstreamer1-plugins-ugly gstreamer1-plugins-bad-freeworld
```

`gstreamer1-plugins-ugly` (RPM Fusion) coexists with Fedora's
`gstreamer1-plugins-ugly-free` rather than replacing it.
`gstreamer1-plugins-bad-freeworld` is what provides HEVC decode to GStreamer, via
libde265.

### Optional extras

```bash
sudo dnf install libheif-freeworld
```

HEIC/HEIF images — the format iPhones shoot in. Fedora's `libheif` can read the
container but not the HEVC-coded image data inside it.

```bash
sudo dnf install vlc-plugins-freeworld
```

Adds the x264 and x265 *encoders* to VLC. VLC's decoding comes from FFmpeg, so
this only matters if you transcode.

Encrypted DVDs need the tainted repository — see
[Third-Party Repositories](repositories.md#tainted) — and then `libdvdcss`:

```bash
sudo dnf install libdvdcss
```

`libdvdcss` circumvents CSS. Whether that is lawful where you live is a question
this page cannot answer for you.

## Hardware video acceleration

Software decode of 1080p is fine on any modern CPU. 4K, high-bitrate HEVC, and
laptop battery life are where hardware decode stops being optional.

**VA-API is the interface that matters now.** VDPAU is effectively finished on
the open drivers: Mesa removed the VDPAU state tracker upstream, and Fedora 44
dropped the `mesa-vdpau-drivers` package with it. `vdpauinfo` still exists and still
reports something useful on NVIDIA's proprietary driver, which provides its own
VDPAU implementation. On AMD and Intel, ignore VDPAU entirely.

Install the diagnostic tools first:

```bash
sudo dnf install libva-utils
```

```bash
vainfo
```

Read the output for entrypoints as well as profiles. A line reading
`VAProfileH264High : VAEntrypointVLD` means hardware decode of H.264 High is
available. If `vainfo` reports no driver at all, or lists only `VAProfileNone`,
the driver is the problem, not the codec package.

**How Fedora wires the replacement drivers.** Fedora patches libva to search
`/usr/lib64/dri-nonfree`, then `/usr/lib64/dri-freeworld`, then `/usr/lib64/dri`.
RPM Fusion's drivers install into the first two directories, so they take
precedence automatically. You do not need `LIBVA_DRIVERS_PATH` or any other
environment variable to make the swap take effect.

### AMD

```bash
sudo dnf install mesa-va-drivers-freeworld
```

Since Fedora no longer ships `mesa-va-drivers`, this is a plain install rather
than a swap; the freeworld package provides the name. It covers `radeonsi` and
`r600`. Note that AV1 and VP9 decode on AMD work on stock Fedora — it is H.264,
HEVC and VC-1 that this package restores.

Vulkan Video decode is a separate, newer path. RPM Fusion documents it as a
swap:

```bash
sudo dnf swap mesa-vulkan-drivers mesa-vulkan-drivers-freeworld
```

Only worth doing if you have an application that specifically uses Vulkan Video;
most still use VA-API.

### Intel

Fedora ships `libva-intel-media-driver`, which is its own build of Intel's iHD
driver with the restricted codecs removed. RPM Fusion's nonfree repository ships
the complete `intel-media-driver`, which installs to `/usr/lib64/dri-nonfree`
and therefore wins the search order:

```bash
sudo dnf install intel-media-driver
```

For older Intel graphics (roughly pre-Broadwell, the i965 generation), the driver
is a different one and lives in RPM Fusion free:

```bash
sudo dnf install libva-intel-driver
```

If `vainfo` picks the wrong driver on a machine that could use either, force it:

```bash
LIBVA_DRIVER_NAME=iHD vainfo
```

### NVIDIA

NVIDIA needs the proprietary driver first — that is its own chapter, and
everything here assumes it is already installed and working. The VA-API side is
a shim that translates VA-API calls to NVDEC, and Fedora now ships it in the
main repositories:

```bash
sudo dnf install libva-nvidia-driver
```

Two things to know about it. First, its own description says it is designed for
Firefox's decode path and "may not operate correctly in other applications" —
that is upstream's assessment, not a hedge. Second, it usually needs to be
pointed at explicitly. The upstream project documents `LIBVA_DRIVER_NAME=nvidia`
as required on current libva, `NVD_BACKEND=direct` as the recommended backend on
driver 525 and later, and `MOZ_DISABLE_RDD_SANDBOX=1` for Firefox. Check the
[upstream README][nvidia-vaapi] for the current set before adding any of them
permanently; the required variables have changed more than once.

For everything else on NVIDIA, VDPAU still works:

```bash
sudo dnf install vdpauinfo
```

```bash
vdpauinfo
```

## Firefox and Chromium

**Firefox** on Fedora loads the system FFmpeg at runtime. With `ffmpeg-free`
installed it falls back to OpenH264 for H.264, which is why video on a stock
install is either absent or software-decoded at baseline quality. After the
`ffmpeg` swap it gets the full decoder set and can use VA-API.

Check `about:support` and look at the `HARDWARE_VIDEO_DECODING` row. "Available
by default" means it is on. Hardware decode has been enabled by default for
Intel and AMD users since `firefox-101.0.1-4`, and works under both Wayland and
X11. The master switch is `media.hardware-video-decoding.enabled` in `about:config`.

When it is not working, the log tells you why:

```bash
MOZ_LOG="FFmpegVideo:5" firefox
```

The recurring causes, in rough order of frequency: `ffmpeg-free` is still
installed; no VA-API driver is installed for the GPU; `vainfo` works but the
profile the site uses is not in the list (a 10-bit HEVC stream on hardware that
only decodes 8-bit, for instance); or a hybrid-graphics laptop is rendering on
one GPU and trying to decode on the other.

**Chromium** as packaged by Fedora links the system `libavcodec`, so the same
`ffmpeg` swap gives it H.264 and HEVC. Verify at `chrome://gpu` — you want
"Video Decode: Hardware accelerated" rather than "Software only". Recent
Chromium releases enable VA-API on Linux without launch flags; older ones needed
`--enable-features=VaapiVideoDecodeLinuxGL`, which was renamed to
`AcceleratedVideoDecodeLinuxGL` in Chromium 131. If you are copying a flag from
an old forum post, that rename is probably why it does nothing.

**DRM and streaming services.** Firefox downloads the Widevine CDM itself once
you allow DRM-controlled content in its settings; nothing needs installing.
Fedora's Chromium ships no CDM, and neither Fedora nor RPM Fusion packages one,
so Netflix and similar will not play in it. If you need DRM in a Chromium-based
browser, use Google Chrome, which bundles the CDM. Expect resolution caps
regardless: Linux browsers get software-level Widevine, and most services
restrict that to 720p or 1080p.

## Flatpak apps

Flatpak applications do not use your host's codecs. They run against a runtime —
usually `org.freedesktop.Platform` or a GNOME/KDE runtime built on it — with its
own FFmpeg and its own GStreamer. Installing every package on this page changes
nothing for a Flatpak Firefox, and conversely, codecs inside a Flatpak do
nothing for your host applications. This is the single most common reason
someone reports that "the codecs didn't work".

**Runtime 25.08 and newer** replaced the old `ffmpeg-full` and `openh264`
extensions with `org.freedesktop.Platform.codecs-extra`, which is installed
automatically alongside the runtime. There is nothing for you to do.

**Runtime 24.08 and older** still needs the extension added by hand:

```bash
flatpak install flathub org.freedesktop.Platform.ffmpeg-full//24.08
```

The branch must match the runtime the app uses. Find that with:

```bash
flatpak info --show-runtime org.videolan.VLC
```

Hardware decode inside a Flatpak uses the runtime's Mesa, not yours, and needs
access to `/dev/dri` — which most media applications already hold. The practical
consequence is that a Flatpak can have working hardware decode on a host with
none installed, and vice versa. Check with the application's own diagnostics
(`about:support`, `chrome://gpu`, mpv's console output) rather than assuming the
host result carries over.

## Atomic desktops

On Silverblue, Kinoite and the other atomic variants, `dnf` is not the tool;
`rpm-ostree` layers packages onto the base image, and every change costs a
reboot, slows every subsequent update, and is one more thing that can block a
rebase. That is why the usual answer on atomic is Flatpak-first: install VLC,
mpv, Firefox and the rest from Flathub and let their runtimes bring their own
codecs, which sidesteps this entire page.

If you do want the host stack layered, layer the RPM Fusion release packages
first and reboot — see
[Third-Party Repositories](repositories.md#on-atomic-desktops).

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
`intel-media-driver` or `libva-nvidia-driver`, same choice as above.

One atomic-specific trap: at a major release upgrade the RPM Fusion release
packages have to be replaced in the same transaction as the rebase — see
[Third-Party Repositories](repositories.md#on-atomic-desktops).

## Testing what your system supports

Installing a package and having an application use it are two different things,
and most reports that "the codecs did not work" live in the gap between them.
These checks run from the library layer outwards, and each one says what its
output should look like.

### Which FFmpeg is installed

```bash
dnf5 repoquery --installed --queryformat '%{name} %{from_repo}\n' 'ffmpeg*'
```

`ffmpeg-free` from `fedora` or `updates` is Fedora's reduced build. `ffmpeg` from
a third-party repository is the full one. If you took the
`libavcodec-freeworld` route instead of the swap, `ffmpeg-free` stays installed
and the package name stops answering the question — go by the decoder list.

That list, the command in [What already works](#what-already-works), is the
authority for your machine. On Fedora 44's `ffmpeg-free` the `h264` and `hevc`
rows are absent from it rather than present and disabled, while `mpeg2video` is
there, because those patents have expired.

Encoders are a separate list:

```bash
ffmpeg -hide_banner -encoders | grep -iE 'libx264|libx265|vaapi'
```

The reduced build offers `libopenh264` for H.264 and nothing for HEVC. The full
build adds `libx264` and `libx265` for software encode, plus `h264_vaapi` and
`hevc_vaapi` for GPU encode.

```bash
ffmpeg -hide_banner -hwaccels
```

That prints the acceleration methods FFmpeg was compiled with — typically
`vaapi`, `vdpau`, `vulkan`, `cuda`, `qsv`. It reports on the binary rather than
the hardware, so `vaapi` in that list says nothing about whether a driver is
installed.

To see what a particular file asks for:

```bash
ffprobe -hide_banner -v error -select_streams v:0 \
  -show_entries stream=codec_name,profile,pix_fmt \
  -of default=noprint_wrappers=1 video.mp4
```

Output of `codec_name=hevc`, `profile=Main 10`, `pix_fmt=yuv420p10le` means the
file wants 10-bit HEVC, a different hardware capability from 8-bit. That is the
value to match against the `vainfo` profile list.

### What GStreamer has

GStreamer is the stack behind GNOME Videos, Rhythmbox, Cheese and most GTK and
Qt media applications, and it keeps its own plugin registry. The `gstreamer1`
package provides the inspector.

```bash
gst-inspect-1.0 | tail -1
```

The closing line summarises the registry — `Total count: 237 plugins, 1374
features` on a desktop install with the full plugin set. The number means little
on its own; it is useful as a before-and-after.

Reading 1300 features is not a test. Ask about one element instead:

```bash
gst-inspect-1.0 avdec_h264
```

A present element prints a factory block with its `Rank`, `Klass` and the plugin
`Filename` it came from. A missing one prints `No such element or plugin
'avdec_h264'` and exits 255, which scripts can key off.

`avdec_h264` and `avdec_h265` come from `gstreamer1-plugin-libav`, which wraps
whichever `libavcodec` is installed and registers only the codecs that library
provides. With `ffmpeg-free` in place neither element exists at all —
`avdec_mpeg2video`, `avdec_vp9` and `avdec_aac` are there, the H.264 and HEVC
wrappers are not. After the swap they appear. HEVC through
`gstreamer1-plugins-bad-freeworld` arrives as a different element, so find it by
pattern rather than by guessing the name:

```bash
gst-inspect-1.0 | grep -iE 'h264|h265|hevc'
```

A plugin can also load with nothing usable inside it:

```bash
gst-inspect-1.0 va
```

Plugin details followed by `0 features` means the VA-API plugin loaded and found
no codec in the driver to wrap.

### VA-API state

Installing `libva-utils` and running `vainfo`, and Fedora's driver search path,
are covered in [Hardware video acceleration](#hardware-video-acceleration). What
the two columns of its output mean:

- The **profile** is the format and its variant — `VAProfileH264High`,
  `VAProfileHEVCMain10`, `VAProfileAV1Profile0`. A profile that is absent from
  the list is unavailable, whatever FFmpeg reports about its own decoders.
- The **entrypoint** is what the hardware will do with that profile.
  `VAEntrypointVLD` is decode; `VAEntrypointEncSlice` and `VAEntrypointEncSliceLP`
  are encode. A profile listed only with `VAEntrypointVLD` decodes and does not
  encode.

Above the table, `vainfo` names the driver it opened and the path it loaded it
from, which is how to confirm the freeworld or nonfree driver won the search
order rather than Fedora's stripped one.

### Did playback use hardware decode?

A clean `vainfo` reports what the GPU can do. Whether an application asked for it
is a separate question, and the two disagree often enough that assuming is where
most of this goes wrong. mpv is the shortest way to watch the decision happen:

```bash
sudo dnf install mpv
```

```bash
mpv --hwdec=auto video.mp4
```

On success, mpv prints one line at default verbosity:

```
Using hardware decoding (vaapi).
```

`nvdec`, `vulkan` or any `-copy` variant in the brackets is also a hardware path.
No such line means software decode: mpv does not announce the fallback, and that
silence is what gets misread as success.

When the line is missing, ask mpv why:

```bash
mpv --hwdec=auto --msg-level=vd=v video.mp4
```

That prints a `Looking at hwdec h264-vaapi...` line per candidate with the reason
each was rejected, the pixel formats the decoder offered, and the codec profile
it found in the file.

Then confirm against load. Software decode of 4K keeps several cores busy;
hardware decode barely moves them:

```bash
top -p "$(pgrep -d, -x mpv)"
```

GPU-side counters are more direct where they exist: `radeontop` on AMD,
`intel_gpu_top` (from `igt-gpu-tools`) on Intel, and `nvtop`, which handles AMD,
Intel and NVIDIA. Watch the video or decode engine rather than overall GPU load.

### Browsers

[Firefox and Chromium](#firefox-and-chromium) covers the capability readouts:
the `HARDWARE_VIDEO_DECODING` row in Firefox's `about:support`, and the Video
Decode line at `chrome://gpu`. Both report what the browser believes it can do.

For what one playback did, Chromium keeps a per-player log at
`chrome://media-internals`: start a video, open that page, select the player
entry and read the decoder name. `FFmpegVideoDecoder` is software decode;
`VaapiVideoDecoder` or `VDAVideoDecoder` is hardware. The exact names have
changed between Chromium versions, so treat them as a guide to what to look for
rather than a fixed list. In Firefox the equivalent
is the `MOZ_LOG` run in that same section.

### Inside a Flatpak

Host results do not carry into a sandbox, so these checks have to run inside one.
Start with the tools the runtime happens to carry:

```bash
flatpak run --command=sh io.mpv.Mpv -c 'command -v ffmpeg gst-inspect-1.0 vainfo'
```

On the freedesktop 25.08 runtime that prints paths for `ffmpeg` and
`gst-inspect-1.0` and nothing for `vainfo`, which the runtime does not ship.
Anything it does list can be run in place:

```bash
flatpak run --command=ffmpeg io.mpv.Mpv -hide_banner -decoders | grep -iE ' (h264|hevc) '
```

Two rows there means the runtime's FFmpeg has both, whatever the host has. The
extension that supplies them on current runtimes:

```bash
flatpak list --runtime --columns=application,branch | grep -i codecs
```

`org.freedesktop.Platform.codecs-extra` on a branch matching the application's
runtime is the expected result — see [Flatpak apps](#flatpak-apps) for the branch
rules and for older runtimes. Substitute the application you care about for
`io.mpv.Mpv`; each one answers only for its own runtime.

## Troubleshooting

### Why does an MP4 refuse to play when WebM and AV1 files work?

The container is fine; the H.264 or HEVC video track inside it is what Fedora's
build cannot decode, and OpenH264 covers a profile almost no video file uses. The
fix is [the FFmpeg swap](#swap-to-the-full-ffmpeg), plus
[the GStreamer plugins](#gstreamer-plugins) for GNOME Videos, Rhythmbox and other
GTK/Qt applications, which decode through a separate stack and need their own
packages.

### Why do Flatpak applications still fail after installing the codecs?

They never saw the install. A Flatpak decodes with its runtime's FFmpeg and
GStreamer, so host packages change nothing inside the sandbox. See
[Flatpak apps](#flatpak-apps) for the runtime extensions and
[Inside a Flatpak](#inside-a-flatpak) for confirming what the sandbox holds.

### Why is there video but no sound, or sound but no video?

Usually the stream is partly decodable — an AAC audio track Fedora can handle
inside an MP4 whose H.264 video track it cannot, or the reverse. Confirm by
testing a known WebM/AV1 source against a known MP4. If both fail, the problem is
audio routing rather than codecs; check `wpctl status` for a sensible default
sink first.

### Why is 4K playback stuttering with the fans spinning up?

Software decode. Two things have to hold, and each has its own check: the driver
has to expose the profile, which [VA-API state](#va-api-state) covers, and the
application has to take it up, which
[Did playback use hardware decode](#did-playback-use-hardware-decode) covers. A
clean `vainfo` alongside a software-decoding player is the usual finding, and
only the second check catches it.

### Why is HEVC still missing after installing everything?

HEVC comes from three different places depending on the application: the full
`ffmpeg` for anything FFmpeg-based, `gstreamer1-plugins-bad-freeworld` for
GStreamer applications, and the GPU driver for hardware decode. Installing one
does not cover the others. On hardware older than roughly 2015 there may be no
HEVC hardware decode at all, and 10-bit HEVC (HDR content) is a separate
capability from 8-bit — compare the file's `ffprobe` profile against the profiles
`vainfo` lists.

### Why won't Netflix and other streaming services play?

See the DRM note in [Firefox and Chromium](#firefox-and-chromium). If Firefox is
involved, check that "Play DRM-controlled content" is enabled in Settings and
that the Widevine plugin shows as installed under `about:addons`.

### Why did a Fedora upgrade break codecs that used to work?

Major version upgrades are where RPM Fusion setups come apart. The release
packages need updating for the new Fedora version, and the `ffmpeg` swap can
silently revert to `ffmpeg-free` if dependency resolution takes the easy path.
After any major upgrade, run `rpm -q ffmpeg` and re-do the swap if it comes back
empty.

### Why does hardware decode fail on NVIDIA when everything is installed?

NVIDIA plus VA-API is the combination most likely to need the environment
variables in [the NVIDIA section](#nvidia) above; `libva-nvidia-driver` is a shim
over NVDEC and usually has to be pointed at explicitly. Set those before
concluding the codecs are at fault, and confirm the result with
[Did playback use hardware decode](#did-playback-use-hardware-decode) rather than
by eye.

## Sources

The package names and commands on this page were checked against Fedora 44 and
RPM Fusion's Fedora 44 repositories. Where something is version-specific it is
called out in the text. The upstream documentation, which is authoritative when
this page and it disagree:

- RPM Fusion, [repository configuration][rpmfusion-config] and
  [multimedia howto][rpmfusion-multimedia]
- RPM Fusion, [OSTree / atomic desktops][rpmfusion-ostree]
- Fedora wiki, [Hardware Video Acceleration][fedora-hwvideo] and
  [Firefox Hardware acceleration][fedora-firefox-hw]
- [nvidia-vaapi-driver][nvidia-vaapi], upstream of `libva-nvidia-driver`

[rpmfusion-config]: https://rpmfusion.org/Configuration
[rpmfusion-multimedia]: https://rpmfusion.org/Howto/Multimedia
[rpmfusion-ostree]: https://rpmfusion.org/Howto/OSTree
[fedora-hwvideo]: https://fedoraproject.org/wiki/Hardware_Video_Acceleration
[fedora-firefox-hw]: https://fedoraproject.org/wiki/Firefox_Hardware_acceleration
[nvidia-vaapi]: https://github.com/elFarto/nvidia-vaapi-driver
