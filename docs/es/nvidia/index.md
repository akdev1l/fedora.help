# Controladores de NVIDIA

Fedora no distribuye el controlador de NVIDIA, así que en una instalación
recién hecha tu tarjeta funciona sobre la pila abierta. Para mucha gente eso
basta. Para juegos, CUDA, NVENC o cualquier tarjeta más nueva de lo que el
controlador abierto ha alcanzado, no.

Esta página cubre el empaquetado de RPM Fusion, la ruta que dan por supuesta la
mayoría de la documentación de Fedora y la mayoría de la resolución de
problemas de la comunidad.

Todo lo de abajo se comprobó contra fuentes de RPM Fusion, NVIDIA y Fedora en
**septiembre de 2026**, con **Fedora 43 y 44** como objetivo. Los números de
rama del controlador y los cortes de las ramas heredadas cambian. Cuando un
número importa, esta página también te dice cómo comprobarlo tú mismo en lugar
de fiarte del número.

## Lo que tienes sin él { #what-you-get-without-it }

El kernel de Fedora incluye `nouveau`, el controlador de kernel de NVIDIA hecho
por ingeniería inversa, y —desde el kernel de Fedora 44— `nova_core`, el
sucesor basado en Rust que se está construyendo para reemplazarlo en las GPU
basadas en GSP. El espacio de usuario viene de Mesa: OpenGL, más
[**NVK**][nvk], el controlador Vulkan de Mesa para hardware de NVIDIA. NVK es
una implementación conforme de Vulkan 1.4 que cubre desde Kepler
(GeForce 600/700) hasta Ada (RTX 40) y Blackwell de consumo (RTX 50), y desde
Mesa 25.1 las tarjetas Turing y posteriores usan NVK más Zink para OpenGL por
omisión.

Esa pila muestra un escritorio, reproduce vídeo y ejecuta un navegador en
prácticamente cualquier tarjeta NVIDIA. Lo que no hace:

- **Subir las frecuencias de la GPU.** Este es el grande. Nouveau
  [no puede reajustar las frecuencias][nouveau-pm] de las GPU Maxwell ni
  Pascal en absoluto — una GTX 1080 funciona a sus frecuencias de arranque, que
  son una fracción de su rendimiento real. Turing y posteriores salen mejor
  paradas porque el firmware GSP se encarga de la gestión de energía. El
  reajuste de frecuencias en Kepler es parcial.
- **CUDA, NVENC o NVDEC.** No hay implementación abierta. Si necesitas
  codificación por hardware, transcodificación de vídeo o cualquier cosa que
  enlace con `libcuda`, necesitas el controlador privativo.
- **Parte del hardware de última generación.** El soporte abierto llega después
  del lanzamiento, no con él.

