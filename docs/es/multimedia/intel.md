# Decodificación por hardware en Intel

Lo que necesita la
[aceleración de vídeo por hardware](index.md#hardware-video-acceleration)
en gráficos Intel. Comprueba `vainfo` allí primero.

Fedora distribuye `libva-intel-media-driver`, que es su propia compilación del
controlador iHD de Intel con los códecs restringidos eliminados. El repositorio
nonfree de RPM Fusion distribuye el `intel-media-driver` completo, que se
instala en `/usr/lib64/dri-nonfree` y por tanto gana el orden de búsqueda:

```bash
sudo dnf install intel-media-driver
```

Para gráficos Intel más antiguos (aproximadamente anteriores a Broadwell, la
generación i965), el controlador es otro distinto y vive en RPM Fusion free:

```bash
sudo dnf install libva-intel-driver
```

Si `vainfo` elige el controlador equivocado en una máquina que podría usar
cualquiera de los dos, fuérzalo:

```bash
LIBVA_DRIVER_NAME=iHD vainfo
```
