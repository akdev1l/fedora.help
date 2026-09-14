# Herramientas

El resto de este sitio está escrito como pasos manuales. Lees un comando,
decides si quieres lo que hace y lo ejecutas. Algunos proyectos, en cambio,
empaquetan ese mismo trabajo de posinstalación como un programa: activar
[los repositorios de terceros](../repositories/index.md), instalar
[los códecs](../multimedia/index.md), configurar
[el controlador de NVIDIA](../nvidia/index.md), escribir las opciones de
modprobe habituales, todo en una sola ejecución.

Esta sección cataloga esas herramientas, para que puedas decidir si usar
alguna en lugar de recorrer las páginas manuales.

**Todo esto es de terceros.** Ninguna de estas herramientas está producida,
respaldada ni revisada por el Proyecto Fedora, y ninguna la mantiene este
sitio. Cada página describe qué hace la herramienta en la versión indicada, en
qué puntos su trabajo se solapa con las páginas de aquí, y qué asumes al
ejecutarla. La posición habitual del sitio se aplica a la herramienta igual
que a cualquier comando de cualquier otra página: entiende lo que cuesta antes
de ejecutarlo.

Cada página se basa en el código fuente de la herramienta. Cuando el código
fuente y la documentación no coinciden, se indica.

## Las herramientas { #the-tools }

- [Fedora Tricks](fedoratricks.md) — una herramienta de línea de comandos en
  Bash que activa RPM Fusion, instala la pila multimedia y configura el
  controlador de NVIDIA. Se distribuye como un RPM desde un
  [COPR](../repositories/copr.md).
