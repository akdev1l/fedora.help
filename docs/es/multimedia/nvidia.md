# Decodificación por hardware en NVIDIA

Lo que necesita la
[aceleración de vídeo por hardware](index.md#hardware-video-acceleration)
en gráficas NVIDIA. Comprueba `vainfo` allí primero.

NVIDIA necesita antes el controlador privativo — ese es
[su propio capítulo](../nvidia/index.md), y todo lo de aquí da por supuesto que
ya está instalado y funcionando. La parte de VA-API es un shim que traduce las
llamadas de VA-API a NVDEC, y Fedora ya lo distribuye en los repositorios
principales:

```bash
sudo dnf install libva-nvidia-driver
```

Hay dos cosas que conviene saber sobre él. Primero, su propia descripción dice
que está diseñado para la vía de decodificación de Firefox y que "may not
operate correctly in other applications" (puede no funcionar correctamente en
otras aplicaciones) — esa es la valoración de upstream, no una cautela por
nuestra parte. Segundo, por lo general hay que indicarlo de forma explícita. El
proyecto upstream documenta `LIBVA_DRIVER_NAME=nvidia` como obligatoria en las
versiones actuales de libva, `NVD_BACKEND=direct` como el backend recomendado
en el controlador 525 y posteriores, y `MOZ_DISABLE_RDD_SANDBOX=1` para
Firefox. Consulta el [README de upstream][nvidia-vaapi] para conocer el
conjunto actual antes de añadir cualquiera de ellas de forma permanente; las
variables de entorno necesarias han cambiado más de una vez.

Para todo lo demás en NVIDIA, VDPAU sigue funcionando:

```bash
sudo dnf install vdpauinfo
```

```bash
vdpauinfo
```

## Fuentes { #sources }

- [nvidia-vaapi-driver][nvidia-vaapi], upstream de `libva-nvidia-driver`

[nvidia-vaapi]: https://github.com/elFarto/nvidia-vaapi-driver
