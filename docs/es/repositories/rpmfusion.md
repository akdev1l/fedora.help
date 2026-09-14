# RPM Fusion

[RPM Fusion][rpmfusion] es el repositorio de terceros estándar de facto para
Fedora, y lo que asume la mayor parte de este sitio. Consta de tres partes:

- **free** — software de código abierto que Fedora excluye por motivos de
  patentes.
  [El FFmpeg completo](../multimedia/index.md#swap-to-the-full-ffmpeg),
  `libavcodec-freeworld`, x264/x265, `mesa-va-drivers-freeworld`,
  [los plugins restringidos de GStreamer](../multimedia/index.md#gstreamer-plugins).
- **nonfree** — redistribuible pero no de código abierto.
  [El controlador de NVIDIA](../nvidia/index.md),
  [el controlador multimedia completo de Intel](../multimedia/intel.md), Steam.
- **tainted** — un repositorio aparte, de activación explícita, para paquetes
  con una posición legal aún peor, en particular `libdvdcss`. No se habilita al
  instalar los otros dos.

## Por qué existe { #why-it-exists }

Las exclusiones de Fedora tienen dos causas distintas, y la división de RPM
Fusion las refleja. Parte del software es libre y de código abierto pero está
cubierto por patentes de software, o resulta arriesgado por otros motivos para
que Red Hat lo distribuya a gran escala desde Estados Unidos; eso es lo que
contiene `free`. Otro software es redistribuible pero no de código abierto, lo
que lo deja fuera de la política de licencias de Fedora sea cual sea su
situación respecto a las patentes; eso es `nonfree`. En ambos casos es legal
ejecutar el código y el empaquetado no tiene nada de polémico. Lo que lo
mantiene fuera son las propias directrices de Fedora.

## Quién lo mantiene { #who-maintains-it }

Un grupo de voluntarios, la mayoría de los cuales son también empaquetadores
activos de Fedora. RPM Fusion sigue las directrices de empaquetado de Fedora, y
su modelo de patrocinio pasa por el de Fedora: solo los patrocinadores de
Fedora pueden patrocinar a un nuevo empaquetador de RPM Fusion. Lo que difiere
es la política sobre qué se puede distribuir, no quién lo distribuye ni con
cuánto cuidado.

El proyecto viene de una fusión. Tres repositorios complementarios
independientes — Livna, Dribble y Freshrpms — anunciaron en noviembre de 2007
que se unirían, y completaron la fusión en noviembre de 2008. Antes de eso, un
escritorio Fedora necesitaba paquetes de varias fuentes incompatibles entre sí;
consolidarlas es la razón por la que un único repositorio de terceros se
convirtió en la norma.

## Habilitar free y nonfree { #enabling-free-and-nonfree }

Los paquetes de release son específicos de cada versión de Fedora.
`$(rpm -E %fedora)` se expande al número de la versión en ejecución, así que
este es el mismo comando que publica la propia
[página de configuración][rpmfusion-config] de RPM Fusion y no hace falta
editarlo:

```bash
sudo dnf install \
  https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

Instala los dos aunque solo hayas venido por uno de ellos. El controlador de
NVIDIA está en `nonfree`, los paquetes multimedia están sobre todo en `free`, y
varios paquetes de `nonfree` dependen de `free`.

Después actualiza y reinicia antes de instalar nada que
[compile un módulo del kernel](../secure-boot.md):

```bash
sudo dnf upgrade --refresh
sudo systemctl reboot
```

## Metadatos de AppStream { #appstream-metadata }

Desde dnf5, los metadatos que hacen que los paquetes de RPM Fusion aparezcan en
GNOME Software y KDE Discover no se instalan automáticamente:

```bash
sudo dnf install rpmfusion-free-appstream-data rpmfusion-nonfree-appstream-data
```

## Tainted { #tainted }

Una segunda activación explícita y deliberada, necesaria para reproducir DVD
cifrados:

```bash
sudo dnf install rpmfusion-free-release-tainted
```

Lo que contiene se trata allí donde se usa — consulta
[Multimedia y códecs](../multimedia/index.md#optional-extras) para `libdvdcss`.

## En escritorios atómicos { #on-atomic-desktops }

Silverblue y Kinoite superponen en su lugar los paquetes de release, y
necesitan un reinicio antes de que los repositorios se puedan usar:

```bash
sudo rpm-ostree install \
  https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

En una actualización de versión mayor, los paquetes de release hay que
reemplazarlos en la misma transacción que el rebase, o la actualización no
resolverá. RPM Fusion lo documenta así:

```bash
sudo rpm-ostree update \
  --uninstall rpmfusion-free-release --uninstall rpmfusion-nonfree-release \
  --install rpmfusion-free-release --install rpmfusion-nonfree-release
```

RPM Fusion documenta el caso atómico al completo en su
[página de OSTree][rpmfusion-ostree].

## Fuentes { #sources }

- RPM Fusion, [configuración del repositorio][rpmfusion-config],
  [OSTree / escritorios atómicos][rpmfusion-ostree] y la
  [documentación para colaboradores][rpmfusion-contributors]
- Las fechas de la fusión provienen del
  [artículo de Wikipedia][rpmfusion-wikipedia], que cita el anuncio de 2007 y
  la finalización en 2008

[rpmfusion]: https://rpmfusion.org/
[rpmfusion-config]: https://rpmfusion.org/Configuration
[rpmfusion-ostree]: https://rpmfusion.org/Howto/OSTree
[rpmfusion-contributors]: https://rpmfusion.org/Contributors
[rpmfusion-wikipedia]: https://en.wikipedia.org/wiki/RPM_Fusion
