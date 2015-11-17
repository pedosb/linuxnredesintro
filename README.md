Material: https://lapsufpa.wordpress.com/material-jtl2015/

# Mensagem dentro de uma música

Informações em: https://goo.gl/b0CetO

## Preparação

Instale os pré-requisitos (assumindo arch linux)

    $ yaourt -S sox

Prepare os arquivos a serem usados, pegue uma música em um formato qualquer
(nos comandos a seguir o nome dela é assumido ``musica_entrada``), pegue também
um gif qualquer e salve-o com o nome ``image.gif``.

Codifique a músida no formato compatível

    $ sox musica_entrada -b 16 music.wav

## Codificando e decodificando

Rode o códificador que vai colocar o arquivo ``image.gif`` dentro da música
``music.wav`` e escrever o arquivo codificado em ``music_encoded.wav``

    $ python encode.py

Rode o código que vai decodificar a mensagem no arquivo ``music_encoded.wav`` e o arquivo gif salvando-o em um arquivo ``out.gif``

    $ python decode.py

# Servidor DASH like

## Preparação

Instale os pré-requisitos (assumindo arch linux)

    $ yaourt -S opencv python2-numpy youtube-dl ffmpeg

Baixe o vídeo

    $ youtube-dl -f137 https://www.youtube.com/watch?v=Ezc4HdLGxg4 -o video.mp4

Rode o script que divide o vídeo em vários de 10sec e com duas codificações

    $ ./enc.sh

## Servidor e cliente

Rode o servidor

    $ python2 vserver.py

E então o cliente

    $ python2 cvclient.py
