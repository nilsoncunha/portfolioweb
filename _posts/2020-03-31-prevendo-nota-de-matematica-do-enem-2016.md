---
layout: post
title: "Prevendo nota de matemática do ENEM de 2016"
featured-img: enem
categories: [Machine Learning, Data Analysis, Python, Linear Regression, Random Forest]
---
Todos sabemos que o Exame Nacional do Ensino Médio (ENEM) é uma prova muito concorrida e que muitos candidatos tem a oportunidade de estudar em uma boa instituição devido a pontuação que obteve. 

> *Neste [notebook](https://colab.research.google.com/drive/1beela9VdVWEcLPEDXUoo7LmFzrmpYxdz) está toda minha análise e os tratamentos realizados. Tem também o [deploy](https://portfolio-enem.herokuapp.com/) que fiz no Heroku, é só preencher os campos e realizar a previsão*

Vamos realizar uma análise da base do ENEM de 2016, fazer a previsão da nota de matemática dos candidados e tentar saber como que se saíram, qual foi o estado com mais participantes e qual foi a melhor pontuação e mais. Então vamos lá!

Para iniciar fiz a importação da base de [treino](https://dl.dropbox.com/s/7vexlzohz7j3qem/train.csv?dl=0) e de [teste](https://dl.dropbox.com/s/dsgzaemaau9g5z0/test.csv?dl=0).

{% highlight python %}
train = pd.read_csv('https://dl.dropbox.com/s/7vexlzohz7j3qem/train.csv?dl=0', index_col=0)
test = pd.read_csv('https://dl.dropbox.com/s/dsgzaemaau9g5z0/test.csv?dl=0')
{% endhighlight %}

A base está distribuida da seguinte forma:
{% highlight python %}
Treino: 13730 linhas e 166 colunas (features)
Teste: 4576 linhas e 47 colunas (features)
{% endhighlight %}

### Analisando a base

Conseguimos identificar que o estado de São Paulo teve o maior número de participantes, seguido por Ceará e Minas Gerais

![participantes](https://dl.dropbox.com/s/zcjxdicfy6tnxf8/candidatos_por_estado.png?dl=0)

Fazendo a verificação por sexo, conseguimos observar que as mulheres tiveram uma maior participação na prova.

![quantidade por sexo](https://dl.dropbox.com/s/zd5a5gxfud3mj4b/candidatos_por_sexo.png?dl=0)

Muitos dos candidatos que realizam esse exame são aqueles que estão concluindo o ensino médio, sendo assim, temos uma grande concentração da idade entre 18 e 19 anos. A probabilidade de termos um candidato com idade menor ou igual a 25 anos é de 69%.

![histograma idade](https://dl.dropbox.com/s/oesti6onck3o1nk/distribuicao_idade.png?dl=0)

Na prova e na redação a maior pontuação é de mil pontos. Na distribuição abaixo observamos que nas provas há uma concentração das notas próximo de 500, já na redação está próximo de 600. A probabilidade dos candidatos obterem uma nota maior ou igual a 600 na prova é de 6,22%, já para a redação a probabilidade é de obterem nota maior ou igual a 700 é de 13,25%.

![notas](https://dl.dropbox.com/s/qlob22eyx0tlx8j/notas.png?dl=0)

Na redação temos alguns pontos que são observados no caso de fugir ao tema, for anulada, entre outros. A tabela abaixo nos mostra como que ficaram essas situações

|Situação|Quantidade|
|:---:|---:|
|Sem problemas|13195|
|Em branco|133|
|Fuga ao tema|105|
|Parte desconectada|29|
|Cópia texto motivador|17|
|Texto insuficiente|12|
|Fere direitos autorais|9|
|Não atendimento ao tipo|7|
|Anulada|3|

Acima mostramos como ficaram as notas de toda a base de dados, agora vamos verificar como que ficaram as notas das provas distribuídas por estado. Há uma boa quantidade de *outliers* (valores fora do comum), mas nossa mediana está bem próximo de 500, conforme citamos anteriormente.

![notas por estado](https://dl.dropbox.com/s/cp7qbaj9w6y369b/notas_estados.png?dl=0)

Quando fazemos a inscrição no ENEM, há um questionário socioeconómico para respondermos. Baseando nisso, vamos observar se dependendo da resposta os candidatos podem se sair melhor que os outros. Uma das perguntas é "Até que série seu pai, ou o homem responsável por você, estudou?". Podemos inferir que quanto maior o grau de escolaridade do pai, mais provável que o candidato obtenha boa nota no exame.

![questionario q001](https://dl.dropbox.com/s/tz4vcr0mfnrclxw/Q001.png?dl=0)

Isso vale também em relação a renda mensal da família. Quanto maior a renda, maior a possibilidade do canditato ter uma melhor nota.

![questionario q006](https://dl.dropbox.com/s/6t33zko9q7ngxop/Q006.png?dl=0)

### Tratando os dados e realizando a previsão

Depois dessas análises, chegou a hora de prepar os dados para nossa previsão. 
Primeiro realizei o tratamento imputando o valor 0 (zero) na prova daqueles candidatos que estavam com com status diferente de "Presente na prova".

{% highlight python %}
train_df.loc[train_df['TP_PRESENCA_CH'] != 1, 'NU_NOTA_CH'] = train_df.loc[train_df['TP_PRESENCA_CH'] != 1, 'NU_NOTA_CH'].fillna(0)
train_df.loc[train_df['TP_PRESENCA_CN'] != 1, 'NU_NOTA_CN'] = train_df.loc[train_df['TP_PRESENCA_CN'] != 1, 'NU_NOTA_CN'].fillna(0)
train_df.loc[train_df['TP_PRESENCA_MT'] != 1, 'NU_NOTA_MT'] = train_df.loc[train_df['TP_PRESENCA_MT'] != 1, 'NU_NOTA_MT'].fillna(0)
train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_LC'] = train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_LC'].fillna(0)
train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_REDACAO'] = train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_REDACAO'].fillna(0)
{% endhighlight %}

Como os modelos de *Machine Learning* não aceitam dados categóricos alterei as informações do sexo de 'F' e 'M' para 0 e 1, respectivamente.

{% highlight python %}
train_df['TP_SEXO'] = train_df['TP_SEXO'].map({'M': 1, 'F': 0})
{% endhighlight %}

Utilizei também o *Label Encoder* para alterarmos o tipo das respostas referente ao questionário socioeconômico. Por exemplo: na coluna que havia as respostas A, B, C e D passarão a ser 1, 2, 3 e 4. O *Label Encoder* se encarrega de fazer essa alteração.

{% highlight python %}
train_df['Q001'] = label_encoder.fit_transform(train_df['Q001'])
train_df['Q002'] = label_encoder.fit_transform(train_df['Q002'])
train_df['Q006'] = label_encoder.fit_transform(train_df['Q006'])
train_df['Q025'] = label_encoder.fit_transform(train_df['Q025'])
train_df['Q047'] = label_encoder.fit_transform(train_df['Q047'])
{% endhighlight %}

Utilizei dois modelos de aprendizado supervisionado baseado em regressão, que foram *Random Forest* e *Linear Regression*, pois estamos querendo realizar a previsão da nota de matemática e supervisionado porque estamos passando a *feature* de resposta para realizar o treinamento. A outros modelos que poderiamos ter utilizado, mas vamos trabalhar apenas com esses.

{% highlight python %}
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(train, target)

lr_score = lr.score(train, target)
{% endhighlight %}
Acurácia do modelo: 91.31%

{% highlight python %}
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_jobs=-1)
rf.fit(train, target)

rf_score = rf.score(train, target)
{% endhighlight %}
Acurácia do modelo: 98.91%

Tivemos nosso modelo *Random Forest* com o *score* melhor que o *Linear Regression*, então quer dizer que o primeiro é melhor que o segundo? ***Não***, isso quer dizer **apenas** que o primeiro melhor se adequou a nossa base e por tanto teve a melhor acurácia. 

Nunca podemos dizer que um modelo é melhor, mas sim que um se adequa melhor que o outro para o que foi proposto.

Então é isso pessoal, espero que tenham gostado e até a próxima.
