# COPR

[COPR][copr] es el servicio de compilación de Fedora. Cualquiera con una cuenta
de Fedora puede compilar paquetes ahí, y el resultado es un repositorio que
puedes habilitar con un solo comando.

## Por qué existe { #why-it-exists }

Reduce el coste de publicar un RPM hasta casi cero. Meter un paquete en Fedora
propiamente dicha implica una revisión, un patrocinador y un compromiso
continuado; COPR no pide nada de eso, así que es donde acaban las compilaciones
nocturnas, los backports personales, los forks parcheados y el software que
nadie piensa mantener a largo plazo.

Esa apertura es también el inconveniente. Funciona sobre infraestructura de
Fedora, que es el origen de casi toda la confusión al respecto: el alojamiento
es de Fedora, los paquetes no. Nada en COPR está revisado por Fedora, cubierto
por el QA de Fedora ni distribuido con las claves de firma de Fedora. Cada
proyecto firma con las suyas.

## Quién lo mantiene { #who-maintains-it }

El Proyecto Fedora opera el servicio. Cada proyecto lo mantiene quien lo creó,
sin ninguna política común; por eso la tabla de
[Repositorios de terceros](index.md) indica al propietario, y no al servicio,
como la parte en la que confías.

Eso hace de un proyecto de COPR una apuesta más estrecha que
[RPM Fusion](rpmfusion.md) o [negativo17](negativo17.md). Estos son
repositorios mantenidos y con un historial detrás; un proyecto de COPR suele
ser una sola persona, y puede quedar abandonado o ser eliminado sin previo
aviso. `dnf` muestra una advertencia en ese sentido la primera vez que
habilitas uno.

## Habilitar un proyecto { #enabling-a-project }

El comando `copr` está en `dnf5-plugins`:

```bash
sudo dnf install dnf5-plugins
sudo dnf copr enable owner/project
```

Consulta qué has habilitado, y revierte uno:

```bash
dnf copr list
sudo dnf copr disable owner/project
```

`disable` deja el repositorio configurado pero inactivo. `sudo dnf copr remove
owner/project` borra la configuración por completo. Ninguno de los dos elimina
los paquetes que hayas instalado desde él, que se quedan en el sistema sin nada
detrás.

## Antes de habilitar uno { #before-enabling-one }

Abre su página en COPR y comprueba tres cosas: cuándo compiló por última vez,
para qué versiones de Fedora compila y si sigue el branching de Fedora. Un
proyecto que no sigue el branching deja de producir compilaciones para tu
versión en cuanto actualizas de versión, y te quedas con paquetes que ningún
repositorio va a actualizar.

Comprueba primero si el paquete ya está en Fedora o en
[RPM Fusion](rpmfusion.md). COPR es adonde acudes cuando no lo está.

## Proyectos destacados { #notable-projects }

Proyectos documentados en otras páginas de este sitio. Confirmado en septiembre
de 2026; para qué versiones de Fedora compila cada uno está en su página de
COPR.

| Proyecto | Qué proporciona | Mantenedor | Sigue el branching |
| --- | --- | --- | --- |
| [`rhea/fedoratricks`][fedoratricks-copr] | [Fedora Tricks](../tooling/fedoratricks.md), una herramienta en Bash que habilita RPM Fusion, instala la pila multimedia y configura el controlador de NVIDIA | Rhea Gustavsson. La descripción del COPR indica que el paquete lo proporciona el servidor de Fedora Discord a sus miembros | Sí |
| [`@kernel-vanilla/fedora`][kernel-vanilla-copr] | Kernels upstream compilados igual que Fedora compila los suyos, a partir de la serie que ya usa tu versión. Uno de siete repositorios que cubren distintas series del kernel | Thorsten Leemhuis, desde 2012. No participa ninguno de los mantenedores del kernel de la propia Fedora | Sí |

[Fedora Tricks](../tooling/fedoratricks.md) cubre qué hace la herramienta y cómo usarla.

Los repositorios del kernel llevan dos condiciones que conviene conocer antes
de habilitar uno. Firmar un kernel vanilla para el Arranque Seguro UEFI
estándar no es posible actualmente, así que hay que desactivar el
[Arranque Seguro](../secure-boot.md#turning-it-off); y pasar un sistema en
funcionamiento a ellos requiere `--setopt=allow_vendor_change=1`, porque los
paquetes del kernel cambian de proveedor. La
[página del wiki][kernel-vanilla-wiki] de Fedora recoge los comandos actuales y
las diferencias entre los siete.


## Fuentes { #sources }

- [COPR][copr], y la [documentación de usuario de COPR][copr-docs] de Fedora
- Wiki de Fedora, [Kernel Vanilla Repositories][kernel-vanilla-wiki]

[copr]: https://copr.fedorainfracloud.org/
[copr-docs]: https://docs.pagure.org/copr.copr/user_documentation.html
[fedoratricks-copr]: https://copr.fedorainfracloud.org/coprs/rhea/fedoratricks/
[kernel-vanilla-copr]: https://copr.fedorainfracloud.org/coprs/g/kernel-vanilla/fedora/
[kernel-vanilla-wiki]: https://fedoraproject.org/wiki/Kernel_Vanilla_Repositories
