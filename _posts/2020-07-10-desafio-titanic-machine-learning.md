---
layout: post
title: "Desafio Titanic Machine Learning"
featured-img: titanic
categories: [Machine Learning, Data Analysis, Logistic Regression, Random Forest, Confusion Matrix]
---

Pode ser que algumas pessoas não tenham assistido ao filme do **Titanic** (*será?*), mas se estiver na área de Ciência de Dados provavelmente já tenha ouvido pelo tão famoso desafio no [Kaggle](https://www.kaggle.com/c/titanic) que dizem ser a "porta de entrada" para os desafios de Machine Learning.

Nesse caso, então vamos aproveitar e verificar o que os dados desse trágico acidente tem a nos dizer, ou melhor, o que conseguimos retirar deles.

<center><img src="https://www.dropbox.com/s/ima4y79h7upuxow/titanic.jpeg?raw=1"></center><br>

> Seguirei o *workflow* da ciência de dados, que é:
> 1. Pegar o problema, que é sobre os passageiros do Titanic;
> 1. obter os dados na plataforma do [Kaggle](https://www.kaggle.com/c/titanic);
> 1. Análise dos dados;
> 1. Limpeza dos dados;
> 1. Preparar parar utilizar as bibliotecas de *Machine Learning*;
> 1. Aplicação do *Machine Learning*;
> 1. Verificar os resultados obtidos;
> 1. Comunicar com o negócio.

<hr>

### Obtendo os dados

*obs.: Você pode acompanhar o notebook completo por [aqui](https://colab.research.google.com/drive/10XbF-MI1mRXpQHTsPL5qfjYkeAkYZQVa?usp=sharing#scrollTo=0R2bspQckKZv)*

O que gosto de utilizar nessas análises é a plataforma do Google Colab importando o arquivo do Dropbox, que consigo uma melhor organização para meu portfólio. Já vi algumas pessoas com dúvidas em como importar os dados dessa forma, porém é bem simples.

- 1) no dropbox clicar para compartilhar o arquivo e copiar o link;
- 2) o arquivo virá com o final `nome_arquivo.csv?dl=0` modifique o `dl=0` para `raw=1`

{% highlight python %}
# importando as bases que estão no meu dropbox pessoal
train = pd.read_csv('https://www.dropbox.com/s/<código_do_arquivo>/train.csv?raw=1')
test = pd.read_csv('https://www.dropbox.com/s/<código_do_arquivo>/test.csv?raw=1')
{% endhighlight %}

<hr>

### Realizando a análise

Há nos dados de treino 891 linhas e 12 colunas, já no de teste 418 linhas e 11 colunas
{% highlight python %}
print(f'{train.shape[0]} linhas e {train.shape[1]} colunas \n')
print(f'{test.shape[0]} linhas e {test.shape[1]} colunas')
{% endhighlight %}

Para verificar a correlação entre as variáveis temos algumas opções, dentre elas:
- Pearson -> Avalia correlação linear entre as variáveis quantitativas
- Spearman -> Avalia a correlação *monotônica*\* entre as variáveis, não necessáriamente sendo linear e também não precisam ser quantitativas.

_\*obs.: Em uma relação monotônica, as variáveis tendem a mover-se na mesma direção relativa, mas não necessariamente a uma taxa constante, como na linear. [ref.](https://operdata.com.br/blog/coeficientes-de-correlacao/)_

Temos que nos atentar para o que queremos saber dos dados e qual a correlação a ser utilizada. Se a relação é linear, o método de Pearson é o mais indicado. Abaixo podemos observar que algumas variáveis obtiveram valores diferentes na correlação

{% highlight python %}
# verificando a correlação
fig, ax = plt.subplots(1, 2, figsize=(15,4))
sns.heatmap(train.corr(method='spearman'), annot=True, fmt='.2f', ax=ax[0]);
sns.heatmap(train.corr(method='pearson'), annot=True, fmt='.2f', ax=ax[1]);
{% endhighlight %}

<center><img src="https://www.dropbox.com/s/yj0fsea72l6bmls/correlation.png?raw=1"></center><br>

Ao todo tivemos uma maior taxa de não sobreviventes e dentre eles a maioria era de homens, de pessoas que estavam na terceira classe e daquelas que embarcaram em *Southampton*. Outro aspecto interessante é que a maioria que embarcaram em *Southampton* foram da terceira classe.

{% highlight python %}
colunas = ['Survived', 'Sex', 'Pclass', 'Embarked']
fig, ax = plt.subplots(1, 4, figsize=(14,4))

for i, j in enumerate(colunas):
    sns.countplot(x=j, data=train, ax=ax[i])

ax[0].set_xticklabels(['No', 'Yes'])
for i in range(len(ax)):
    ax[i].set_ylabel('');
{% endhighlight %}

<center><img src='https://www.dropbox.com/s/qw70gxrxrnucr1o/sobreviventes.png?raw=1'></center><br>
  
{% highlight python %}
grid = sns.FacetGrid(data=train, col='Pclass', row='Sex', hue='Survived')
grid.map(plt.hist, 'Embarked').add_legend();
{% endhighlight %}

<center><img src='https://www.dropbox.com/s/5itasy2vbchyxpq/facetgrid.png?raw=1'></center><br>

<hr>
  
### Limpeza e preparação

Como temos os dados separados em treino e teste, para não esquecer de fazer o tratamento em uma base e na outra não, vou juntá-los para realizar o tratamento ao mesmo tempo.

{% highlight python %}
# Pegando o indice para utilizar ao separá-los novamente
train_idx = train.shape[0]

# Como vamos remover o passengerId temos que copiá-lo para uma outra variável
passengerId = test['PassengerId']

# Salvando o target para treinar nosso modelo.
target = train['Survived'].copy()
train.drop('Survived', axis=1, inplace=True)

train_df = pd.concat([train, test], axis=0).reset_index(drop=True)
{% endhighlight %}

Vamos remover agora a variável `PassengerId`, precisaremos dela somente no teste para salvar o modelo e subir o arquivo para o Kaggle

{% highlight python %}
train_df.drop('PassengerId', axis=1, inplace=True)
{% endhighlight %}

Novamente visualizando os dados nulos, a coluna Cabin está com mais de 70% de dados faltantes, nesse caso será removida.
{% highlight python %}
train_df.isnull().mean().sort_values(ascending=False)
{% endhighlight %}
```
Cabin       0.774637
Age         0.200917
Embarked    0.001528
Fare        0.000764
Ticket      0.000000
Parch       0.000000
SibSp       0.000000
Sex         0.000000
Name        0.000000
Pclass      0.000000
dtype: float64
```

Para a Embarked irei alterar o valor nulo pelo mais frequente.
{% highlight python %}
# verificando o valor mais frequente
train_df['Embarked'].describe()
{% endhighlight %}
```
count     1307
unique       3
top          S
freq       914
Name: Embarked, dtype: object
```

{% endhighlight %}
# realizando a alteração
train_df['Embarked'] = train_df['Embarked'].fillna('S')
{% endhighlight %}

Em Fare e Age irei utilizar a mediana.
{% highlight python %}
train_df['Fare'] = train_df['Fare'].fillna(train_df['Fare'].median())
train_df['Age'] = train_df['Age'].fillna(train['Age'].median())
{% endhighlight %}

Ao listar o nome dos passageiros observamos que há o pronome de tratamento, será que isso será relevante para nosso modelo? Criarei uma nova coluna e verificamos o resultado posteriormente
{% highlight python %}
train_df['Pronouns'] = train_df['Name']
{% endhighlight %}

Realizando a alteração na nova coluna para deixar apenas os pronomes sem o ponto final. Ao utilizar o `contains` estou verificando se há aquela palavra no nome. Como utilizei `regex=False` verifico se no nome contém a palavra específica.

{% highlight python %}
pronomes_1 = ['Miss.','Mrs','Mr.','Ms.','Master.','Col.','Major.','Capt.','Dr.','Rev.','Sir.']
pronomes_2 = ['Mlle.','Dona.','Don.','Jonkheer.','Countess.','Mme.']

for _, j in enumerate(pronomes_1):
    train_df['Pronouns'].loc[train_df['Name'].str.contains(j, regex=False)] = j
    train_df['Pronouns'] = train_df['Pronouns'].str.replace('.','')

for _, k in enumerate(pronomes_2):
    train_df['Pronouns'].loc[train_df['Name'].str.contains(k, regex=False)] = 'Other'
    train_df['Pronouns'] = train_df['Pronouns'].str.replace('.','')
{% endhighlight %}

Com isso obtemos as informações

{% highlight python %}
train_df['Pronouns'].value_counts()

Mr        757
Miss      258
Mrs       200
Master     61
Rev         8
Dr          8
Other       7
Col         4
Major       2
Ms          2
Sir         1
Capt        1
Name: Pronouns, dtype: int64
{% endhighlight %}

Agora alterar a variável Sex para 0 e 1 e também alterar a coluna Embarked que criará três novas colunas (serão três porque há apenas três valores). Podemos utilizar o OneHotEncoding ou até mesmo o getdummies do pandas.

{% highlight python %}
train_df['Sex'] = train_df['Sex'].map({'female': 0, 'male': 1})

train_df = pd.get_dummies(train_df, columns=['Embarked'])
{% endhighlight %}

Utilizarei o *LabelEncoder* para alterar as variáveis *Ticket* e *Pronouns*, que são categóricas, para um valor numérico.

*Essa opção gera os números aleatórios para as informações, com isso pode ser que os números fique muito diferente um dos outros. Um problema que pode ocorrer é o modelo achar que um valor é melhor que o outro só porque aquele valor é maior, isso só consegue descobrir realizando os treinos e testes no modelo.*

{% highlight python %}
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

train_df['Ticket'] = le.fit_transform(train_df['Ticket'])
train_df['Pronouns'] = le.fit_transform(train_df['Pronouns'])
{% endhighlight %}

Como os valores de Fare, e agora Ticket, têm uma variância bem alta, então realizarei a padronização dos dados

{% highlight python %}
from sklearn.preprocessing import StandardScaler

padronizar = StandardScaler()
padronizado = padronizar.fit_transform(train_df[['Fare','Ticket']])
{% endhighlight %}

Pclass|Sex|Age|SibSp|Parch|Pronouns|Embarked_C|Embarked_Q|Embarked_S|FareStandard|TicketStandard
---|---|---|---|---|---|---|---|---|---|---
0|3|1|22.0|1|0|6|0|0|1|-0.503291|0.922332
1|1|0|38.0|1|0|7|1|0|0|0.734744|1.267701
2|3|0|26.0|0|0|5|0|0|1|-0.490240|1.620266
3|1|0|35.0|1|0|7|0|0|1|0.383183|-1.434095
4|3|1|35.0|0|0|6|0|0|1|-0.487824|0.666902

Com a base tratada já posso implementar o modelo de Machine Learning, antes disso irei realizar a separação dos dados novamente em treino e teste.

{% highlight python %}
# Selecionando os dados até o index que havia selecionado no início.
train = train_df.iloc[:train_idx]
test = train_df.iloc[train_idx:]
{% endhighlight %}

### Aplicação do modelo de *Machine Learning*

Utilizarei os modelos *LogisticRegression* e *RandomForestClassifier*

{% highlight python %}
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
{% endhighlight %}

Como temos duas bases que são treino e teste, irei pegar uma porção dos dados de treino para criar os dados de validação e verificar a métrica do modelo

{% highlight python %}
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(train, 
                                                    target, 
                                                    test_size=0.3, 
                                                    random_state=1234)
{% endhighlight %}

Realizando o treino e a previsão dos modelos

{% highlight python %}
# Treinando a Logistic Regression
lr = LogisticRegression(n_jobs = -1, max_iter=500, random_state=10)
lr.fit(X_train, y_train)

# Treinando a Random Forest
rfc = RandomForestClassifier(n_jobs = -1, n_estimators=700, random_state=10)
rfc.fit(X_train, y_train)

# Fazendo a previsão dos modelos
lr_previsao = lr.predict(X_test)
rfc_previsao = rfc.predict(X_test)
{% endhighlight %}

### Verificação das métricas

Após implementar os modelos, chegou a hora de avaliar se conseguiram realizar uma boa classificação ou não.

{% highlight python %}
from sklearn.metrics import confusion_matrix, accuracy_score, \
                            precision_score, recall_score,  \
                            f1_score, classification_report

# Métricas Logistic Regression
lr_accuracy = accuracy_score(y_test, lr_previsao)
lr_precision = precision_score(y_test, lr_previsao)
lr_recall = recall_score(y_test, lr_previsao)
lr_f1 = f1_score(y_test, lr_previsao)

# Métricas Random Forest Classifier
rf_accuracy = accuracy_score(y_test, rfc_previsao)
rf_precision = precision_score(y_test, rfc_previsao)
rf_recall = recall_score(y_test, rfc_previsao)
rf_f1 = f1_score(y_test, rfc_previsao)
{% endhighlight %}

Para melhor visualizar criei um *dataframe* com as informações

{% highlight python %}
metricas = pd.DataFrame({
    'Logistic Regression': [lr_accuracy, lr_precision, lr_recall, lr_f1],
    'Random Forest': [rf_accuracy, rf_precision, rf_recall, rf_f1]},
    index=['Acurácia', 'Precisão', 'Recall', 'F1_Score'])
metricas
{% endhighlight %}


Logistic|Regression|Random Forest
---|---|---
Acurácia|0.820896|0.854478
Precisão|0.793478|0.824742
Recall|0.715686|0.784314
F1_Score|0.752577|0.804020

Obtemos as métricas separadas, porém podemos utilizar o `classification_report` que trará todas essas métricas e também separadas por classe

{% highlight python %}
lr_report = classification_report(y_test, lr_previsao)
rf_report = classification_report(y_test, rfc_previsao)

print('Report Logistic Regression: \n')
print(lr_report)
print(20*'-', '\n')
print('Report Random Forest: \n')
print(rf_report)
{% endhighlight %}

Report Logistic Regression: 

              precision    recall  f1-score   support

           0       0.84      0.89      0.86       166
           1       0.79      0.72      0.75       102

    accuracy                           0.82       268
   macro avg       0.81      0.80      0.81       268
weighted avg       0.82      0.82      0.82       268

-------------------- 

Report Random Forest: 

              precision    recall  f1-score   support

           0       0.87      0.90      0.88       166
           1       0.82      0.78      0.80       102

    accuracy                           0.85       268
   macro avg       0.85      0.84      0.84       268
weighted avg       0.85      0.85      0.85       268

#### *Mas o que seriam essas métrica?*

Antes disso vou falar um pouco da Matrix de Confusão (que só pelo nome já deixa confuso).

A matriz é responsável por nos mostrar como o modelo está se comportando. Como na base a previsão obtém a resposta se `não sobreviveu (0)` ou `sobreviveu (1)`, então trará a seguinte informação:

> obs.: Coloquei primeiro o *positivo (1)* e depois o *negativo (0)* e também o *Valor Verdadeiro* a esquerda e o *Valor Predito* acima, mas por que está falando isso? Porque **se alterarmos essa ordem também será alterado a estrutura da matriz e como devemos ler, então cuidado.** Continuando...

<center><img src='https://www.dropbox.com/s/rtc2uv2sq3wcvsx/matriz_confusao.png?raw=1'></center>

- **TP ou VP (True Positive ou Verdadeiro Positivo)**: Modelo previu que sobreviveu e acertou
- **FN (False Negative ou Falso Negativo)**: O modelo previu que não sobreviveu, mas na verdade sobreviveu. **Erro tipo II**
- **FP (False Positive ou Falso Positivo)**: O modelo previu que sobreviveu, mas na verdade não sobreviveu. **Erro tipo I**
- **TN ou VN (True Negative ou Verdadeiro Negativo)**: Modelo previu que não sobreviveu e acertou

Mas qual o motivo dessa matriz? Ela irá nos ajudar a entender as métricas.

Verificando como que fica a matriz de confusão com os dados

{% highlight python %}
fig, ax = plt.subplots(1, 2, figsize=(12,5))

lr_matrix = confusion_matrix(y_test, lr_previsao, labels=[1,0]) # Confusion Matrix Logistic Regression
rf_matrix = confusion_matrix(y_test, rfc_previsao, labels=[1,0]) # Confusion Matrix Random Forest

cm = [lr_matrix, rf_matrix]

for i in range(len(cm)):
    sns.heatmap(cm[i], annot=True, fmt='.2f', ax=ax[i]);
    title = ['Logistic Regression','Random Forest']
    ax[i].set_title(title[i], fontsize=18);
    ax[i].set_xticklabels(['1', '0'])
    ax[i].set_yticklabels(['1', '0'])
    ax[i].set_xlabel('Valor predito')
    ax[i].set_ylabel('Valor real')
{% endhighlight %}

<center><img src='https://www.dropbox.com/s/axozkxr9xx41byz/matriz_confus%C3%A3o.png?raw=1'></center>
  
O modelo de *Logistic Regression* acerta (VP) a previsão de que tiveram 73 pessoas sobreviventes, porém se engana (FN) ao predizer que 29 não sobreviveram.

O modelo também errou (FP) ao prever que 19 pessoas sobreviveram, mas acertou (VN) ao dizer que 147 pessoas não sobreviveram.

O que uma métrica tem de melhor que a outra? Isso vai depender mais do que você precisa para o seu modelo naquele momento e com isso escolher aquela que fará mais sentido para você solucionar o problema

- Explicando cada uma das métricas

- **Acurácia**: Retorna os acertos obtidos dividido pela quantidade total dos dados, **ignora os erros cometidos**

$$
Acurácia = \frac{\text{VP + VN}}{\text{VP + VN + FP + FN}}
$$
<br>
$$\text{Logistic Regression} = \frac{73 + 147}{73 + 29 + 19 + 147} = 0,8208$$
<br>
$$\text{Random Forest} = \frac{80 + 149}{80 + 22 + 17 + 149} = 0,8544$$
<br>

- **Precisão**: Retorna o quanto o modelo está acertando, ou seja, quando retornar os sobreviventes se ele está acertando quais eram.

$$
Precisão = \frac{\text{VP}}{\text{VP + FP}}
$$
<br>
$$\text{Logistic Regression} = \frac{73}{73 + 19} = 0,7934$$
<br>
$$\text{Random Forest} = \frac{80}{80 + 17} = 0,8247$$
<br>

- **Recall**: Retorna se o modelo está acertando a classe a qual o valor pertence, ou seja, se é sobrevivente quanto que está prevendo corretamente que sobreviveu

$$
Recall = \frac{\text{VP}}{\text{VP + FN}}
$$
<br>
$$\text{Logistic Regression} = \frac{73}{73 + 29} = 0,7156$$
<br>
$$\text{Random Forest} = \frac{80}{80 + 22} = 0,7843$$
<br>

- **F1_Score**: Retorna a combinação ([média harmônica](https://pt.wikipedia.org/wiki/M%C3%A9dia_harm%C3%B4nica)) de precisão e recall. 

$$
\text{F1_Score} = 2 \times \frac{\text{precisão} \times \text{recall}}{\text{precisão + recall}}
$$
<br>
$$\text{Logistic Regression} = 2 \times \frac{0,7934 \times 0,7156}{0,7934 + 0,7156} = 0,7525$$
<br>
$$\text{Random Forest} = 2 \times \frac{0,8247 \times 0,7843}{0,8247 + 0,7843} = 0,8040$$
<br>
