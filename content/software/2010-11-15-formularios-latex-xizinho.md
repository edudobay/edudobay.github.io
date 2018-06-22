---
layout: post
title:  "Formulários para preencher em LaTeX – Parte 1: o “xizinho”"
date:   2010-11-15 14:45:22 +0000
categories: programming
tags:   latex
---
Pretendo escrever uma pequena série de posts sobre como criar formulários em LaTeX, para serem preenchidos no próprio código. Nessa primeira parte, vou mostrar uma maneira de fazer lacunas para preencher com um “X”, como na figura abaixo:

![Sim ou não?]({filename}/assets/2010/11/simnao.png)

Para isso, vou usar o pacote `tikz`, que permite que você faça desenhos e diagramas em LaTeX de uma forma bastante humana; a interface de código é bem utilizável e ele gera resultados muito bons esteticamente.

A lacuna não preenchida é fácil: basta colocar um comando de espaçamento entre os parênteses — eu escolhi o comando `\quad`, que gera um espaçamento de `1em` (é uma unidade que corresponde aproximadamente à largura de um M maiúsculo na fonte atual), mas poderíamos usar qualquer outra largura, com o comando `\hspace`{*largura*}.

{% highlight tex %}
(\quad)
{% endhighlight %}

Como o objetivo é alinhar o X com os parênteses, precisamos conhecer as dimensões dos parênteses (imagino que em geral o par seja simétrico, então só precisamos medir um deles). Devemos levar em conta que, com relação à linha de base do texto (a “pauta” virtual que o computador usa para alinhar os caracteres), cada caractere pode estender-se para cima e/ou para baixo. Em LaTeX (e em tipografia em geral), chamamos os comprimentos acima e abaixo da linha de base, respectivamente, de **altura** e **profundidade**, conforme o diagrama abaixo:

![Altura e profundidade do caractere]({filename}/assets/2010/11/baseline1.png)

Para medir a altura e a profundidade do caractere, vamos olhar para a sua caixa delimitadora, ou seja, o menor retângulo que consegue englobar o caractere todo (sombreado em azul claro na figura). Em LaTeX, podemos criar uma caixa (virtual, que não sai no documento) com o comando `\newbox`, e depois colocamos dentro dela um caractere (ou qualquer porção de texto) com o comando `\sbox`:

{% highlight tex %}
\newbox{\crossbox}% cria o comando para conter a caixa
\sbox{\crossbox}{(}% coloco na caixa o parêntese esquerdo
{% endhighlight %}

(`\crossbox` é o nome da caixa.) Para descobrir as dimensões da caixa, usamos os comandos (do TeX) `\ht` (*height*) e `\dp` (*depth*). O desenho do X será feito assim:

{% highlight tex %}
  \begin{tikzpicture}[baseline=0pt]
  \useasboundingbox (0, -\dp\crossbox) rectangle (1em, \ht\crossbox);
  \draw[line width=0.6pt]
    (0, -\dp\crossbox) -- (1em, \ht\crossbox)
    (1em, -\dp\crossbox) -- (0, \ht\crossbox);%
  \end{tikzpicture}
{% endhighlight %}

Vou explicar os detalhes:

* `\begin{tikzpicture}` e `\end{tikzpicture}` são os delimitadores de desenho para o pacote tikz. A opção `[baseline=0pt]` serve para que a origem do sistema de coordenadas do desenho coincida com a linha de base do texto (o padrão é alinhar o limite inferior do desenho na linha de base).
* `\useasboundingbox` serve para ajustar a caixa delimitadora do desenho (os limites laterais do desenho, que irão se alinhar com o texto em volta). Eu quero que o X tenha exatamente a mesma largura do espaço das lacunas em branco, então preciso ajustar `1em` de largura. A altura não importa muito pois já definimos que o alinhamento vertical com o texto se dará pela origem do sistema de coordenadas, mas, já que precisamos definir alguma altura, vamos definir tudo certo de uma vez.
* O comando `\draw` é que desenha o X propriamente dito; cada par `(ponto) -- (ponto)` equivale a um segmento. A opção `line width` especifica a espessura da linha; acho que `0.5` ou `0.6pt` já estão de bom tamanho.

Vamos juntar tudo isso e criar um comando personalizado. Vou deixar a largura como um parâmetro ajustável (que pode ser acessado usando o código `#1`), cujo valor padrão é de `1em`.

{% highlight tex %}
\newbox{\crossbox}
\newcommand{\cross}[1][1em]{{ "{%" }}
  \sbox{\crossbox}{(}%
  \begin{tikzpicture}[baseline=0pt]
  \useasboundingbox (0,-\dp\crossbox) rectangle (#1,\ht\crossbox);
  \draw[line width=0.6pt]
    (0,-\dp\crossbox) -- (#1,\ht\crossbox)
    (#1,-\dp\crossbox) -- (0,\ht\crossbox);
  \end{tikzpicture}%
}
{% endhighlight %}

Note que eu criei a caixa *antes* da definição do comando. Se eu a criasse *dentro* do comando, o LaTeX iria reclamar se você usasse o comando mais de uma vez, pois você estaria tentando criar uma caixa já existente.

Perceba também que eu coloquei vários símbolos de comentário (`%`) no final das linhas. Isso é necessário para que o LaTeX não coloque espaços extras em lugares indevidos.

Para chamar esse comando, basta usar a sintaxe `\cross`, ou `\cross[largura]` caso queira uma largura diferente de `1em`. O exemplo no começo desse post foi produzido com o seguinte código:

{% highlight tex %}
(\quad) Sim \\
(\cross) Não
{% endhighlight %}
