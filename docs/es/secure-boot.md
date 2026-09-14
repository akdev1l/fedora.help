# Arranque Seguro

El Arranque Seguro es el firmware comprobando una firma antes de ejecutar
nada. En Fedora funciona de serie, y sigue funcionando hasta que instalas un
módulo del kernel que Fedora no ha firmado — [el controlador de
NVIDIA](nvidia/index.md), VirtualBox, algunos controladores de Wi-Fi y de
panel táctil, cualquier cosa construida por akmods o DKMS. Entonces el kernel
se niega a cargar el módulo.

Esa negativa es silenciosa. No hay ningún error en la salida de la
instalación, y el síntoma llega un reinicio más tarde: una pantalla en negro,
o un escritorio funcionando con un controlador de reserva a la resolución
equivocada. Esta página cubre las dos salidas.

## Comprueba qué tienes { #check-what-you-have }

```bash
mokutil --sb-state
```

`SecureBoot enabled` significa que todo lo que sigue te aplica.
`SecureBoot disabled` significa que los módulos sin firmar se cargan sin
problema y puedes saltarte esta página, al coste descrito en
[Desactivarlo](#turning-it-off).

## Inscribir tu propia clave { #enrolling-your-own-key }

El enfoque que documentan Fedora y RPM Fusion: generar un par de claves,
inscribir la mitad pública en la lista de Machine Owner Key del firmware, y
dejar que
[akmods](nvidia/index.md#what-akmods-actually-does-and-why-you-must-wait)
firme con ella cada módulo que construya. Haz esto **antes** de instalar un
controlador — hacerlo después funciona, pero te llevas un mal arranque de por
medio.

Esto reproduce el [Secure Boot HowTo][rpmfusion-secureboot] de RPM Fusion.

```bash
sudo dnf install akmods mokutil openssl
```

Genera el par de claves. `-a` acepta los valores por defecto en lugar de irte
preguntando por la configuración de un certificado:

```bash
sudo kmodgenca -a
```

Eso escribe el certificado en `/etc/pki/akmods/certs/` y la clave privada en
`/etc/pki/akmods/private/`. akmods genera esta clave por su cuenta en su
primera ejecución si te saltas el paso; hacerlo a propósito significa que
sabes dónde está.

> La clave privada vive sin cifrar en tu sistema de archivos raíz. Cualquier
> cosa que pueda leerla puede firmar un módulo del kernel en el que tu máquina
> confiará. Si el disco no está cifrado, ese es el intercambio que estás
> haciendo. RPM Fusion trata el cifrado de disco completo como un requisito
> aquí.

Pon la clave pública en cola para su inscripción:

```bash
sudo mokutil --import /etc/pki/akmods/certs/public_key.der
```

`mokutil` te pide establecer una contraseña de un solo uso. La escribes en el
siguiente arranque, así que elige algo corto y sin ambigüedades.

```bash
sudo systemctl reboot
```

El siguiente arranque se detiene en una pantalla azul de **MOK Management**
antes de que el gestor de arranque ceda el control. Esto no es un error. Elige
**Enroll MOK** → **Continue** → **Yes**, y después introduce la contraseña que
acabas de establecer.

> El teclado del MOK Manager está fijado a QWERTY de EE. UU. sea cual sea tu
> distribución de teclado. En AZERTY, Dvorak o cualquier otra, la contraseña
> que escribes no es la contraseña que crees estar escribiendo. Elige en
> consecuencia.

El sistema se reinicia otra vez. Confirma que la clave ha surtido efecto:

```bash
sudo mokutil --test-key /etc/pki/akmods/certs/public_key.der
```

A partir de aquí akmods firma con esa clave cada módulo que construye, para
este kernel y para todos los futuros.

### Si usas DKMS en su lugar { #if-you-use-dkms-instead }

DKMS firma con su propia clave por sistema en `/var/lib/dkms/mok.pub`,
inscrita con el mismo paso de `mokutil --import`. El resto del proceso es
idéntico. [negativo17](repositories/negativo17.md) ofrece DKMS como
alternativa a akmods; RPM Fusion usa únicamente akmods.

## Desactivarlo { #turning-it-off }

Desactiva el Arranque Seguro en la configuración de tu firmware y el módulo
sin firmar se carga. A lo que renuncias es a la verificación de la cadena de
arranque por parte del firmware: el gestor de arranque y el kernel ya no se
comprueban contra una firma antes de ejecutarse, así que un compromiso que
llegue a tu ESP o a `/boot` puede persistir entre reinstalaciones sin ser
detectado.

Comprueba dos cosas primero. Algunos sistemas atan BitLocker o una política de
TPM al estado del Arranque Seguro, lo que importa en una máquina con arranque
dual. Y algunos firmwares esconden la opción hasta que estableces una
contraseña de supervisor.

## En escritorios atómicos { #on-atomic-desktops }

[Silverblue, Kinoite y los
demás](nvidia/index.md#atomic-variants-silverblue-kinoite) construyen los
módulos mientras componen un despliegue, lo que significa que la clave de
firma tiene que estar disponible durante la composición — tiene que ir
empaquetada en lugar de estar en `/etc`. RPM Fusion apunta al repositorio de
terceros [silverblue-akmods-keys][sbkeys] para esto. No ha tenido commits
desde 2023, así que verifícalo contra tu versión antes de confiar en él.

Las [imágenes precompiladas](nvidia/index.md#the-prebuilt-route) esquivan el
problema distribuyendo módulos ya firmados con la clave del proyecto; esa
clave la inscribes una vez. Las imágenes de Universal Blue lo envuelven en
`ujust enroll-secure-boot-key`, donde la contraseña la establece la imagen en
vez de establecerla tú.

## Qué lo rompe más adelante { #what-breaks-it-later }

- **Las actualizaciones de firmware pueden borrar las claves MOK inscritas.**
  Si un módulo deja de cargarse después de una actualización de BIOS o UEFI,
  vuelve a ejecutar el paso de `mokutil --import` e inscríbela de nuevo.
- **Esta clave firma módulos, no kernels.** Un kernel compilado por uno mismo
  es un problema aparte con una solución aparte.
- **Un intento por reinicio.** Equivocarse con la contraseña de MOK significa
  reiniciar y empezar de nuevo el diálogo de inscripción.

## Resolución de problemas { #troubleshooting }

**El módulo se ha construido pero no se carga.** Confirma que el módulo existe
para el kernel en ejecución, y después comprueba el estado de la firma:

```bash
sudo dmesg | grep -i 'Loading of unsigned module\|module verification failed'
mokutil --test-key /etc/pki/akmods/certs/public_key.der
```

**Pantalla en negro después de instalar un controlador.** Arranca el kernel
anterior desde el menú de GRUB, o añade `nomodeset` a la línea de comandos del
kernel desde el editor de GRUB, y después trabaja desde una TTY.
[Controladores de NVIDIA](nvidia/index.md#recovering-from-a-black-screen)
tiene la secuencia de recuperación completa para ese caso.

**`mokutil --test-key` dice que la clave no está inscrita, pero la
inscribiste.** O bien la contraseña del MOK Manager se escribió mal — mira la
nota sobre QWERTY más arriba — o una actualización de firmware borró el
almacén de claves.

## Fuentes { #sources }

- RPM Fusion, [Secure Boot HowTo][rpmfusion-secureboot]
- Documentación de Fedora, [firmar módulos del kernel][fedora-signing]
- [silverblue-akmods-keys][sbkeys], para el caso atómico

[rpmfusion-secureboot]: https://rpmfusion.org/Howto/Secure%20Boot
[fedora-signing]: https://docs.fedoraproject.org/en-US/quick-docs/mok-enrollment/
[sbkeys]: https://github.com/CheariX/silverblue-akmods-keys