El controlador está ausente porque NVIDIA lo distribuye bajo una licencia que
prohíbe la redistribución que Fedora exige — la misma razón por la que
[faltan los códecs](../multimedia/index.md#why-the-multimedia-stack-is-limited).
Consulta la [página principal][index] para la forma general de todo eso.

## ¿Lo necesitas? { #do-you-need-it }

Instálalo si quieres rendimiento 3D serio, cómputo con CUDA u OpenCL,
codificación NVENC, o si tu tarjeta es demasiado nueva para Mesa. No lo
instales si la máquina es un portátil donde lo que más importa es la autonomía,
si la tarjeta es lo bastante antigua como para que ninguna rama soportada la
cubra, o si el escritorio ya funciona y no hay ninguna queja — el controlador
privativo añade un módulo del kernel fuera del árbol que hay que
[reconstruir en cada actualización del kernel](#living-with-kernel-updates), y
eso es un coste de mantenimiento permanente.

Los costes, dichos una sola vez: el controlador no es libre, no es auditable,
lo construye y distribuye un tercero
[fuera del límite de confianza de Fedora](../repositories/index.md#what-you-are-agreeing-to),
y se carga como un módulo del kernel sin firmar salvo que
[lo firmes tú mismo](../secure-boot.md#enrolling-your-own-key).

## Identifica tu GPU y elige una rama { #identify-your-gpu-and-pick-a-branch }

NVIDIA divide su controlador en una rama actual y varias ramas heredadas
congeladas. Instalar la equivocada da un controlador que carga y luego se niega
a manejar tu tarjeta.

Localiza la tarjeta:

```bash
# Every display-class device, with numeric PCI IDs
lspci -nn | grep -E 'VGA|3D|Display'
```

El `[10de:xxxx]` del final es el ID PCI de fabricante:dispositivo. `10de` es
NVIDIA. Si tu tarjeta NVIDIA aparece como `3D controller` en vez de como `VGA
compatible controller`, es un portátil de gráficos híbridos — consulta
[Gráficos híbridos](#hybrid-graphics-optimus-laptops).

Asocia la tarjeta a una rama con el
[listado de controladores Unix][nvidia-unix] de NVIDIA. A fecha de septiembre
de 2026:

| Arquitectura | Tarjetas | Rama |
| --- | --- | --- |
| Turing y posteriores | GTX 16, RTX 20/30/40/50 | actual (610 en F44, 580 en F43) |
| Maxwell, Pascal, Volta | GTX 745/750/750 Ti, GTX 900, GTX 10, TITAN V | 580 |
| Kepler | GeForce 600/700, incluida la GTX 780 Ti | 470 |
| Fermi | GeForce 400/500 | 390 |
| Tesla y anteriores | GeForce 8/9/200/300 y por debajo | ninguna — solo nouveau |

Dos trampas en esa tabla:

**Los números de modelo de portátil cruzan arquitecturas.** La GTX 860M, la 920
y buena parte de las líneas 800M/900M existen como silicio Kepler y como
silicio Maxwell bajo el mismo nombre comercial. El ID PCI es el único
discriminador fiable. Pega el tuyo en la
[lista de chips soportados][chips] de NVIDIA para el controlador actual: si
está en la tabla «Current NVIDIA GPUs» quieres la rama actual, y si aparece más
abajo bajo «The 580.xx driver supports the following set of GPUs» lo que
quieres es esa rama heredada.

**Lo «actual» depende de tu versión de Fedora.** En Fedora 43 la rama actual
*es* la 580, así que las tarjetas Maxwell y Pascal usan el paquete normal. En
Fedora 44 la rama actual pasó a ser la 610 y la 580 se convirtió en un paquete
heredado aparte. La rama 580 es la última que soporta Maxwell, Pascal y Volta
en absoluto; NVIDIA ha dicho que recibirá arreglos de compatibilidad con el
kernel pero ninguna característica nueva.

Por debajo de Fermi no hay nada. La rama 340, que cubría las GeForce
8/9/200/300, no está empaquetada para Fedora 43 ni 44 por RPM Fusion. Esas
tarjetas funcionan con nouveau o no funcionan.

En vez de fiarte de la tabla, pregúntale a tu propio sistema qué existe:

```bash
dnf5 list --available 'akmod-nvidia*'
```

## Empaquetado { #packaging }

Esta página documenta el empaquetado de RPM Fusion, que es lo que dan por
supuesto la mayoría de la documentación de Fedora y la mayoría de la resolución
de problemas de la comunidad.

Un segundo repositorio, negativo17, empaqueta el mismo controlador con nombres
distintos y con propiedad de archivos solapada. Los dos no se pueden mezclar.
Si quieres ramas del controlador más nuevas antes, DKMS en lugar de akmods, o
bibliotecas de CUDA sin el controlador de pantalla, consulta
[La ruta de negativo17](negativo17.md) — compara ambos y contiene el
procedimiento para cambiar de uno a otro.

## Arranque Seguro: haz esto antes de instalar nada { #secure-boot-do-this-before-you-install-anything }

Esta es la forma más común de que esta instalación salga mal. Con el Arranque
Seguro activado y el módulo sin firmar, el kernel se niega a cargarlo y nada en
la salida de la instalación lo dice.

```bash
mokutil --sb-state
```

Si eso dice `SecureBoot enabled`, recorre
[Arranque Seguro](../secure-boot.md) antes de instalar el controlador.

## Instalar el controlador { #installing-the-driver }

### Habilita el repositorio nonfree { #enable-the-nonfree-repository }

El controlador está en el repositorio **nonfree** de RPM Fusion. Habilita
`free` y `nonfree`, después actualiza y reinicia, como se describe en
[Repositorios de terceros](../repositories/rpmfusion.md#enabling-free-and-nonfree).

El reinicio importa aquí. Instala el controlador contra un kernel que no estás
ejecutando y el sistema de akmods se las apañará, pero te habrás complicado tu
propia depuración.

### Instalación { #install }

Rama actual — Turing y posteriores:

```bash
sudo dnf5 install akmod-nvidia
```

Ramas heredadas, si tu tarjeta necesita una:

```bash
# Maxwell / Pascal / Volta, on Fedora 44
sudo dnf5 install akmod-nvidia-580xx xorg-x11-drv-nvidia-580xx

# Kepler
sudo dnf5 install akmod-nvidia-470xx xorg-x11-drv-nvidia-470xx

# Fermi
sudo dnf5 install akmod-nvidia-390xx xorg-x11-drv-nvidia-390xx
```

Para CUDA, OpenCL, NVENC y NVDEC, añade el subpaquete de CUDA — esto es lo que
necesitan `nvidia-smi`, la codificación por hardware de ffmpeg y cualquier cosa
que enlace con `libcuda`:

```bash
sudo dnf5 install xorg-x11-drv-nvidia-cuda
```

Las ramas heredadas tienen el suyo propio, limitado a la última versión de CUDA
que esa rama soportaba: `xorg-x11-drv-nvidia-580xx-cuda`, `-470xx-cuda`,
`-390xx-cuda`.

Para la decodificación de vídeo por VA-API a través del decodificador de
NVIDIA, consulta [Multimedia y códecs](../multimedia/nvidia.md) — el paquete
puente necesita variables de entorno que esa página documenta.

### Lo que akmods hace en realidad, y por qué tienes que esperar { #what-akmods-actually-does-and-why-you-must-wait }

`akmod-nvidia` no contiene un módulo del kernel. Contiene el *código fuente* de
uno, y depende de un conjunto de herramientas de compilación. El servicio
`akmods` construye un RPM kmod de verdad contra tu kernel en ejecución y lo
instala localmente. Dos unidades de systemd lo gobiernan:

- `akmods.service` se ejecuta en el arranque y construye lo que falte.
- `akmods@<kernel>.service` se ejecuta inmediatamente después de una
  transacción RPM del kernel, de modo que el módulo para un kernel recién
  instalado normalmente se construye antes de que reinicies.

Esto significa que el fin de la transacción de dnf **no** es el fin de la
instalación. La compilación se ejecuta después y tarda hasta cinco minutos en
una máquina lenta.

> Reiniciar antes de que la compilación termine es la segunda forma más común
> de acabar en una pantalla en negro. Espera, y comprueba.

Comprueba:

```bash
modinfo -F version nvidia
```

Un número de versión —`610.57.04` o similar— significa que el módulo existe y
que el kernel lo encuentra. `modinfo: ERROR: Module nvidia not found` significa
que no, y reiniciar ahora te dejará caer en nouveau o en nada.

Para comprobar un kernel que no estás ejecutando ahora mismo:

```bash
modinfo -F version nvidia -k 6.19.14-300.fc44.x86_64
```

Si no ha aparecido, mira la compilación:

```bash
systemctl status akmods.service
ls -l /var/cache/akmods/nvidia/
```

Las compilaciones correctas dejan `<version>-for-<kernel>.log`. Los fallos
dejan `<version>-for-<kernel>.failed.log`, y el final de ese archivo es el
error del compilador. Fuerza un reintento con:

```bash
sudo akmods --force --kernels $(uname -r)
```

### Lo que el paquete cambió en tu máquina { #what-the-package-changed-on-your-machine }

Instalar `xorg-x11-drv-nvidia` ejecuta `grubby` sobre todas tus entradas de
arranque para añadir
`rd.driver.blacklist=nouveau,nova_core modprobe.blacklist=nouveau,nova_core`
y para quitar cualquier `nomodeset`. Inspecciona con qué has acabado:

```bash
cat /proc/cmdline
```

El paquete también instala `nvidia-fallback.service`, que se dispara cuando
nouveau está en la lista negra pero `/sys/module/nvidia` no existe — carga
nouveau de todos modos e imprime *"NVIDIA kernel module missing. Falling back
to nouveau"* en la pantalla de bienvenida de Plymouth. Si ves ese mensaje,
tienes un escritorio que funciona y un controlador roto: vuelve a
[`modinfo` de más arriba](#what-akmods-actually-does-and-why-you-must-wait).

Desinstalar quita de nuevo esos argumentos del kernel, así que una eliminación
limpia no te deja con nouveau en la lista negra y nada que lo sustituya.

Por último, los módulos de NVIDIA se mantienen deliberadamente **fuera** del
initramfs. Del arranque temprano se encarga `simpledrm` usando el modo del
firmware. Por eso no necesitas reconstruir el initramfs después de actualizar
el controlador.

### Módulo del kernel abierto frente a privativo { #open-vs-proprietary-kernel-module }

NVIDIA distribuye dos implementaciones en espacio de kernel: la privativa y una
de código abierto (MIT/GPL). El espacio de usuario sigue siendo privativo en
cualquiera de los dos casos. Los paquetes recientes de RPM Fusion incluyen
ambos códigos fuente y eligen entre ellos en tiempo de compilación según el ID
PCI de tu GPU, así que el valor por omisión normalmente es el correcto y no hay
nada que hacer.

Existe un paquete `akmod-nvidia-open` en el
[repositorio `tainted`](../repositories/rpmfusion.md#tainted) de RPM Fusion
para quien necesite parchear el módulo del kernel abierto por su cuenta. Se
mantiene deliberadamente fuera de los repositorios por omisión; si no vas a
modificar el código fuente del módulo, no lo quieres.

### Evita que dnf lo elimine { #keep-dnf-from-removing-it }

El empaquetado de akmods permite que `dnf autoremove` decida que
`akmod-nvidia` es una hoja innecesaria y se lo lleve, junto con las
herramientas de compilación de las que depende. Márcalo como instalado por el
usuario:

```bash
sudo dnf5 mark user akmod-nvidia
```

## Gráficos híbridos (portátiles Optimus) { #hybrid-graphics-optimus-laptops }

En un portátil con gráficos integrados Intel o AMD más un chip NVIDIA, la GPU
de NVIDIA normalmente no tiene ninguna pantalla conectada directamente a ella —
el panel interno cuelga de la iGPU. La tarjeta NVIDIA renderiza, la iGPU
muestra. Eso es el descargue de renderizado de PRIME, y en Fedora lo configuran
automáticamente los paquetes del controlador. No hay nada que preparar.

Para enviar una aplicación concreta a la GPU de NVIDIA:

```bash
# Vulkan applications
__NV_PRIME_RENDER_OFFLOAD=1 vkcube

# GLX applications on Xwayland also need GLVND pointed at the NVIDIA driver
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia glxinfo | grep vendor
```

`__NV_PRIME_RENDER_OFFLOAD` es la que hace el trabajo: carga la capa Vulkan de
NVIDIA y se aplica también a los clientes GLX y EGL.
`__GLX_VENDOR_LIBRARY_NAME` gobierna únicamente la selección de fabricante de
GLX, así que importa para las aplicaciones que se ejecutan a través de Xwayland
y la ignora una aplicación Wayland nativa que dibuje mediante EGL. Poner ambas
es inofensivo.

Ese par de variables es todo lo que hay en los scripts envoltorio
`nvidia-offload` que verás en otras distribuciones. Si quieres uno, son dos
líneas:

```bash
printf '#!/bin/sh\nexport __NV_PRIME_RENDER_OFFLOAD=1\nexport __GLX_VENDOR_LIBRARY_NAME=nvidia\nexec "$@"\n' \
  | sudo tee /usr/local/bin/nvidia-offload >/dev/null
sudo chmod +x /usr/local/bin/nvidia-offload
```

Después, `nvidia-offload steam`, y así sucesivamente. El menú de aplicaciones
de GNOME también ofrece «Launch using Discrete Graphics Card» (lanzar usando la
tarjeta gráfica dedicada) para los lanzamientos desde archivos desktop.

Dos controles más finos, ambos de la documentación de PRIME de NVIDIA tal como
la resumen [las notas sobre Optimus de RPM Fusion][rpmfusion-optimus]:
`__VK_LAYER_NV_optimus=NVIDIA_only` restringe la lista de GPU que ve una
aplicación Vulkan, y `__NV_PRIME_RENDER_OFFLOAD_PROVIDER=NVIDIA-G0` elige una
GPU concreta en una máquina con varias. El nombre que toma es un nombre de
proveedor de X RandR, y `xrandr --listproviders` es lo que imprime esos
nombres — un cliente X11, así que informa de lo que expone el servidor X con el
que habla y no de lo que contiene la máquina. Para el inventario propio de la
máquina de GPU y controladores asociados, usa `sudo lspci -nnk`.

### Gestión de energía { #power-management }

La posición honesta: con el controlador privativo cargado, un portátil Optimus
consume más energía que ese mismo portátil sobre la pila abierta, porque la
pila abierta puede apagar por completo la GPU dedicada y la gestión dinámica de
energía del controlador privativo es menos completa. Donde el firmware lo
permite, desactivar Optimus es la salida fiable de ese compromiso.

Se puede optar por la gestión dinámica de energía:

```bash
sudo tee /etc/modprobe.d/nvidia-dpm.conf >/dev/null <<'EOF'
options nvidia NVreg_DynamicPowerManagement=0x02
EOF
```

`0x02` es el ajuste más agresivo — la GPU se apaga cuando está inactiva.
Reinicia para que surta efecto. Si ves bloqueos al despertar, borra el archivo.

### Monitores externos { #external-monitors }

En algunos portátiles las salidas HDMI o DisplayPort están cableadas a la GPU
de NVIDIA y no a la iGPU. Un monitor externo muerto ahí es una cuestión de qué
GPU es dueña del puerto. Confirma primero qué hay presente y qué está asociado
a ello:

```bash
sudo lspci -nnk
```

El enrutado de la salida entre dos GPU es entonces decisión del compositor, y
el comportamiento varía entre GNOME, KDE y versiones del controlador. El
arreglo que RPM Fusion documenta para esto —un archivo de configuración que
marca la GPU dedicada como primaria— se aplica a las sesiones de Xorg y no
tiene equivalente en Wayland, así que no hay un único cambio de configuración
que merezca la pena reproducir aquí. Consulta las notas de publicación
actuales de tu compositor y del controlador para la versión que tengas.

Donde el firmware ofrezca ese ajuste, desactivar Optimus enruta las salidas a
través de la GPU de NVIDIA de forma permanente. Eso mantiene la GPU dedicada
encendida en todo momento, así que la autonomía baja.

## Convivir con las actualizaciones del kernel { #living-with-kernel-updates }

Cada actualización del kernel de Fedora invalida tu módulo de NVIDIA. Un módulo
construido para 6.19.14 no cargará en 6.20.1. La maquinaria de
[akmod](#what-akmods-actually-does-and-why-you-must-wait) o de
[DKMS](negativo17.md#install) existe para reconstruirlo, y casi siempre lo hace
durante la propia transacción de dnf del kernel.

Falla cuando falla la compilación: un kernel demasiado nuevo para la rama del
controlador, un `kernel-devel` que falta, un cambio en el compilador, quedarse
sin disco. Te enteras en el siguiente reinicio.

**Antes de reiniciar tras cualquier actualización del kernel**, cuando la
máquina te importe:

```bash
sudo dnf5 upgrade
modinfo -F version nvidia -k $(rpm -q --last kernel | head -1 | sed 's/^kernel-//;s/ .*//')
```

Si eso imprime una versión, puedes reiniciar sin riesgo.

### Recuperarse de una pantalla en negro { #recovering-from-a-black-screen }

No has perdido nada. Recorre estos pasos en orden.

**1. Consigue una consola de texto.** Desde la pantalla en negro, prueba
Ctrl+Alt+F3. Si obtienes un indicador de inicio de sesión, el kernel está bien
y solo los gráficos están rotos — salta al paso 4.

**2. Arranca el kernel anterior.** Mantén pulsada Esc (o Mayús en algunos
sistemas) durante el arranque para llegar al menú de GRUB, y elige la entrada
del kernel más antiguo. Fedora mantiene tres instalados por omisión. El kernel
viejo todavía tiene su módulo funcional, así que esto normalmente te devuelve
directamente a un escritorio.

**3. Arranca con nouveau en su lugar.** En el menú de GRUB, pulsa `e` para
editar la entrada, busca la línea `linux` y borra
`rd.driver.blacklist=nouveau,nova_core modprobe.blacklist=nouveau,nova_core`.
Ctrl+X lo arranca. Obtienes un escritorio lento pero funcional con los paquetes
de NVIDIA todavía instalados. Esto es temporal — el cambio no se escribe en
disco.

`nomodeset` en esa misma línea es la versión más drástica: desactiva por
completo el modesetting del kernel y te da un framebuffer sin aceleración.
Úsalo solo si quitar la lista negra no basta.

**4. Reconstruye el módulo.** Desde un TTY o desde una sesión con nouveau:

```bash
sudo akmods --force --kernels $(uname -r)
modinfo -F version nvidia
```

Si la compilación falla, lee el motivo:

```bash
sudo tail -50 /var/cache/akmods/nvidia/*.failed.log
```

Un fallo contra un kernel recién salido normalmente significa que la rama del
controlador no se ha puesto al día. Quedarse en el kernel anterior hasta que se
actualice el controlador es una respuesta legítima.

## Suspensión y reanudación { #suspend-and-resume }

Ventanas corrompidas, un escritorio colgado o una pantalla en negro tras la
reanudación suele ser memoria de vídeo que no se preserva durante la
suspensión. El arreglo es el subpaquete de gestión de energía:

```bash
sudo dnf5 install xorg-x11-drv-nvidia-power
sudo systemctl enable nvidia-suspend.service nvidia-resume.service nvidia-hibernate.service
```

Ese paquete instala `/usr/lib/modprobe.d/nvidia-power-management.conf` con las
opciones pertinentes presentes pero comentadas. Para activarlas, anúlalo —
nunca edites archivos bajo `/usr/lib`:

```bash
sudo tee /etc/modprobe.d/nvidia-power-management.conf >/dev/null <<'EOF'
options nvidia NVreg_PreserveVideoMemoryAllocations=1
options nvidia NVreg_TemporaryFilePath=/var/tmp
EOF
```

La primera preserva el contenido completo de la memoria de vídeo durante la
suspensión. La segunda envía ese volcado a `/var/tmp` y no a `/tmp`, que en
Fedora es tmpfs — escribir en RAM toda la memoria de vídeo de una GPU frustra
el propósito y puede fallar directamente. Reinicia para aplicarlo.

## Variantes atómicas (Silverblue, Kinoite) { #atomic-variants-silverblue-kinoite }

El esquema coincide con el de la instalación clásica. Todos los pasos
mecánicos difieren.

Añade RPM Fusion y reinicia para que los repositorios existan — consulta
[Repositorios de terceros](../repositories/rpmfusion.md#on-atomic-desktops).

Superpón el controlador:

```bash
rpm-ostree install akmod-nvidia xorg-x11-drv-nvidia
# add xorg-x11-drv-nvidia-cuda too if you need nvidia-smi or CUDA
```

Establece los argumentos del kernel a mano. En la Fedora clásica el RPM lo hace
por ti con `grubby`; en ostree el paquete no puede modificar la configuración
de arranque, así que este paso es cosa tuya:

```bash
rpm-ostree kargs \
  --append=rd.driver.blacklist=nouveau,nova_core \
  --append=modprobe.blacklist=nouveau,nova_core
```

Después reinicia en el nuevo despliegue.

Lo que difiere del flujo de trabajo clásico:

- **El módulo se construye durante la transacción de superposición, no en el
  arranque.** `akmods.service` se niega a ejecutarse en un sistema ostree (su
  unidad lleva `ConditionPathExists=!/run/ostree-booted`). Por eso
  `rpm-ostree install akmod-nvidia` tarda varios minutos.
- **Cada actualización del kernel significa un nuevo despliegue**, con el
  módulo reconstruido como parte de su composición. La ventaja es que una
  compilación fallida te da un despliegue fallido en lugar de un arranque roto,
  y el despliegue anterior sigue en el menú de GRUB.
- **Las actualizaciones de versión mayor requieren volver a superponer los
  paquetes release** en la misma transacción que el rebase — consulta
  [Repositorios de terceros](../repositories/rpmfusion.md#on-atomic-desktops).
- **El Arranque Seguro es realmente incómodo.** La clave de firma tiene que
  estar disponible durante la composición, lo que significa empaquetarla en vez
  de dejarla en `/etc` — consulta
  [Arranque Seguro](../secure-boot.md#on-atomic-desktops).

### La ruta preconstruida { #the-prebuilt-route }

Universal Blue publica imágenes de Fedora Atomic —Bazzite, Bluefin, Aurora—
con variantes NVIDIA en las que el controlador ya viene construido dentro de la
imagen y firmado con la clave del proyecto. No se superpone nada y no se
compila nada en tu máquina; las actualizaciones del kernel llegan como una
imagen nueva con un módulo a juego ya dentro.

Aun así tienes que inscribir su clave de firma una vez, algo que esas imágenes
envuelven en `ujust enroll-secure-boot-key`. La contraseña la fija la imagen y
no tú — Bluefin documenta `universalblue`, y los hilos de la comunidad
mencionan `ublue-os` para otras imágenes. Consulta
[Arranque Seguro](../secure-boot.md#on-atomic-desktops) para la mecánica de la
inscripción.

El compromiso es el habitual de las imágenes preconstruidas: obtienes las
pruebas de integración de otra gente y ningún paso de compilación local, y
cedes el control sobre qué rama del controlador y qué paquetes ejecutas.

## Quitarlo y volver a nouveau { #removing-it-and-going-back-to-nouveau }

```bash
sudo dnf5 remove 'xorg-x11-drv-nvidia*'
sudo systemctl reboot
```

El scriptlet de desinstalación de RPM Fusion quita la lista negra de nouveau de
tus argumentos del kernel, así que la máquina vuelve con nouveau. Confírmalo
antes de reiniciar:

```bash
cat /proc/cmdline    # should no longer mention rd.driver.blacklist=nouveau
```

Si en su lugar instalaste desde negativo17, su secuencia de eliminación está en
[La ruta de negativo17](negativo17.md#switching-between-the-two).

> Otra vez: nada de `dnf remove '*nvidia*'`. Eso se lleva por delante
> `nvidia-gpu-firmware`, que nouveau y `nova_core` necesitan.

Tras el reinicio no debería haber nada de NVIDIA cargado:

```bash
lsmod | grep -E 'nvidia|nouveau'
```

Si alguna vez ejecutaste en esta máquina el instalador `.run` propio de NVIDIA,
sobrescribió bibliotecas de la distribución sin que RPM lo supiera y quitar el
paquete no deshará eso. RPM Fusion documenta un
[procedimiento de recuperación][rpmfusion-nvidia] para ese caso. No lo ejecutes
en ningún otro caso — borra bibliotecas del sistema.

## Resolución de problemas { #troubleshooting }

### ¿Por qué hay una pantalla en negro tras el primer reinicio? { #why-is-there-a-black-screen-after-the-first-reboot }

Recórrelo en orden. ¿Se construyó el módulo (`modinfo -F version nvidia` desde
un TTY o desde un arranque de rescate)?, ¿está activado el Arranque Seguro
(`mokutil --sb-state`)? y ¿se inscribió la clave (`sudo mokutil --test-key
/etc/pki/akmods/certs/public_key.der`)?

Un módulo que se compiló bien pero que es rechazado al cargarse es casi siempre
un [problema de firma](../secure-boot.md#troubleshooting):

```bash
sudo dmesg | grep -iE 'nvidia|lockdown|module verification'
```

[Recuperarse de una pantalla en negro](#recovering-from-a-black-screen) tiene
la secuencia completa.

### ¿Qué significa «NVIDIA kernel module missing. Falling back to nouveau»? { #what-does-nvidia-kernel-module-missing-falling-back-to-nouveau-mean }

Que `nvidia-fallback.service` está haciendo su trabajo. Tu escritorio funciona,
el controlador no. Consulta
[Recuperarse de una pantalla en negro](#recovering-from-a-black-screen) para la
reconstrucción.

### ¿Por qué la pantalla se queda en 1024x768? { #why-is-the-display-stuck-at-1024x768 }

El controlador de NVIDIA no está en uso. O bien recurrió a nouveau, en cuyo
caso consulta [la entrada anterior](#what-does-nvidia-kernel-module-missing-falling-back-to-nouveau-mean),
o bien `nomodeset` está en la línea de comandos del kernel:

```bash
cat /proc/cmdline
sudo grubby --update-kernel=ALL --remove-args='nomodeset'
```

### ¿Por qué dejó de cargarse el módulo tras una actualización del kernel? { #why-did-the-module-stop-loading-after-a-kernel-update }

La compilación falló o no se ha ejecutado. Consulta
[Convivir con las actualizaciones del kernel](#living-with-kernel-updates). Si
la rama del controlador todavía no soporta el kernel nuevo, espera a que el
controlador se actualice en lugar de forzar nada.

### ¿Debería añadir `nvidia-drm.modeset=1` a la línea de comandos del kernel? { #should-i-add-nvidia-drmmodeset1-to-the-kernel-command-line }

No. El módulo de RPM Fusion habilita el modesetting del kernel por omisión, y
RPM Fusion advierte de que no se ponga el parámetro a mano — interactúa mal con
el manejo del arranque temprano por `simpledrm` del kernel de Fedora. Mensajes
de foro y artículos de blog antiguos todavía te dicen que lo pongas; están
describiendo una configuración de hace varios años.

Desactivar el modesetting es un paso de depuración, y es reversible:

```bash
sudo grubby --update-kernel=ALL --args='nvidia-drm.modeset=0'
sudo grubby --update-kernel=ALL --remove-args='nvidia-drm.modeset=0'
```

### ¿Por qué no aparece la petición de la frase de paso de LUKS? { #why-doesnt-the-luks-passphrase-prompt-appear }

Con cifrado de disco completo y la tarjeta NVIDIA como única GPU, la petición
se dibuja antes de que el controlador se inicialice:

```bash
sudo grubby --update-kernel=ALL --args='plymouth.use-simpledrm=1'
```

### ¿Por qué está muerto el monitor externo en mi portátil? { #why-is-the-external-monitor-dead-on-my-laptop }

Comprueba primero si el puerto está siquiera cableado a la GPU de NVIDIA —
`sudo lspci -nnk` muestra qué GPU tiene qué controlador asociado. Después
consulta [Monitores externos](#external-monitors).

### ¿Por qué la suspensión y reanudación rompe la pantalla? { #why-does-suspend-and-resume-break-the-display }

Consulta [Suspensión y reanudación](#suspend-and-resume). Si sigue fallando con
la preservación de la memoria de vídeo habilitada, comprueba que `/var/tmp`
tenga sitio para el volcado.

### ¿Por qué `dnf autoremove` eliminó el controlador? { #why-did-dnf-autoremove-remove-the-driver }

Considera que `akmod-nvidia` es
[un paquete hoja](#keep-dnf-from-removing-it):

```bash
sudo dnf5 mark user akmod-nvidia
```

Después reinstálalo.

### ¿Cómo informo de un fallo? { #how-do-i-report-a-bug }

NVIDIA y RPM Fusion quieren los dos el mismo paquete de registros:

```bash
sudo nvidia-bug-report.sh
```

[index]: ../index.md
[rpmfusion-nvidia]: https://rpmfusion.org/Howto/NVIDIA
[rpmfusion-optimus]: https://rpmfusion.org/Howto/Optimus
[chips]: https://download.nvidia.com/XFree86/Linux-x86_64/615.71.09/README/supportedchips.html
[nvidia-unix]: https://www.nvidia.com/en-us/drivers/unix/
[nvk]: https://docs.mesa3d.org/drivers/nvk.html
[nouveau-pm]: https://nouveau.freedesktop.org/PowerManagement.html
