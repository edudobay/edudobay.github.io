---
layout: post
title:  Segmentation fault no Bash
date:   2010-02-12 23:24:44 +0000
categories: programming
tags:   bash, shell
---
Troquei o Ubuntu pelo ArchLinux, salvando toda minha pasta home para continuar usando no novo sistema. Instalei tudo direitinho, criei um usuário e, quando fui substituir a home dele pela antiga, o usuário não logava. Não dava pra ver nenhum erro porque ele limpava a tela e voltava pro login após o erro; entrei como root e fui logar via `su`. O resultado: *segmentation fault*. Mas que diabos? Não imaginava nada que pudesse causar isso. Então deixei a pasta vazia e fui copiando as coisas aos poucos.

De repente fui abrir outra aba no terminal e vi que ela fechava sozinha, e de fato o bash tinha voltado a dar segfault. Tentei procurar no Google, nenhuma solução concreta. Num fórum em alemão o cara pareceu sugerir o gdb (debugger). Surpresa: o gdb também dava segfault, sem mesmo rodar o bash! Foi aí que liguei os pontos: tanto o gdb quanto o bash usam *line completion*, ou seja, deviam usar a readline, e portanto seriam afetados pelo arquivo `~/.inputrc` que eu tinha copiado há pouco. Fui olhar o arquivo e tinha uma linha mandando incluir o arquivo de sistema `/etc/inputrc`. Só que o arquivo de sistema também mandava ler o arquivo de usuário! Era essa referência cíclica que estava causando o erro. Eliminei-a e deu tudo certo :D

Claro, é natural que tenha diferenças entre distribuições, mas essa é meio esquisita, porque parece que no ArchLinux o arquivo de sistema é lido antes do de usuário (enquanto que no Ubuntu é o de usuário que é lido primeiro). Pela documentação da readline, parece que é o Ubuntu que está certo. Depois talvez eu dê uma investigada melhor pra ver se entendi bem a ordem das coisas.
