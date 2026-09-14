# Intel Hardware Decode

What [hardware video acceleration](index.md#hardware-video-acceleration)
needs on Intel graphics. Check `vainfo` there first.

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
