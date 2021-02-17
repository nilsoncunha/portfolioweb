---
layout: post
title: "Como foi o desafio do IGTI"
featured-img: desafio_igti
categories: [Python, MongoDB, Engenheiro Dados]
---

## Como resolvi o desafio do IGTI

Fala pessoal, dessa vez vindo aqui para mostrar a solução do desafio do IGTI no _bootcamp_ de Engenheiro de Dados.

O desafio consistia em criar um _pipeline_ no _Airflow_ para pegar os dados de duas api's, uma do IBGE (contendo região, estado, municipio, etc) e outra fornecida pelo professor com os dados no MongoDB (principal), criar na AWS um serviço do S3 para armazenar os arquivos e também um RDS (usando um banco da preferência do aluno, escolhi o Postgres) simulando um DW. Nesse DW deveriamos fazer a ingestão dos dados somente das mulheres com idade entre 20 a 40 anos. No final deveria ser respondido algumas perguntas.

Fiz a primeira versão do desafio com a versão 1.10 do _Airflow_ (código não ficou muito bonito, mas funcionou kkk), logo depois fiz uma segunda versão utilizando a versão 2.0 do _Airflow_ (está muito linda a interface).

Nesse link ([igti_desafio_v1]('https://github.com/nilsoncunha/bootcamp_igti_engenheiro_de_dados/blob/main/modulo_desafio/igti_desafio_v1.py')) você consegue visualizar o código que fiz com a versão 1.10 do _Airflow_ e nesse ([igti_desafio_v2]('https://github.com/nilsoncunha/bootcamp_igti_engenheiro_de_dados/blob/main/modulo_desafio/igti_desafio_v2.py')) já com a versão 2.0.

O que achei bem interessante no _Airflow_ é o fato de conseguir trabalhar com senhas e usuários sem precisar de passar diretamente no código (muito útil), basta criar uma variavel e inserir os valores. 

_obs.: o próprio Airflow se encarrega de ocultar o campo valor quando a variável é uma senha, para isso basta colocar no campo key a palavra 'secret'_

<center><img src="https://www.dropbox.com/s/xjr6usd08bpg56r/igti_v2_variables.jpg?raw=1"></center>


Feito isso, criei a instancia no RDS para simular meu Data Warehouse.

<center><img src="https://www.dropbox.com/s/d0edfbgj9uunspq/igti_v2_aws_postgres.png?raw=1"></center>


Na _[Dag]('https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#dags')_ observamos que, como não há dependência entre entre as funções consigo paralelizar a execução e simultaneamente fazer a captura e tratamento dos dados das api's, logo após subir os arquivos para o S3 e fazer a ingestão no DW.

<center><img src='https://www.dropbox.com/s/6227lavsj8jsdsu/igti_v2_grafico.png?raw=1'></center>


O código para essa execução ficou assim.

{% highlight python %}
ibge = dados_ibge()
api = dados_api()
s3_ibge = upload_s3(ibge)
s3_api = upload_s3(api)
dw_ibge = escrever_dw(ibge)
dw_api = escrever_dw(api)

desafio_final = desafio_final_pipeline()
{% endhighlight %}

Para extrair as informações utilizei o [Metabase]('https://www.metabase.com/') gerei alguns gráficos e respondi questões relacionadas ao desafio.

<center><img src="https://www.dropbox.com/s/lqmeo8krgmponq1/igti_v2_painel_metabase.png?raw=1"></center>


E é isso pessoal, até uma próxima.
