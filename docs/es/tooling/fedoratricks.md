# Fedora Tricks

<div class="facts" markdown>

| | |
| --- | --- |
| Página | [github.com/RheaAyase/fedoratricks][fedoratricks] |
| Mantenedor | Rhea Gustavsson, con otros tres colaboradores |
| Forma | Bash, se ejecuta desde una terminal — sin TUI, sin GUI |
| Distribución | RPM desde el [COPR rhea/fedoratricks][fedoratricks-copr] |
| Licencia | MIT |
| Versión | 0.3-1, publicada el 16 de julio de 2026 |
| Compila para | Fedora 43, 44, 45 y Rawhide, x86_64 y aarch64 |

</div>

## Qué es { #what-it-is }

`fedoratricks` es un conjunto de módulos de Bash detrás de un único comando.
Salió del servidor de Fedora Discord — la propia descripción del COPR dice que
el paquete «lo proporciona el servidor de Fedora Discord a sus miembros para
ayudar con problemas de “soporte”» — y su objetivo declarado es explicar cada
paso mientras lo ejecuta. Imprime cada comando que ejecuta antes de ejecutarlo.

El desarrollo empezó en junio de 2026 y las tres versiones etiquetadas salieron
a lo largo de seis semanas. A septiembre de 2026 el último commit es del 16 de
julio, hay dos issues abiertas sin respuesta y el número de versión sigue
siendo 0.x.

## Qué automatiza { #what-it-automates }

En 0.3 hay cuatro comandos alcanzables: `rpmfusion`, `multimedia`, `nvidia` y
`logs`.

| Comando | Qué hace | Equivalente manual |
| --- | --- | --- |
| `rpmfusion install` | Instala los paquetes release free y nonfree de la versión que informa `rpm -E %fedora`, y después activa los cuatro repositorios de forma explícita | [Repositorios de terceros](../repositories/index.md) |
| `rpmfusion remove` | Elimina los dos paquetes release. El repositorio tainted no se toca en ninguno de los dos sentidos | |
| `multimedia install` | Mete el FFmpeg de RPM Fusion en lugar de `ffmpeg-free` e instala el grupo `multimedia`, ofreciendo ejecutar antes el paso de `rpmfusion` si faltan los repositorios | [Multimedia y códecs](../multimedia/index.md) |
| `multimedia install --with-optional` | Añade extras de códecs, después lee la GPU de `lspci` y añade el controlador VA-API correspondiente | |
| `multimedia install --config` | Solo Intel. Escribe `/etc/modprobe.d/intel-fedoratricks.conf` con `enable_guc` y `enable_fbc=1`, y después reconstruye el initramfs | |
| `nvidia install` | Elige una rama del controlador a partir del nombre comercial de la tarjeta, instala `akmod-nvidia` y el paquete de CUDA correspondiente, y activa `nvidia-persistenced` | [Controladores de NVIDIA](../nvidia/index.md) |
| `nvidia install --config` | Escribe `/etc/modprobe.d/nvidia-fedoratricks.conf` con las opciones de gestión de energía y de Resizable BAR, activa los servicios de suspensión y fuerza los módulos dentro del initramfs | |
| `logs` | Recopila la salida del journal, de `dmesg` y de `inxi` para una solicitud de soporte | — |

Los dos comandos `install` tienen su `remove` correspondiente.

## Cómo ejecutarlo { #how-to-run-it }

El COPR es un repositorio personal, bajo el mismo modelo de confianza que
cualquier cosa de [Repositorios de terceros](../repositories/copr.md).

```bash
sudo dnf copr enable rhea/fedoratricks
```

```bash
sudo dnf install fedoratricks
```

Después, **como tu usuario normal**:

```bash
fedoratricks rpmfusion install
```

```bash
fedoratricks multimedia install --with-optional
```

```bash
fedoratricks nvidia install --config
```

Ejecutarlo bajo `sudo` falla a propósito — el punto de entrada termina si su
UID efectivo es 0, y escala los comandos uno a uno con `sudo` a medida que
llega a ellos. Tanto el README como la referencia de comandos incluida dan sus
ejemplos como `sudo fedoratricks ...`, que ya no funciona.

Todos los comandos aceptan `-h`, y `man fedoratricks` se instala con el
paquete. `install` y `remove` son las dos acciones que acepta cada comando
modificador; sin acción imprime la ayuda y termina con un código distinto de
cero.

## Contrapartidas { #trade-offs }

