# Terra

[Terra][terra] es un repositorio comunitario para Fedora gestionado por
[Fyra Labs][fyra], el equipo detrás de Ultramarine Linux. Contiene unos tres
mil paquetes que Fedora no distribuye, y es rolling: los paquetes siguen las
publicaciones de upstream en lugar de quedar congelados durante toda la vida
de una versión de Fedora.

## Por qué existe { #why-it-exists }

El proceso de empaquetado de Fedora es deliberadamente lento. Un paquete
necesita una revisión, un patrocinador y un mantenedor dispuesto a mantenerlo
compilando durante años, y las versiones estables dejan las versiones
congeladas. Ese es el compromiso correcto para una distribución y el
equivocado para software que se mueve cada semana.

Terra adopta la posición contraria. Las actualizaciones se automatizan desde
upstream mediante sus propias herramientas, todo el conjunto de paquetes vive
en un único repositorio público y cada compilación se ejecuta en un CI
público. Sus mantenedores son explícitos sobre cuál es la diferencia que les
importa: llaman a [RPM Fusion](rpmfusion.md) «un gran repositorio» y dicen que
lo que Terra aporta es transparencia y un modelo rolling, más que una posición
legal distinta.

En la práctica es donde buscas software de escritorio que es joven, que se
mueve rápido o que nadie ha empaquetado para Fedora: emuladores de terminal,
editores, herramientas para el intérprete de comandos, compositores de Wayland
y similares. `ghostty`, `zed`, `zen-browser`, `cursor`, `starship`, `zellij`,
`lact` y `topgrade` están todos ahí.

## Quién lo mantiene { #who-maintains-it }

Fyra Labs, una empresa más que un grupo de voluntarios, algo poco habitual
entre los repositorios de esta página. El empaquetado está abierto a
colaboradores a través de la organización `terrapkg` en GitHub, y las
contribuciones se revisan, pero la infraestructura no la gestiona la
comunidad: Terra afirma que solo empleados de confianza de Fyra Labs tienen
acceso a los sistemas de compilación y a las claves de firma.

La cadena de compilación es obra suya, más que la de Fedora. Los paquetes se
compilan con **Andaman**, una cadena de compilación en Rust que maneja Mock y
`rpmbuild`; se entregan mediante **Subatomic**, que genera los metadatos del
repositorio; y se localizan a través de **Tetsudou**, un generador de
metalinks que apunta `dnf` a una réplica. Los specs y los scripts de
actualización viven en un monorepo, y GitHub Actions compila en cada push.

Seis distribuciones derivadas lo usan: Ultramarine, Bazzite, Nobara, RakuOS,
Zirconium y Armada.

## Cómo activarlo { #enabling-it }

```bash
sudo dnf install --nogpgcheck --repofrompath 'terra,https://repos.fyralabs.com/terra$releasever' terra-release terra-gpg-keys
```

`--nogpgcheck` se aplica a esa única transacción, que es la forma en que la
clave de firma llega al sistema en primer lugar: `terra-gpg-keys` la contiene,
y todo lo posterior se comprueba contra ella.

Terra publica para Fedora 42 hasta 45.

### En escritorios atómicos { #on-atomic-desktops }

```bash
curl -fsSL https://raw.githubusercontent.com/terrapkg/packages/f$(rpm --eval '%{fedora}')/anda/terra/release/terra.repo | pkexec tee /etc/yum.repos.d/terra.repo
rpm-ostree install terra-release terra-gpg-keys
```

En secureblue, `run0` sustituye a `pkexec`.

### Subrepositorios opcionales { #optional-sub-repositories }

El repositorio base es deliberadamente conservador. Se distribuyen otros
cuatro como paquetes separados, y cada uno activa un canal propio:

```bash
sudo dnf install terra-release-extras
sudo dnf install terra-release-mesa
sudo dnf install terra-release-nvidia
sudo dnf install terra-release-multimedia
```

`terra-release-multimedia` necesita Fedora 43 o posterior.

## Solapamiento con RPM Fusion { #overlap-with-rpm-fusion }

Los canales `mesa`, `nvidia` y `multimedia` cubren el mismo terreno que
[RPM Fusion](rpmfusion.md), y se aplica la misma advertencia que con
[negativo17](negativo17.md): un controlador gráfico o una pila multimedia
deberían venir de un solo repositorio, no de dos compitiendo por los mismos
nombres de archivo. El repositorio base de Terra no se solapa, así que
activarlo junto a RPM Fusion no da problemas; los subrepositorios son donde
hay que elegir.

## Fuentes { #sources }

- [Terra][terra] y su [documentación][terra-docs], incluyendo el
  [resumen de la infraestructura][terra-infra] y las
  [preguntas frecuentes][terra-faq]
- Los comandos de activación están citados de las propias
  [instrucciones de instalación][terra-install] de Terra
- Los nombres de los paquetes y las versiones de Fedora publicadas se
  comprobaron contra `https://repos.fyralabs.com/terra44` en septiembre de
  2026

[terra]: https://terrapkg.com/
[terra-docs]: https://docs.terrapkg.com/
[terra-infra]: https://docs.terrapkg.com/general/infrastructure
[terra-faq]: https://docs.terrapkg.com/general/faq
[terra-install]: https://docs.terrapkg.com/usage/installing
[fyra]: https://fyralabs.com/
