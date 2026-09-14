# Escritorios atómicos

En Silverblue, Kinoite y las demás variantes atómicas, `dnf` no es la
herramienta; `rpm-ostree` superpone paquetes sobre la imagen base, y cada
cambio cuesta un reinicio, ralentiza todas las actualizaciones posteriores y es
una cosa más que puede bloquear un rebase. Por eso la respuesta habitual en
atómico es Flatpak primero: instala VLC, mpv, Firefox y el resto desde Flathub
y deja que [sus runtimes traigan sus propios códecs](index.md#flatpak-apps), lo
que permite saltarse esta página entera.

Si aun así quieres la pila del sistema anfitrión superpuesta, superpón primero
los paquetes de release de RPM Fusion y reinicia — consulta
[Repositorios de terceros](../repositories/rpmfusion.md#on-atomic-desktops).

El cambio de FFmpeg no tiene equivalente en `rpm-ostree`, así que se expresa
como un override que elimina toda la familia `-free` e instala el reemplazo en
una sola transacción:

```bash
sudo rpm-ostree override remove \
  ffmpeg-free libavcodec-free libavdevice-free libavfilter-free \
  libavformat-free libavutil-free libpostproc-free libswresample-free \
  libswscale-free fdk-aac-free \
  --install ffmpeg
```

Los paquetes de controladores de hardware se superponen con normalidad —
`mesa-va-drivers-freeworld`, `intel-media-driver` o `libva-nvidia-driver`,
[la misma elección que arriba](index.md#hardware-video-acceleration).

Una trampa específica de atómico: en una actualización de versión mayor, los
paquetes de release de RPM Fusion hay que reemplazarlos en la misma transacción
que el rebase — consulta
[Repositorios de terceros](../repositories/rpmfusion.md#on-atomic-desktops).
