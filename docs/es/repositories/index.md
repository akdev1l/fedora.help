# Repositorios de terceros

Casi todo lo que hay en este sitio viene de un repositorio que Fedora no
gestiona. Configúralos una vez; el resto de páginas dan por hecho que has
pasado antes por aquí.

| Repositorio | Qué contiene | Quién lo gestiona | Página |
| --- | --- | --- | --- |
| RPM Fusion | Los paquetes sujetos a patentes y no libres que Fedora excluye: el FFmpeg completo, los plugins restringidos de GStreamer, el controlador de NVIDIA, Steam | Un grupo de voluntarios, en su mayoría empaquetadores de Fedora | [RPM Fusion](rpmfusion.md) |
| negativo17 | El mismo controlador de NVIDIA que RPM Fusion, empaquetado de otra forma, más CUDA y otro software relacionado con el hardware | Simone Caronni, empaquetador de Fedora, en su propia infraestructura | [negativo17](negativo17.md) |
| Terra | Unos tres mil paquetes que Fedora no incluye, con versiones rolling en lugar de congeladas: software de escritorio más reciente, herramientas de shell, compositores Wayland | Fyra Labs, el equipo detrás de Ultramarine Linux | [Terra](terra.md) |
| Flathub | Aplicaciones de escritorio en sandbox, incluidas la mayoría de las privativas: Steam, Discord, Spotify, Chrome | Una comunidad de base; cada aplicación viene de quien la publica | [Flathub](flathub.md) |
| COPR | Lo que cada persona haya decidido compilar. Un proyecto por propietario, sin política común | Quien compila cada proyecto. Fedora gestiona el servicio, no el contenido | [COPR](copr.md) |

La mayoría de la gente necesita RPM Fusion y nada más. negativo17 es una
alternativa para el controlador de NVIDIA, y los dos no se pueden mezclar para
eso. Terra añade software que ninguno de los dos incluye, y sus canales de
gráficos y multimedia son opcionales por la misma razón. Flathub es un tipo de
fuente distinto —aplicaciones en sandbox en lugar de paquetes del sistema— y
Fedora ya incluye una versión filtrada de él. COPR es adonde acudes para un
paquete que no existe en ninguno de ellos.

## A qué estás accediendo { #what-you-are-agreeing-to }

Un repositorio de terceros queda fuera del límite de confianza de Fedora. Tiene
sus propios mantenedores, su propio sistema de compilación y sus propias claves
de firma, y `dnf` ejecuta sus scriptlets de paquete como root exactamente igual
que los de un paquete de Fedora. Habilitar uno es una decisión sobre en quién
confías para ejecutar código en tu máquina.

Conviene conocer dos consecuencias más antes de empezar:

- **Fedora no da soporte a sistemas con estos repositorios habilitados.** Los
  informes de error contra paquetes de Fedora que hayan sido sustituidos por
  versiones de terceros se cerrarán.
- **Las actualizaciones de versión se complican.** Los paquetes «release» se
  versionan para cada versión de Fedora, y cualquier paquete sustituido tiene
  que resolverse contra la nueva. Una actualización que habría salido limpia
  puede atascarse en un paquete de terceros que aún no se ha recompilado.

Tanto RPM Fusion como negativo17 son muy usados y están bien mantenidos. Eso es
un juicio sobre su trayectoria y no cambia el modelo de confianza.

## No los mezcles para el mismo software { #do-not-mix-them-for-the-same-software }

RPM Fusion y negativo17 empaquetan el mismo controlador de NVIDIA con nombres
distintos y con propiedad de archivos solapada, y dnf instalará piezas de ambos
sin quejarse. Elige una vía y quédate en ella —
[Controladores de NVIDIA](../nvidia/index.md) los compara y tiene el
procedimiento para cambiar si ya tienes instalado el que no era.

Tener ambos repositorios habilitados está bien en sí mismo, siempre que cada
pieza concreta de software venga de solo uno de ellos.
