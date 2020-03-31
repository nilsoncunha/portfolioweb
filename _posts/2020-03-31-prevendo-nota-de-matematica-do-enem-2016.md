---
layout: post
title: "Prevendo nota de matemática do ENEM de 2016"
featured-img: enem
categories: [Machine Learning, Data Analysis, Python, Linear Regression, Random Forest]
---
Todos sabemos que o Exame Nacional do Ensino Médio (ENEM) é uma prova muito concorrida e que muitos candidatos tem a oportunidade de estudar em uma boa instituição devido a pontuação que obteve. 

Vamos realizar uma análise da base do ENEM de 2016, fazer a previsão da nota de matemática dos candidados e tentar saber como será que se saíram, qual foi o estado com mais participantes e qual foi a melhor pontuação e mais. Utilizarei texto mesclando com gráfico para tentar melhorar a visualização das informações. Então vamos lá!

Iniciando nossa análise, conseguimos identificar que o estado de São Paulo teve o maior número de participantes, seguido por Ceará e Minas Gerais

![participantes](https://dl.dropbox.com/s/t0x9bon85ccu4g2/sg_uf_residencia.png?dl=0)

Fazendo a verificação por sexo, conseguimos observar que as mulheres tiveram uma maior participação na prova.

![quantidade por sexo](https://dl.dropbox.com/s/38z6thk8kcmub79/img2.png?dl=0)

Muitos dos candidatos que realizam esse exame são aqueles que estão concluindo o ensino médio, sendo assim, temos uma grande concentração da idade entre 18 e 19 anos.

![histograma idade](https://dl.dropbox.com/s/8x9chm2rxgmi9a8/histograma-idade.png?dl=0)

Mediante esses dados, a probabilidade dos candidatos que realizaram a prova ter idade menor ou igual a 25 anos é de 69%, uma taxa razoável, já que a grande maioria são de concluíntes do ensino médio. Veremos agora como está distribuída a nota dos candidatos.
