# AMD Hardware Decode

What [hardware video acceleration](index.md#hardware-video-acceleration)
needs on AMD graphics. Check `vainfo` there first.

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
