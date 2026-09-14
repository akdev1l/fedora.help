# Secure Boot

Secure Boot is the firmware checking a signature before it runs anything. On
Fedora it works out of the box, and it keeps working until you install a kernel
module Fedora did not sign — the NVIDIA driver, VirtualBox, some Wi-Fi and
touchpad drivers, anything built by akmods or DKMS. The kernel then refuses to
load the module.

That refusal is quiet. There is no error in the installation output, and the
symptom arrives one reboot later: a black screen, or a desktop running on a
fallback driver at the wrong resolution. This page covers the two ways out.

## Check what you have

```bash
mokutil --sb-state
```

`SecureBoot enabled` means anything below applies to you. `SecureBoot disabled`
means unsigned modules load fine and you can skip this page, at the cost
described in [Turning it off](#turning-it-off).

## Enrolling your own key

The approach Fedora and RPM Fusion document: generate a keypair, enroll the
public half in the firmware's Machine Owner Key list, and let akmods sign every
module it builds with it. Do this **before** installing a driver — doing it
afterwards works, but you get one bad boot in between.

This reproduces RPM Fusion's [Secure Boot HowTo][rpmfusion-secureboot].

```bash
sudo dnf install akmods mokutil openssl
```

Generate the keypair. `-a` accepts the defaults instead of prompting you
through a certificate config:

```bash
sudo kmodgenca -a
```

That writes the certificate to `/etc/pki/akmods/certs/` and the private key to
`/etc/pki/akmods/private/`. akmods generates this key on its own first run if
you skip the step; doing it deliberately means you know where it is.

> The private key lives unencrypted on your root filesystem. Anything that can
> read it can sign a kernel module your machine will trust. If the disk is not
> encrypted, that is the trade you are making. RPM Fusion treats full-disk
> encryption as a requirement here.

Queue the public key for enrollment:

```bash
sudo mokutil --import /etc/pki/akmods/certs/public_key.der
```

`mokutil` asks you to set a one-time password. You type it at the next boot, so
pick something short and unambiguous.

```bash
sudo systemctl reboot
```

The next boot stops at a blue **MOK Management** screen before the bootloader
hands off. This is not an error. Choose **Enroll MOK** → **Continue** → **Yes**,
then enter the password you just set.

> The MOK Manager keyboard is hardcoded to US QWERTY whatever your layout is.
> On AZERTY, Dvorak or anything else, the password you type is not the password
> you think you are typing. Choose accordingly.

The system reboots again. Confirm the key took:

```bash
sudo mokutil --test-key /etc/pki/akmods/certs/public_key.der
```

From here akmods signs every module it builds with that key, for this kernel
and every future one.

### If you use DKMS instead

DKMS signs with its own per-system key at `/var/lib/dkms/mok.pub`, enrolled
with the same `mokutil --import` step. The rest of the flow is identical.
[negativo17](repositories.md#negativo17) offers DKMS as an alternative to
akmods; RPM Fusion uses akmods only.

## Turning it off

Disable Secure Boot in your firmware setup and the unsigned module loads. What
you give up is the firmware's verification of the boot chain: the bootloader
and kernel are no longer checked against a signature before they run, so a
compromise that reaches your ESP or `/boot` can persist across reinstalls
undetected.

Check two things first. Some systems tie BitLocker or a TPM policy to Secure
Boot state, which matters on a dual-boot machine. And some firmware hides the
setting until you set a supervisor password.

## On atomic desktops

Silverblue, Kinoite and the rest build modules while composing a deployment,
which means the signing key has to be available during the compose — it has to
be packaged rather than sitting in `/etc`. RPM Fusion points at the third-party
[silverblue-akmods-keys][sbkeys] repository for this. It has had no commits
since 2023, so verify it against your release before relying on it.

Prebuilt images sidestep the problem by shipping modules already signed with
the project's key; you enroll that key once. Universal Blue's images wrap it in
`ujust enroll-secure-boot-key`, where the password is set by the image rather
than by you.

## What breaks it later

- **Firmware updates can clear enrolled MOK keys.** If a module stops loading
  after a BIOS or UEFI update, re-run the `mokutil --import` step and enroll
  again.
- **This key signs modules, not kernels.** A self-compiled kernel is a separate
  problem with a separate solution.
- **One attempt per reboot.** Getting the MOK password wrong means rebooting
  and starting the enrollment prompt again.

## Troubleshooting

**The module built but will not load.** Confirm the module exists for the
running kernel, then check the signature state:

```bash
sudo dmesg | grep -i 'Loading of unsigned module\|module verification failed'
mokutil --test-key /etc/pki/akmods/certs/public_key.der
```

**Black screen after installing a driver.** Boot the previous kernel from the
GRUB menu, or add `nomodeset` to the kernel command line from the GRUB editor,
then work from a TTY. [NVIDIA Drivers](nvidia/index.md) has the full recovery
sequence for that case.

**`mokutil --test-key` says the key is not enrolled, but you enrolled it.**
Either the MOK Manager password was mistyped — see the QWERTY note above — or a
firmware update cleared the key store.

## Sources

- RPM Fusion, [Secure Boot HowTo][rpmfusion-secureboot]
- Fedora documentation, [signing kernel modules][fedora-signing]
- [silverblue-akmods-keys][sbkeys], for the atomic case

[rpmfusion-secureboot]: https://rpmfusion.org/Howto/Secure%20Boot
[fedora-signing]: https://docs.fedoraproject.org/en-US/quick-docs/mok-enrollment/
[sbkeys]: https://github.com/CheariX/silverblue-akmods-keys
