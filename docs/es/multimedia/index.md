# Multimedia y códecs

Una instalación recién hecha de Fedora reproduce AV1 y WebM a la perfección y
se atraganta con un MP4 normal y corriente. Eso es lo primero con lo que topa
casi todo el mundo, y es el único problema posinstalación cuyo arreglo exige de
verdad software que Fedora no puede distribuir.

Esta página cubre la situación de los códecs de principio a fin:
[qué funciona ya](#what-already-works),
[qué añade RPM Fusion](#rpm-fusion),
[cómo poner en marcha de verdad la decodificación de vídeo por hardware](#hardware-video-acceleration),
y por qué nada de eso se aplica a
[las aplicaciones Flatpak](#flatpak-apps).

## Por qué la pila multimedia está limitada { #why-the-multimedia-stack-is-limited }

La restricción es legal, no técnica. H.264, HEVC/H.265, VC-1 y varios formatos
MPEG más antiguos están cubiertos por consorcios de patentes que licencian por
unidad, y distribuir decodificadores para ellos supondría pagar a esos
consorcios o asumir la responsabilidad. Consulta la
[página principal](../index.md) para la forma general de ese argumento.

Faltan dos cosas concretas, y ambas se derivan de la misma decisión:

- **El FFmpeg de Fedora es una compilación reducida.** El paquete se llama
  `ffmpeg-free` y está compilado con los decodificadores y codificadores
  sujetos a patentes desactivados. Todo lo que enlaza con `libavcodec` hereda
  eso: mpv, VLC, Chromium, Firefox, el plugin libav de GStreamer.
- **Mesa recibe el mismo trato.** Fedora 44 no distribuye `mesa-va-drivers` en
  absoluto, así que en AMD y en Intel a través de Mesa no hay, de entrada,
  ningún controlador VA-API para los formatos restringidos.

Todo lo que sigue es una manera de reponer esas dos piezas.

## Qué funciona ya { #what-already-works }

Nada de esto necesita un repositorio de terceros:

- **AV1**: dav1d para decodificar, libaom / rav1e / SVT-AV1 para codificar
- **VP8 y VP9**, Theora y toda la ruta WebM
- **Opus, Vorbis, FLAC**, decodificación y codificación de MP3 (LAME),
  decodificación de AAC (`fdk-aac-free`)
- Contenedores **Matroska, WebM, Ogg, MP4**: el contenedor no es el problema,
  lo es la pista de vídeo que lleva dentro
- **H.264 vía OpenH264**, del repositorio `fedora-cisco-openh264`

OpenH264 merece su propio párrafo, porque es la fuente de mucha confusión. Se
compila en la infraestructura de Fedora pero lo distribuye Cisco, que paga las
tasas de licencia del binario. El repositorio viene activado por defecto desde
Fedora 33. Es **solo perfil Constrained Baseline y solo por software**, lo que
significa que cubre las videollamadas WebRTC y poco más: un MP4 de perfil High
a 1080p, que es prácticamente cualquier archivo de vídeo con el que te vayas a
topar, no es algo que OpenH264 pueda decodificar.

Si el repositorio está desactivado en tu instalación:

```bash
sudo dnf config-manager setopt fedora-cisco-openh264.enabled=1
```

```bash
sudo dnf install openh264 mozilla-openh264 gstreamer1-plugin-openh264
```

Lo que *no* funciona en una instalación tal cual: el perfil High de H.264,
HEVC/H.265, VC-1 y la decodificación acelerada por hardware de cualquiera de
ellos en cualquier GPU.

La lista de tu propia máquina, que es la única que importa:

```bash
ffmpeg -hide_banner -decoders | grep -iE 'h264|hevc'
```

El conjunto exacto de decodificadores desactivados cambia entre versiones a
medida que caducan las patentes, así que trata esa salida como la autoridad, por
encima de cualquier lista escrita en otra parte.

## RPM Fusion { #rpm-fusion }

Los códecs de esta página vienen de
[RPM Fusion](../repositories/rpmfusion.md): el lado `free` para los paquetes de
código abierto sujetos a patentes, `nonfree` para el controlador multimedia
completo de Intel. Esa página cubre cómo activarlo, lo que cuesta en confianza y
en soporte, y la variante para escritorios atómicos.

Todo lo que sigue da por supuesto que `free` y `nonfree` están activados.

## Instalar los códecs { #installing-the-codecs }

### Cambiar al FFmpeg completo { #swap-to-the-full-ffmpeg }

Este es el único paso que arregla la mayoría de las cosas:

```bash
sudo dnf swap ffmpeg-free ffmpeg --allowerasing
```

El `ffmpeg` de RPM Fusion declara un conflicto con `ffmpeg-free`, y
`--allowerasing` hace falta de verdad aquí porque toda la familia `libav*-free`
tiene que salir con él.

Lo que ese único comando desbloquea, porque todos estos enlazan con
`libavcodec` o le hacen `dlopen`: mpv, VLC (a través de `vlc-plugin-ffmpeg`), el
Chromium de Fedora, Firefox y el plugin `libav` de GStreamer. También activa las
rutas de decodificación VA-API dentro del propio FFmpeg; la parte de hardware
sigue necesitando un controlador,
[tratada más abajo](#hardware-video-acceleration).

**La alternativa más ligera.** `libavcodec-freeworld` mantiene instalado el
`ffmpeg-free` de Fedora y deja un `libavcodec` más completo en
`/usr/lib64/ffmpeg`, por delante del de Fedora en la ruta del enlazador. Existe
para quien quiere quedarse con la compilación de FFmpeg de Fedora y solo añadir
los decodificadores que faltan:

```bash
sudo dnf install libavcodec-freeworld
```

Elige uno u otro. Si ya has hecho el cambio a `ffmpeg`, a
`libavcodec-freeworld` no le queda nada que complementar y no lo necesitas.

### Plugins de GStreamer { #gstreamer-plugins }

GStreamer es una pila de decodificación distinta de FFmpeg, y es la que usan
GNOME Videos (Totem), GNOME Music, Rhythmbox, Cheese y la mayoría de
aplicaciones multimedia GTK/Qt. El grupo `multimedia` de Fedora cubre los
plugins libres; RPM Fusion extiende ese mismo grupo con los restringidos, y
dnf5 fusiona las dos definiciones:

```bash
sudo dnf group install multimedia --setopt=install_weak_deps=False --exclude=PackageKit-gstreamer-plugin
```

`install_weak_deps=False` evita que arrastre extras recomendados que no has
pedido. `PackageKit-gstreamer-plugin` se excluye porque es la pieza que lanza
los diálogos de «se necesita software adicional para reproducir este archivo»,
que no ayudan una vez has instalado los códecs a mano.

Si prefieres nombrar los paquetes en vez de fiarte de un grupo:

```bash
sudo dnf install gstreamer1-plugins-ugly gstreamer1-plugins-bad-freeworld
```

`gstreamer1-plugins-ugly` (RPM Fusion) convive con el
`gstreamer1-plugins-ugly-free` de Fedora en vez de reemplazarlo.
`gstreamer1-plugins-bad-freeworld` es lo que aporta la decodificación de HEVC a
GStreamer, a través de libde265.

### Extras opcionales { #optional-extras }

```bash
sudo dnf install libheif-freeworld
```

Imágenes HEIC/HEIF: el formato en el que disparan los iPhone. El `libheif` de
Fedora puede leer el contenedor pero no los datos de imagen codificados en HEVC
que lleva dentro.

```bash
sudo dnf install vlc-plugins-freeworld
```

Añade los *codificadores* x264 y x265 a VLC. La decodificación de VLC viene de
FFmpeg, así que esto solo importa si transcodificas.

Los DVD cifrados necesitan el repositorio tainted (consulta
[Repositorios de terceros](../repositories/rpmfusion.md#tainted)) y luego
`libdvdcss`:

```bash
sudo dnf install libdvdcss
```

`libdvdcss` elude el CSS. Si eso es legal donde vives es una pregunta que esta
página no puede responder por ti.

## Aceleración de vídeo por hardware { #hardware-video-acceleration }

La decodificación por software de 1080p va bien en cualquier CPU moderna. El 4K,
el HEVC de alta tasa de bits y la autonomía de un portátil son donde la
decodificación por hardware deja de ser opcional.

**VA-API es la interfaz que importa ahora.** VDPAU está prácticamente acabado en
los controladores abiertos: Mesa eliminó el state tracker de VDPAU en upstream, y
Fedora 44 retiró con ello el paquete `mesa-vdpau-drivers`. `vdpauinfo` sigue
existiendo y sigue informando de algo útil con el controlador privativo de
NVIDIA, que aporta su propia implementación de VDPAU. En AMD e Intel, ignora
VDPAU por completo.

Instala primero las herramientas de diagnóstico:

```bash
sudo dnf install libva-utils
```

```bash
vainfo
```

Lee en la salida tanto los entrypoints como los perfiles. Una línea que diga
`VAProfileH264High : VAEntrypointVLD` significa que hay decodificación por
hardware de H.264 High disponible. Si `vainfo` no informa de ningún controlador,
o solo lista `VAProfileNone`, el problema es el controlador, no el paquete de
códecs.

**Cómo conecta Fedora los controladores de reemplazo.** Fedora parchea libva
para que busque en `/usr/lib64/dri-nonfree`, luego en `/usr/lib64/dri-freeworld`
y luego en `/usr/lib64/dri`. Los controladores de RPM Fusion se instalan en los
dos primeros directorios, así que tienen precedencia automáticamente. No hace
falta `LIBVA_DRIVERS_PATH` ni ninguna otra variable de entorno para que el
cambio surta efecto.

Qué paquete restaura la decodificación por hardware depende de la GPU:

| GPU | Página |
| --- | --- |
| AMD | [Decodificación por hardware en AMD](amd.md) |
| Intel | [Decodificación por hardware en Intel](intel.md) |
| NVIDIA | [Decodificación por hardware en NVIDIA](nvidia.md) |

En Silverblue, Kinoite y las demás variantes rpm-ostree el enfoque entero es
distinto: consulta [Escritorios atómicos](atomic.md).

## Firefox y Chromium { #firefox-and-chromium }

**Firefox** en Fedora carga el FFmpeg del sistema en tiempo de ejecución. Con
`ffmpeg-free` instalado recurre a OpenH264 para H.264, y por eso el vídeo en una
instalación tal cual o falta o se decodifica por software con calidad baseline.
Tras [el cambio a `ffmpeg`](#swap-to-the-full-ffmpeg) obtiene el juego completo
de decodificadores y puede usar VA-API.

Comprueba `about:support` y mira la fila `HARDWARE_VIDEO_DECODING`. «Available
by default» significa que está activa. La decodificación por hardware viene
activada por defecto para los usuarios de Intel y AMD desde
`firefox-101.0.1-4`, y funciona tanto en Wayland como en X11. El interruptor
general es `media.hardware-video-decoding.enabled` en `about:config`.

Cuando no funciona, el registro dice por qué:

```bash
MOZ_LOG="FFmpegVideo:5" firefox
```

Las causas recurrentes, más o menos por orden de frecuencia: `ffmpeg-free` sigue
instalado; no hay ningún controlador VA-API instalado para la GPU; `vainfo`
funciona pero el perfil que usa el sitio no está en la lista (un flujo HEVC de
10 bits en hardware que solo decodifica 8 bits, por ejemplo); o un portátil de
gráficos híbridos está renderizando en una GPU e intentando decodificar en la
otra.

**Chromium** tal como lo empaqueta Fedora enlaza con el `libavcodec` del
sistema, así que el mismo cambio a `ffmpeg` le da H.264 y HEVC. Verifícalo en
`chrome://gpu`: quieres «Video Decode: Hardware accelerated» en lugar de
«Software only». Las versiones recientes de Chromium activan VA-API en Linux sin
banderas de arranque; las antiguas necesitaban
`--enable-features=VaapiVideoDecodeLinuxGL`, que pasó a llamarse
`AcceleratedVideoDecodeLinuxGL` en Chromium 131. Si estás copiando una bandera
de un mensaje antiguo de un foro, ese cambio de nombre es probablemente la razón
de que no haga nada.

**DRM y servicios de streaming.** Firefox descarga el CDM de Widevine por su
cuenta en cuanto permites el contenido controlado por DRM en sus ajustes; no hay
nada que instalar. El Chromium de Fedora no incluye ningún CDM, y ni Fedora ni
RPM Fusion empaquetan uno, así que Netflix y similares no se reproducirán en él.
Si necesitas DRM en un navegador basado en Chromium, usa Google Chrome, que trae
el CDM incorporado. En cualquier caso, cuenta con límites de resolución: los
navegadores de Linux reciben Widevine a nivel de software, y la mayoría de
servicios lo restringen a 720p o 1080p.

## Aplicaciones Flatpak { #flatpak-apps }

Las aplicaciones Flatpak no usan los códecs del anfitrión. Se ejecutan contra un
runtime (normalmente `org.freedesktop.Platform` o un runtime de GNOME/KDE
construido sobre él) con su propio FFmpeg y su propio GStreamer. Instalar todos
los paquetes de esta página no cambia nada para un Firefox en Flatpak y, a la
inversa, los códecs dentro de un Flatpak no hacen nada por las aplicaciones del
anfitrión. Esta es la razón más habitual con diferencia de que alguien informe
de que «los códecs no funcionaron».

**El runtime 25.08 y posteriores** sustituyeron las antiguas extensiones
`ffmpeg-full` y `openh264` por `org.freedesktop.Platform.codecs-extra`, que se
instala automáticamente junto al runtime. No hay nada que hacer.

**El runtime 24.08 y anteriores** todavía necesitan que se añada la extensión a
mano:

```bash
flatpak install flathub org.freedesktop.Platform.ffmpeg-full//24.08
```

La rama debe coincidir con el runtime que usa la aplicación. Averígualo con:

```bash
flatpak info --show-runtime org.videolan.VLC
```

La decodificación por hardware dentro de un Flatpak usa el Mesa del runtime, no
el tuyo, y necesita acceso a `/dev/dri`, que la mayoría de aplicaciones
multimedia ya tienen. La consecuencia práctica es que un Flatpak puede tener
decodificación por hardware funcionando en un anfitrión que no la tenga
instalada, y al revés. Compruébalo con
[los diagnósticos de la propia aplicación](#inside-a-flatpak)
(`about:support`, `chrome://gpu`, la salida de consola de mpv) en vez de dar por
hecho que el resultado del anfitrión se traslada.

## Probar qué admite tu sistema { #testing-what-your-system-supports }

Instalar un paquete y conseguir que una aplicación lo use son dos cosas
distintas, y la mayoría de los avisos de que «los códecs no funcionaron» viven
en el hueco entre ambas. Estas comprobaciones van desde la capa de bibliotecas
hacia fuera, y cada una indica qué aspecto debería tener su salida.

### Qué FFmpeg está instalado { #which-ffmpeg-is-installed }

```bash
dnf5 repoquery --installed --queryformat '%{name} %{from_repo}\n' 'ffmpeg*'
```

`ffmpeg-free` desde `fedora` o `updates` es la compilación reducida de Fedora.
`ffmpeg` desde un repositorio de terceros es la completa. Si tomaste
[la vía de `libavcodec-freeworld`](#swap-to-the-full-ffmpeg) en lugar del
cambio, `ffmpeg-free` sigue instalado y el nombre del paquete deja de responder
la pregunta: guíate por la lista de decodificadores.

Esa lista, el comando de [Qué funciona ya](#what-already-works), es la autoridad
para tu máquina. En el `ffmpeg-free` de Fedora 44 las filas `h264` y `hevc`
están ausentes de ella en vez de presentes y desactivadas, mientras que
`mpeg2video` sí está, porque esas patentes han expirado.

Los codificadores son una lista aparte:

```bash
ffmpeg -hide_banner -encoders | grep -iE 'libx264|libx265|vaapi'
```

La compilación reducida ofrece `libopenh264` para H.264 y nada para HEVC. La
completa añade `libx264` y `libx265` para codificar por software, más
`h264_vaapi` y `hevc_vaapi` para codificar en la GPU.

```bash
ffmpeg -hide_banner -hwaccels
```

Eso imprime los métodos de aceleración con los que se compiló FFmpeg:
normalmente `vaapi`, `vdpau`, `vulkan`, `cuda`, `qsv`. Informa del binario y no
del hardware, así que ver `vaapi` en esa lista no dice nada sobre si hay un
controlador instalado.

Para ver qué pide un archivo concreto:

```bash
ffprobe -hide_banner -v error -select_streams v:0 \
  -show_entries stream=codec_name,profile,pix_fmt \
  -of default=noprint_wrappers=1 video.mp4
```

Una salida de `codec_name=hevc`, `profile=Main 10`, `pix_fmt=yuv420p10le`
significa que el archivo quiere HEVC de 10 bits, una capacidad de hardware
distinta de la de 8 bits. Ese es el valor que hay que cotejar con la lista de
perfiles de `vainfo`.

### Qué tiene GStreamer { #what-gstreamer-has }

GStreamer es la pila que hay detrás de GNOME Videos, Rhythmbox, Cheese y la
mayoría de aplicaciones multimedia GTK y Qt, y mantiene su propio registro de
plugins. El paquete `gstreamer1` aporta el inspector.

```bash
gst-inspect-1.0 | tail -1
```

La línea final resume el registro: `Total count: 237 plugins, 1374
features` en una instalación de escritorio con el juego completo de plugins. El
número por sí solo significa poco; sirve como comparación antes y después.

Leer 1300 features no es una prueba. Pregunta mejor por un elemento concreto:

```bash
gst-inspect-1.0 avdec_h264
```

Un elemento presente imprime un bloque de factory con su `Rank`, su `Klass` y el
`Filename` del plugin del que viene. Uno ausente imprime `No such element or
plugin 'avdec_h264'` y sale con 255, algo que los scripts pueden aprovechar.

`avdec_h264` y `avdec_h265` vienen de `gstreamer1-plugin-libav`, que envuelve el
`libavcodec` que haya instalado y registra solo los códecs que esa biblioteca
aporta. Con `ffmpeg-free` puesto ninguno de los dos elementos existe siquiera:
`avdec_mpeg2video`, `avdec_vp9` y `avdec_aac` están ahí, los envoltorios de
H.264 y HEVC no. Tras el cambio aparecen. El HEVC que llega vía
[`gstreamer1-plugins-bad-freeworld`](#gstreamer-plugins) lo hace como un
elemento distinto, así que búscalo por patrón en vez de adivinando el nombre:

```bash
gst-inspect-1.0 | grep -iE 'h264|h265|hevc'
```

Un plugin también puede cargarse sin nada utilizable dentro:

```bash
gst-inspect-1.0 va
```

Los detalles del plugin seguidos de `0 features` significan que el plugin de
VA-API se cargó y no encontró en el controlador ningún códec que envolver.

### Estado de VA-API { #va-api-state }

Instalar `libva-utils` y ejecutar `vainfo`, y la ruta de búsqueda de
controladores de Fedora, se tratan en
[Aceleración de vídeo por hardware](#hardware-video-acceleration). Lo que
significan las dos columnas de su salida:

- El **perfil** es el formato y su variante: `VAProfileH264High`,
  `VAProfileHEVCMain10`, `VAProfileAV1Profile0`. Un perfil ausente de la lista
  no está disponible, diga lo que diga FFmpeg sobre sus propios decodificadores.
- El **entrypoint** es lo que el hardware hará con ese perfil.
  `VAEntrypointVLD` es decodificación; `VAEntrypointEncSlice` y
  `VAEntrypointEncSliceLP` son codificación. Un perfil listado solo con
  `VAEntrypointVLD` decodifica y no codifica.

Encima de la tabla, `vainfo` nombra el controlador que abrió y la ruta desde la
que lo cargó, que es la manera de confirmar que ganó el orden de búsqueda el
controlador freeworld o nonfree y no el recortado de Fedora.

### ¿Usó la reproducción decodificación por hardware? { #did-playback-use-hardware-decode }

Un `vainfo` limpio informa de lo que la GPU puede hacer. Si una aplicación lo
pidió es otra cuestión, y ambas cosas discrepan lo bastante a menudo como para
que dar por hecho sea donde casi todo esto se tuerce. mpv es la vía más corta
para ver la decisión en directo:

```bash
sudo dnf install mpv
```

```bash
mpv --hwdec=auto video.mp4
```

Si tiene éxito, mpv imprime una línea con el nivel de detalle por defecto:

```
Using hardware decoding (vaapi).
```

`nvdec`, `vulkan` o cualquier variante `-copy` entre paréntesis también es una
ruta de hardware. Que no aparezca esa línea significa decodificación por
software: mpv no anuncia el recurso alternativo, y ese silencio es lo que se
malinterpreta como éxito.

Cuando falta la línea, pregúntale a mpv por qué:

```bash
mpv --hwdec=auto --msg-level=vd=v video.mp4
```

Eso imprime una línea `Looking at hwdec h264-vaapi...` por candidato con el
motivo por el que se rechazó cada uno, los formatos de píxel que ofreció el
decodificador y el perfil de códec que encontró en el archivo.

Después confírmalo contra la carga. La decodificación por software de 4K
mantiene varios núcleos ocupados; la decodificación por hardware apenas los
mueve:

```bash
top -p "$(pgrep -d, -x mpv)"
```

Los contadores del lado de la GPU son más directos donde existen: `radeontop` en
AMD, `intel_gpu_top` (de `igt-gpu-tools`) en Intel y `nvtop`, que sirve para
AMD, Intel y NVIDIA. Vigila el motor de vídeo o de decodificación en vez de la
carga total de la GPU.

### Navegadores { #browsers }

[Firefox y Chromium](#firefox-and-chromium) cubre las lecturas de capacidades:
la fila `HARDWARE_VIDEO_DECODING` en el `about:support` de Firefox y la línea
Video Decode en `chrome://gpu`. Ambas informan de lo que el navegador cree que
puede hacer.

Para saber qué hizo una reproducción concreta, Chromium guarda un registro por
reproductor en `chrome://media-internals`: arranca un vídeo, abre esa página,
selecciona la entrada del reproductor y lee el nombre del decodificador.
`FFmpegVideoDecoder` es decodificación por software; `VaapiVideoDecoder` o
`VDAVideoDecoder` es por hardware. Los nombres exactos han cambiado entre
versiones de Chromium, así que tómalos como una guía de qué buscar y no como una
lista fija. En Firefox el equivalente es la ejecución de `MOZ_LOG` de esa misma
sección.

### Dentro de un Flatpak { #inside-a-flatpak }

Los resultados del anfitrión no se trasladan a un sandbox, así que estas
comprobaciones tienen que ejecutarse dentro de uno. Empieza por las herramientas
que el runtime lleve:

```bash
flatpak run --command=sh io.mpv.Mpv -c 'command -v ffmpeg gst-inspect-1.0 vainfo'
```

En el runtime freedesktop 25.08 eso imprime rutas para `ffmpeg` y
`gst-inspect-1.0` y nada para `vainfo`, que el runtime no incluye. Lo que sí
liste puede ejecutarse ahí mismo:

```bash
flatpak run --command=ffmpeg io.mpv.Mpv -hide_banner -decoders | grep -iE ' (h264|hevc) '
```

Dos filas ahí significan que el FFmpeg del runtime tiene ambos, tenga lo que
tenga el anfitrión. La extensión que los aporta en los runtimes actuales:

```bash
flatpak list --runtime --columns=application,branch | grep -i codecs
```

`org.freedesktop.Platform.codecs-extra` en una rama que coincida con el runtime
de la aplicación es el resultado esperado; consulta
[Aplicaciones Flatpak](#flatpak-apps) para las reglas de ramas y para los
runtimes antiguos. Sustituye `io.mpv.Mpv` por la aplicación que te interese;
cada una responde solo por su propio runtime.

## Resolución de problemas { #troubleshooting }

### ¿Por qué un MP4 se niega a reproducirse cuando los archivos WebM y AV1 sí funcionan? { #why-does-an-mp4-refuse-to-play-when-webm-and-av1-files-work }

El contenedor está bien; la pista de vídeo H.264 o HEVC que lleva dentro es lo
que la compilación de Fedora no puede decodificar, y OpenH264 cubre un perfil
que casi ningún archivo de vídeo usa. El arreglo es
[el cambio de FFmpeg](#swap-to-the-full-ffmpeg), más
[los plugins de GStreamer](#gstreamer-plugins) para GNOME Videos, Rhythmbox y
otras aplicaciones GTK/Qt, que decodifican a través de una pila aparte y
necesitan sus propios paquetes.

### ¿Por qué las aplicaciones Flatpak siguen fallando después de instalar los códecs? { #why-do-flatpak-applications-still-fail-after-installing-the-codecs }

Nunca vieron esa instalación. Un Flatpak decodifica con el FFmpeg y el
GStreamer de su runtime, así que los paquetes del anfitrión no cambian nada
dentro del sandbox. Consulta [Aplicaciones Flatpak](#flatpak-apps) para las
extensiones de runtime y [Dentro de un Flatpak](#inside-a-flatpak) para
confirmar qué contiene el sandbox.

### ¿Por qué hay vídeo pero no sonido, o sonido pero no vídeo? { #why-is-there-video-but-no-sound-or-sound-but-no-video }

Normalmente el flujo es decodificable solo en parte: una pista de audio AAC que
Fedora sí maneja dentro de un MP4 cuya pista de vídeo H.264 no, o al revés.
Confírmalo probando una fuente WebM/AV1 conocida frente a un MP4 conocido. Si
fallan las dos, el problema es el enrutado de audio y no los códecs; comprueba
antes con `wpctl status` que haya un sumidero por defecto razonable.

### ¿Por qué la reproducción en 4K da tirones y los ventiladores se disparan? { #why-is-4k-playback-stuttering-with-the-fans-spinning-up }

Decodificación por software. Tienen que cumplirse dos cosas, y cada una tiene su
propia comprobación: el controlador tiene que exponer el perfil, lo que cubre
[Estado de VA-API](#va-api-state), y la aplicación tiene que aprovecharlo, lo
que cubre
[¿Usó la reproducción decodificación por hardware?](#did-playback-use-hardware-decode).
Lo habitual es encontrar un `vainfo` limpio junto a un reproductor que
decodifica por software, y solo la segunda comprobación lo detecta.

### ¿Por qué sigue faltando HEVC después de instalarlo todo? { #why-is-hevc-still-missing-after-installing-everything }

El HEVC viene de tres sitios distintos según la aplicación:
[el `ffmpeg` completo](#swap-to-the-full-ffmpeg) para todo lo basado en FFmpeg,
[`gstreamer1-plugins-bad-freeworld`](#gstreamer-plugins) para las aplicaciones
GStreamer y [el controlador de la GPU](#hardware-video-acceleration) para la
decodificación por hardware. Instalar uno no cubre los otros. En hardware
anterior a 2015 aproximadamente puede que no haya
decodificación por hardware de HEVC en absoluto, y el HEVC de 10 bits
(contenido HDR) es una capacidad distinta de la de 8 bits: compara el perfil que
`ffprobe` da para el archivo con los perfiles que lista `vainfo`.

### ¿Por qué no se reproducen Netflix y otros servicios de streaming? { #why-wont-netflix-and-other-streaming-services-play }

Consulta la nota sobre DRM en [Firefox y Chromium](#firefox-and-chromium). Si
hay Firefox de por medio, comprueba que «Reproducir contenido controlado por
DRM» esté activado en los ajustes y que el plugin de Widevine aparezca como
instalado en `about:addons`.

### ¿Por qué una actualización de Fedora rompió códecs que antes funcionaban? { #why-did-a-fedora-upgrade-break-codecs-that-used-to-work }

Las actualizaciones a una versión mayor son donde las configuraciones de RPM
Fusion se descosen. Los paquetes de release necesitan actualizarse a la nueva
versión de Fedora, y el cambio a `ffmpeg` puede revertirse en silencio a
`ffmpeg-free` si la resolución de dependencias toma el camino fácil. Después de
cualquier actualización mayor, ejecuta `rpm -q ffmpeg` y rehaz el cambio si
devuelve vacío.

### ¿Por qué falla la decodificación por hardware en NVIDIA cuando está todo instalado? { #why-does-hardware-decode-fail-on-nvidia-when-everything-is-installed }

NVIDIA más VA-API es la combinación que con más probabilidad necesita las
variables de entorno de [la sección de NVIDIA](nvidia.md) de más arriba;
`libva-nvidia-driver` es una capa fina sobre NVDEC y normalmente hay que
apuntarla de forma explícita. Ponlas antes de concluir que la culpa es de los
códecs, y confirma el resultado con
[¿Usó la reproducción decodificación por hardware?](#did-playback-use-hardware-decode)
en vez de a ojo.

## Fuentes { #sources }

Los nombres de paquetes y los comandos de esta página se comprobaron contra
Fedora 44 y los repositorios de RPM Fusion para Fedora 44. Donde algo depende de
la versión se indica en el texto. La documentación upstream, que es la autoridad
cuando esta página y ella discrepan:

- RPM Fusion, [configuración de repositorios][rpmfusion-config] y
  [howto de multimedia][rpmfusion-multimedia]
- RPM Fusion, [OSTree / escritorios atómicos][rpmfusion-ostree]
- Wiki de Fedora, [Hardware Video Acceleration][fedora-hwvideo] y
  [Firefox Hardware acceleration][fedora-firefox-hw]

[rpmfusion-config]: https://rpmfusion.org/Configuration
[rpmfusion-multimedia]: https://rpmfusion.org/Howto/Multimedia
[rpmfusion-ostree]: https://rpmfusion.org/Howto/OSTree
[fedora-hwvideo]: https://fedoraproject.org/wiki/Hardware_Video_Acceleration
[fedora-firefox-hw]: https://fedoraproject.org/wiki/Firefox_Hardware_acceleration
