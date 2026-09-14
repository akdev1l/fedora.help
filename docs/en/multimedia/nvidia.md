# NVIDIA Hardware Decode

What [hardware video acceleration](index.md#hardware-video-acceleration)
needs on NVIDIA graphics. Check `vainfo` there first.

NVIDIA needs the proprietary driver first — that is
[its own chapter](../nvidia/index.md), and everything here assumes it is already
installed and working. The VA-API side is a shim that translates VA-API calls
to NVDEC, and Fedora now ships it in the main repositories:

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

## Sources

- [nvidia-vaapi-driver][nvidia-vaapi], upstream of `libva-nvidia-driver`

[nvidia-vaapi]: https://github.com/elFarto/nvidia-vaapi-driver
