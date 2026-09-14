# negativo17

[negativo17][negativo17] es un repositorio personal. Se solapa con RPM Fusion
en lugar de complementarlo: paquetes divididos más pequeños, más cosas
compiladas desde el código fuente, mayor apego a las directrices de
empaquetado de Fedora y la posibilidad de elegir entre akmods y DKMS para los
módulos del kernel. Está organizado como varios repositorios independientes —
[el de NVIDIA](../nvidia/negativo17.md) es el que quiere la mayoría.

## Por qué existe { #why-it-exists }

El empaquetado dividido es el objetivo. RPM Fusion distribuye el controlador
de NVIDIA como un único paquete grande del que cuelgan subpaquetes;
negativo17 lo parte en piezas más pequeñas, de modo que puedes instalar las
bibliotecas de CUDA sin el controlador gráfico, o las bibliotecas de 32 bits
por separado. También sigue la rama «short-lived» de NVIDIA en lugar de la de
producción, lo que lo sitúa una rama por delante de RPM Fusion buena parte del
tiempo.

A cambio, la cobertura es más estrecha. negativo17 solo empaqueta la rama
actual del controlador, así que una tarjeta antigua que necesite 580, 470 o
390 tiene que recurrir a RPM Fusion.

## Quién lo mantiene { #who-maintains-it }

Simone Caronni, un empaquetador de Fedora afincado en Zúrich que mantiene el
paquete de Steam de Fedora, entre otros. Ha trabajado con desarrolladores de
Fedora para conseguir que el controlador privativo de NVIDIA conviva con la
pila de Mesa mediante glvnd, que es el problema en torno al cual se construyó
el repositorio.

Esta es la infraestructura de una sola persona en lugar de un proyecto
colectivo con un proceso de apadrinamiento, y esa es la principal diferencia
estructural con [RPM Fusion](rpmfusion.md). Tiene una larga trayectoria, y eso
es un juicio sobre el mantenedor, no un cambio en
[el modelo de confianza](index.md#what-you-are-agreeing-to).

## Habilitar el repositorio de NVIDIA { #enabling-the-nvidia-repository }

```bash
sudo dnf config-manager addrepo \
  --from-repofile=https://negativo17.org/repos/fedora-nvidia.repo
```

Eso define `fedora-nvidia` apuntando a
`https://negativo17.org/repos/nvidia/fedora-$releasever/$basearch/`, firmado
con la clave GPG propia del repositorio.

Habilitar este repositorio junto a RPM Fusion no da problemas. Instalar el
controlador de NVIDIA desde ambos sí — consulta
[No los mezcles](index.md#do-not-mix-them-for-the-same-software).

## Fuentes { #sources }

- [negativo17][negativo17], la documentación propia del repositorio
- [El repositorio del controlador de NVIDIA][negativo17-nvidia], para la
  división del empaquetado

[negativo17]: https://negativo17.org/
[negativo17-nvidia]: https://negativo17.org/nvidia-driver/
