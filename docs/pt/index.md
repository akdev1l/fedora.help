# {{ brand }}: Torne o Fedora Seu

{{ brandlink() }} é um guia comunitário não oficial sobre o software que o
Fedora não pode distribuir: codecs multimídia, o driver da NVIDIA, repositórios
de terceiros como RPM Fusion e Flathub, e os aplicativos proprietários de que
quase todo desktop acaba precisando. Mais as correções que uma instalação
recém-feita costuma exigir.

## Por que este site existe

O Fedora distribui apenas software livre e de código aberto, conforme a
[missão do Projeto Fedora][mission]. A posição jurídica da Red Hat também
descarta código sujeito a patentes ou com restrições de redistribuição. Por
isso, várias coisas que usuários de desktop consideram garantidas não podem
ficar dentro do Fedora:

- Codecs multimídia patenteados (H.264, HEVC, AAC e afins)
- O driver proprietário da NVIDIA
- Firmware proprietário e blobs de habilitação de hardware
- Aplicativos de código fechado: Steam, Discord, Chrome, Spotify

Isso está fora do escopo do projeto, então a documentação precisa viver em
outro lugar.

## Para quem isto foi escrito

Usuários de Fedora no desktop que querem as partes proprietárias funcionando e
que querem entender o que instalaram depois que estiver pronto.

Os guias pressupõem um leitor que:

- sabe abrir um terminal e trabalhar em um prompt de comando
- não tem medo de executar comandos, inclusive como root
- lê um comando antes de colá-lo
- quer acumular o próprio conhecimento sobre o Fedora pelo caminho

Eles têm como alvo as versões do Fedora atualmente suportadas em x86_64 —
Workstation e os spins de desktop. Variantes atômicas (Silverblue, Kinoite)
são destacadas onde os passos diferem.

Nada disso é obrigatório. Uma instalação padrão do Fedora está completa e é
suportada como vem; cada página daqui sai desse território.

## Sem vínculo com o Projeto Fedora

{{ brandlink() }} é um projeto comunitário independente. Não é produzido,
endossado nem revisado pelo Projeto Fedora ou pela Red Hat, e "Fedora" é uma
marca registrada da Red Hat, Inc. Para a documentação oficial, consulte
[docs.fedoraproject.org][docs].

[mission]: https://docs.fedoraproject.org/pt/project/
[docs]: https://docs.fedoraproject.org/
