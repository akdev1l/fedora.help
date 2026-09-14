# La ruta negativo17

[negativo17](../repositories/negativo17.md) empaqueta el mismo controlador de
NVIDIA que RPM Fusion, de otra manera. [Controladores de NVIDIA](index.md)
documenta la ruta de RPM Fusion y es la que hay que seguir si no tienes ninguna
razón concreta para estar aquí. Esta página cubre la alternativa, y cómo pasar
de una a otra.

Las dos son mutuamente excluyentes. Distribuyen paquetes con **propiedad de
archivos solapada y nombres distintos**, así que dnf instalará piezas de ambas
sin quejarse y te dejará con medio controlador. La propia documentación de
negativo17 abre su sección de instalación diciéndote que elimines antes
cualquier paquete NVIDIA de RPM Fusion.

## Cuál usar { #which-one-to-use }

| | RPM Fusion | negativo17 |
| --- | --- | --- |
| Nombres de los paquetes | `xorg-x11-drv-nvidia*`, `akmod-nvidia` | `nvidia-driver*`, `akmod-nvidia`, `dkms-nvidia` |
| Módulo del kernel | akmod (recompilado localmente) | akmod **o** DKMS, a tu elección |
| Rama en Fedora | production/current | rama de vida corta |
| Versión, septiembre de 2026 (F44) | 610.57.04 | 615.71.09 |
| Ramas heredadas | 580, 470, 390 empaquetadas | ninguna — solo la actual |
| Arranque Seguro | firma automáticamente mediante akmods | firma con akmods, o firmar a mano |
| Estilo de empaquetado | un paquete grande de controlador más subpaquetes | dividido en muchos subpaquetes pequeños |

Las dos funcionan. Ninguna es «correcta».

Elige RPM Fusion si tu tarjeta es antigua y necesita una rama heredada, si usas
[una variante atómica](index.md#atomic-variants-silverblue-kinoite), o si
quieres el camino con más resolución de problemas de la comunidad detrás. Elige
negativo17 si quieres antes las ramas de controlador más nuevas, si quieres
DKMS en lugar de akmods, o si quieres la división de paquetes más fina —
bibliotecas de CUDA sin el controlador de pantalla, por ejemplo.

negativo17 solo empaqueta la rama actual. Si tu tarjeta necesita la 580, la 470
o la 390, esta ruta no está disponible — consulta
[Identifica tu GPU y elige una rama](index.md#identify-your-gpu-and-pick-a-branch).

## Instalación { #install }

Resuelve primero el [Arranque Seguro](../secure-boot.md), igual que en
[la ruta de RPM Fusion](index.md#secure-boot-do-this-before-you-install-anything).
Habilita el repositorio `fedora-nvidia` como se describe en
[Repositorios de terceros](../repositories/negativo17.md), y luego instala con
akmods:

```bash
sudo dnf5 install nvidia-driver akmod-nvidia nvidia-settings
```

O con DKMS en su lugar:

```bash
sudo dnf5 install nvidia-driver dkms-nvidia nvidia-settings
```

DKMS y akmods resuelven el mismo problema — recompilar un módulo fuera del
árbol cuando cambia el kernel — con mecanismos distintos. DKMS se engancha a la
instalación del paquete del kernel y recompila sobre la marcha; akmods se
ejecuta como servicio de systemd. DKMS firma sus módulos con su propia clave
por sistema en `/var/lib/dkms/mok.pub`, que se inscribe con `mokutil --import`
de la misma manera — consulta
[Arranque Seguro](../secure-boot.md#if-you-use-dkms-instead). akmods aquí usa
la misma clave `/etc/pki/akmods` que la ruta de RPM Fusion.

CUDA y lo demás son paquetes separados, que es el sentido de este repositorio:

```bash
# CUDA runtime for the driver, no display components
sudo dnf5 install nvidia-driver-cuda

# 32-bit libraries for Steam and Wine
sudo dnf5 install nvidia-driver-libs.i686
```

Espera a que el módulo se compile y verifícalo antes de reiniciar — la misma
comprobación `modinfo -F version nvidia`, y por las mismas razones, que en
[Qué hace realmente akmods](index.md#what-akmods-actually-does-and-why-you-must-wait).

> La propia página de instalación de negativo17 te dice que
> [desactives el Arranque Seguro](../secure-boot.md#turning-it-off) en lugar de
> firmar, y apunta a la guía de firma de módulos de Red Hat como alternativa.
> La ruta con akmods de arriba también funciona aquí, ya que el mismo paquete
> `akmods` lo compila y lo firma.

## Módulos del kernel abierto y privativo { #open-and-proprietary-kernel-modules }

El empaquetado de negativo17 permite cambiar entre
[las fuentes del módulo del kernel privativo y abierto](index.md#open-vs-proprietary-kernel-module)
mediante `/etc/nvidia/kernel.conf`, recompilando con `akmods --rebuild` o con
el par equivalente `dkms build` / `dkms install`. Su documentación recoge los
comandos exactos; hacen referencia a versiones del controlador de la época de
la 545, así que trata esas cadenas de versión como ejemplos más que como
versiones actuales.

## Cambiar de una a otra { #switching-between-the-two }

No instales una encima de la otra. Elimina la primera por completo, y luego
instala la segunda.

**RPM Fusion → negativo17:**

```bash
sudo dnf5 remove 'xorg-x11-drv-nvidia*' 'akmod-nvidia*'
sudo dnf5 config-manager addrepo \
  --from-repofile=https://negativo17.org/repos/fedora-nvidia.repo
sudo dnf5 install nvidia-driver akmod-nvidia
```

**negativo17 → RPM Fusion:**

```bash
sudo dnf5 remove 'nvidia-driver*' 'dkms-nvidia*' 'akmod-nvidia*' 'nvidia-kmod-common'
sudo dnf5 config-manager setopt fedora-nvidia.enabled=0
sudo dnf5 install akmod-nvidia
```

> **No** uses `dnf remove '*nvidia*'` para esto, aunque lo verás sugerido. Ese
> glob coincide con `nvidia-gpu-firmware`, un paquete de Fedora que nouveau y
> `nova_core` necesitan para poder siquiera arrancar tu tarjeta. Eliminarlo te
> deja sin ningún controlador funcional de ningún tipo.

Entre la eliminación y la reinstalación, tu máquina no tiene ningún controlador
de NVIDIA. Ejecuta la secuencia entera de una sentada, y verifica con `modinfo`
antes de reiniciar. Si algo sale mal a medio camino, todavía puedes arrancar —
la eliminación
[quita la lista negra de nouveau de los argumentos del kernel](index.md#what-the-package-changed-on-your-machine).

## ¿Cómo sé cuál está instalado? { #how-do-i-tell-which-one-is-installed }

```bash
dnf5 repoquery --installed '*nvidia*' --queryformat '%{name} %{from_repo}\n'
```

Si hay paquetes que vienen de más de uno de `rpmfusion-nonfree*` y
`fedora-nvidia`, empieza de nuevo desde una eliminación limpia usando la
secuencia de arriba.

## Fuentes { #sources }

- [negativo17][negativo17], la documentación del propio repositorio
- RPM Fusion, [NVIDIA HowTo][rpmfusion-nvidia]

[negativo17]: https://negativo17.org/
[rpmfusion-nvidia]: https://rpmfusion.org/Howto/NVIDIA
