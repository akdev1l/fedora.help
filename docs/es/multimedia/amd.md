# Decodificación por hardware en AMD

Lo que necesita la
[aceleración de vídeo por hardware](index.md#hardware-video-acceleration)
en gráficas AMD. Comprueba antes `vainfo` allí.

```bash
sudo dnf install mesa-va-drivers-freeworld
```

Como Fedora ya no distribuye `mesa-va-drivers`, esto es una instalación normal
en lugar de un cambio; el paquete freeworld proporciona ese nombre. Cubre
`radeonsi` y `r600`. Ten en cuenta que la decodificación de AV1 y VP9 en AMD
funciona en Fedora tal cual; lo que este paquete restaura es H.264, HEVC y
VC-1.

La decodificación con Vulkan Video es una vía aparte y más reciente. RPM Fusion
la documenta como un cambio:

```bash
sudo dnf swap mesa-vulkan-drivers mesa-vulkan-drivers-freeworld
```

Solo merece la pena hacerlo si alguna de tus aplicaciones usa específicamente
Vulkan Video; la mayoría siguen usando VA-API.
