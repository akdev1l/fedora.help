# Flathub

[Flathub][flathub] es donde se publica como Flatpaks la mayor parte de las
aplicaciones de escritorio de Linux. Queda fuera de la temática del resto de
esta página: un Flatpak lleva su propio runtime y sus propias bibliotecas, se
instala por usuario o para todo el sistema sin tocar los paquetes del sistema
anfitrión, y se ejecuta en sandbox. Nada de lo que hay en Flathub puede entrar
en conflicto con un RPM.

Fedora ya incluye un remoto de Flathub, pero filtrado, y el filtro es la razón
por la que la mayoría de la gente acaba aquí.

## Por qué existe { #why-it-exists }

Empaquetar una aplicación de escritorio una vez por distribución y por versión
es un trabajo que nadie quiere repetir. Flatpak permite que un upstream
distribuya una única compilación que funciona en todas partes, contra un
runtime que él mismo fija, de modo que una aplicación puede usar un toolkit más
reciente que el que trae el sistema anfitrión. Flathub es la tienda que
distribuye esas compilaciones.

Para este sitio importa porque es la respuesta práctica para buena parte del
software privativo de escritorio que Fedora no puede distribuir. Steam,
Discord, Spotify, Chrome y Zoom están todos ahí. Es también la vía que
recomienda [la guía de multimedia](../multimedia/index.md#flatpak-apps) para
gestionar los códecs en los [escritorios atómicos](../multimedia/atomic.md),
donde superponer paquetes en el sistema anfitrión cuesta un reinicio cada vez.

## Quién lo mantiene { #who-maintains-it }

Flathub se describe a sí mismo como una comunidad de base de código abierto más
que como un proyecto dirigido por una fundación, con infraestructura donada por
varios patrocinadores. Las aplicaciones llegan por dos vías: desarrolladores
upstream que publican su propio software, y voluntarios que empaquetan el de
otra gente. La distinción se ve: una aplicación cuyo publicador ha demostrado
que controla el proyecto upstream lleva un distintivo de **verificación** en su
página de Flathub.

Ese distintivo habla de la procedencia. No implica que se haya revisado nada.
Ni Flathub ni Fedora auditan lo que hace una aplicación una vez instalada. Lo
que la limita es el sandbox, y cada aplicación declara sus propios permisos,
así que un Flatpak que pide todo el sistema de archivos lo obtiene. Flathub
muestra esos permisos en la página de cada aplicación antes de que la instales.

## Qué incluye Fedora { #what-fedora-ships }

Fedora preconfigura el remoto `flathub`, filtrado hasta dejar una lista corta.
Los propios metadatos del remoto lo delatan:

```bash
flatpak remotes --columns=name,title
```

Lo que informa es **Fedora Flathub Selection** (la selección de Flathub de
Fedora), no Flathub. El filtro está en
`/usr/share/flatpak/fedora-flathub.filter`, y deniega por defecto con un puñado
de excepciones: los runtimes de freedesktop, más una lista corta de
aplicaciones: Bitwarden, Postman, Teams, Minecraft y Skype en el momento de
escribir esto. Todo lo demás de Flathub es invisible para `flatpak search` y
para GNOME Software mientras el filtro siga ahí.

El filtro se mantiene de forma abierta, en
[pagure.io/fedora-flathub-filter][filter].

## Habilitar el repositorio completo { #enabling-the-full-repository }

```bash
sudo flatpak remote-modify --no-filter flathub
```

Eso retira el filtro de Fedora y deja el remoto apuntando adonde ya apuntaba.
GNOME Software ofrece lo mismo como un interruptor de «Repositorios de
terceros» en su pantalla de primer arranque y en sus ajustes.

Si el remoto no está en absoluto, añádelo:

```bash
flatpak remote-add --if-not-exists flathub \
  https://dl.flathub.org/repo/flathub.flatpakrepo
```

Luego comprueba lo que tienes:

```bash
flatpak remotes --columns=name,title,filter
```

## La posición de confianza { #the-trust-position }

El riesgo de Flathub tiene una forma distinta del de los repositorios
anteriores. No instala nada en `/usr`, no puede sustituir un paquete de Fedora,
y desinstalar una aplicación la elimina por completo. Aquí confías en cada
publicador por separado, y en que el sandbox contenga aquello que ese
publicador haya distribuido.

Aplicación por aplicación, entonces: prefiere publicadores verificados, lee los
permisos en la página de Flathub, y recuerda que un Flatpak que pide
`filesystem=host` ha renunciado a casi todo aquello para lo que servía el
sandbox.

## Fuentes { #sources }

- [Flathub][flathub], y sus listados de permisos por aplicación
- [fedora-flathub-filter][filter], el filtro que incluye Fedora
- El archivo del filtro en una instalación de Fedora,
  `/usr/share/flatpak/fedora-flathub.filter`

[flathub]: https://flathub.org/
[filter]: https://pagure.io/fedora-flathub-filter
