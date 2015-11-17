# Servidor DASH like

Instale os pré-requisitos (assumindo arch linux)

    $ yaourt -S opencv python2-numpy youtube-dl ffmpeg

## Preparação

Baixe o vídeo

    $ youtube-dl -f137 https://www.youtube.com/watch?v=Ezc4HdLGxg4 -o video.mp4

Rode o script que divide o vídeo em vários de 10sec e com duas codificações

    $ ./enc.sh

Rode o servidor

    $ python2 vserver.py

E então o cliente

    $ python2 cvclient.py