**Escala a root.** No se ejecuta entero como root, lo que limita el radio de
impacto, e imprime cada comando antes de ejecutarlo — más visible que un
instalador típico de curl a shell. Sigue siendo un programa con permisos de
`sudo` haciendo cambios de paquetes y de configuración del kernel en tu
máquina, desde un COPR
[fuera de la frontera de confianza de Fedora](../repositories/index.md#what-you-are-agreeing-to),
en la versión 0.3.

**La salida va a un registro, no a tu terminal.** La salida de los comandos se
redirige por defecto a `/var/log/fedoratricks`, con
`~/.local/share/fedoratricks/fedoratricks.log` como alternativa. Ves las líneas
de comando y un resumen de tareas; no ves pasar la lista de transacción de dnf,
que es el momento en el que normalmente detectarías una eliminación inesperada
con `--allowerasing`. Si tiene que crear el archivo de registro, lo crea con
modo 666 — escribible por cualquiera.

**Toma las decisiones por ti.** Los comandos que imprime se parecen a los que
usan las páginas manuales de aquí. Lo que decide: qué paquetes entran en el
conjunto opcional, si suprimir las dependencias débiles,
[qué rama de NVIDIA quiere tu tarjeta](../nvidia/index.md#identify-your-gpu-and-pick-a-branch),
qué opciones de modprobe merece la pena poner. Si algo se rompe más adelante
— una actualización de versión atascada en un paquete sustituido, un
controlador que carga pero no gobierna la tarjeta — estarás depurando
decisiones que no tomaste. Los comandos impresos y el registro te dan una forma
de volver a ellas.

**Deshacer viene incorporado, y es parcial.** Cada tarea modificadora registra
un deshacer junto a su acción. Si una tarea falla a mitad de ejecución, la
herramienta deshace en orden inverso, y para los pasos de dnf captura antes el
ID de la transacción y revierte con `dnf history undo -y`. Tras una ejecución
correcta, `remove` revierte cada módulo: `nvidia remove` saca `akmod-nvidia*` y
`xorg-x11-drv-nvidia*`, borra los dos archivos de configuración y reconstruye
el initramfs; `multimedia remove` reinstala `ffmpeg-free` con
`--disablerepo="rpmfusion*"`; `rpmfusion remove` elimina los paquetes release.
Lo que no vuelve es el estado que tenías antes — los paquetes que
`--allowerasing` eliminó a la entrada no se reinstalan a la salida, y
`rpmfusion remove` deja cualquier paquete de RPM Fusion que hayas instalado por
el camino todavía en el sistema y sin repositorio detrás.

**Sigue tu versión de Fedora.** El número de versión sale de `rpm -E %fedora`
en tiempo de ejecución, así que la misma versión de la herramienta funciona a
través de las actualizaciones; el COPR sigue las ramas de Fedora y ahora mismo
compila para 43, 44, 45 y Rawhide. La correspondencia de ramas de NVIDIA es la
excepción.

**No sirve para escritorios atómicos.** Silverblue, Kinoite y las demás
[variantes de rpm-ostree](../repositories/rpmfusion.md#on-atomic-desktops) se
detectan y se rechazan de plano. No hay ninguna ruta con `rpm-ostree`.

## Fuentes { #sources }

Comprobado en septiembre de 2026. La documentación propia de la herramienta,
que manda donde ella y esta página no coincidan:

- [fedoratricks en GitHub][fedoratricks] — el código fuente, el README y las
  versiones etiquetadas
- La [referencia de comandos][fedoratricks-docs] y la
  [guía de desarrollo][fedoratricks-dev] incluidas, que documenta el sistema de
  tareas y de deshacer
- El [COPR rhea/fedoratricks][fedoratricks-copr] — los chroots de compilación,
  las versiones y la descripción del proyecto

El comportamiento descrito aquí se ha leído de `fedoratricks.sh` y de los
archivos bajo `commands/` en la etiqueta `0.3-1`. La herramienta no se ha
ejecutado de principio a fin en una máquina de pruebas.

[fedoratricks]: https://github.com/RheaAyase/fedoratricks
[fedoratricks-copr]: https://copr.fedorainfracloud.org/coprs/rhea/fedoratricks/
[fedoratricks-docs]: https://github.com/RheaAyase/fedoratricks/blob/main/docs/docs.md
[fedoratricks-dev]: https://github.com/RheaAyase/fedoratricks/blob/main/docs/developer.md
