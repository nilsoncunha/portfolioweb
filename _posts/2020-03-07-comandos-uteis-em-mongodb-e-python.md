---
layout: post
title: "Comandos uteis em MongoDB e Python"
featured-img:
categories: [Python, MongoDB]
---

Quando começamos a utilizar uma nova ferramenta é comum nos primeiros momentos esquecermos um código e ter que procurar na documentação ou dar aquela _"Googada"_ para conseguir encontar como fazer aquilo novamente? Pois bem, também me vi assim em relação ao _MongoDB_ e utilizando o _Python_ para extrair essas informações. Com isso resolvi criar esse post com os principais comandos, borá lá? 

## MongoDB

A sintaxe base que utilizaremos na maior parte do tempo é `db.collection.funcao({})`

* Criando ou selecionando um banco já existente _(código é o mesmo)_
{% highlight python %}
> use portfolio
switched to db portfolio
{% endhighlight %}

* Criando a collecion
{% highlight python %}
# _Passando o parâmetro do createCollection('nome_collection')
> db.createCollection("times")
{ "ok" : 1 }

ou

# _Criando já inserindo dados
> db.dados.insert({"nome": "Ciclano", "rua": "Logo ali", "bairro": "Bom começo"})
WriteResult({ "nInserted" : 1 })
{% endhighlight %}

* Consultando as collections criadas
{% highlight python %}
> show collections
dados
times
{% endhighlight %}

* Excluindo uma collection
{% highlight python %}
> db.dados.drop()
true
{% endhighlight %}

* Inserindo dados em uma collection
{% highlight python %}
# _Único dado
> db.times.insert({'nome': 'Athletico Paranaense', 'cidade': 'Curitiba', 'estado': 'Paraná'})
WriteResult({ "nInserted" : 1 })

# _Vários dados em uma mesma collection. Passamos uma lista de dados. 
> db.times.insert([
    {nome: 'Atlético Goianiense', cidade: 'Goiânia', estado: 'Goiás'},
    {nome: 'Atlético Mineiro', cidade: 'Belo Horizonte', estado: 'Minas Gerais'},
    {nome: 'Bahia', cidade: 'Salvador', estado: 'Bahia'},
    {nome: 'Botafogo', cidade: 'Rio de Janeiro', estado: 'Rio de Janeiro'},
    {nome: 'Ceará', cidade: 'Fortaleza', estado: 'Ceará'},
    {nome: 'Corinthians', cidade: 'São Paulo', estado: 'São Paulo'},
    {nome: 'Coritiba', cidade: 'Curitiba', estado: 'Paraná'},
    {nome: 'Flamengo', cidade: 'Rio de Janeiro', estado: 'Rio de Janeiro'},
    {nome: 'Fluminense', cidade: 'Rio de Janeiro', estado: 'Rio de Janeiro'},
    {nome: 'Fortaleza', cidade: 'Fortaleza', estado: 'Ceará'},
    {nome: 'Goiás', cidade: 'Goiânia', estado: 'Goiás'},
    {nome: 'Grêmio', cidade: 'Porto Alegre', estado: 'Rio Grande do Sul'},
    {nome: 'Internacional', cidade: 'Porto Alegre', estado: 'Rio Grande do Sul'},
    {nome: 'Palmeiras', cidade: 'São Paulo', estado: 'São Paulo'},
    {nome: 'Red Bull Bragantino', cidade: 'Bragança Paulista', estado: 'São Paulo'},
    {nome: 'Santos', cidade: 'Santos', estado: 'São Paulo'},
    {nome: 'São Paulo', cidade: 'São Paulo', estado: 'São Paulo'},
    {nome: 'Sport', cidade: 'Recife', estado: 'Pernambuco'},
    {nome: 'Vasco da Gama', cidade: 'Rio de Janeiro', estado: 'Rio de Janeiro'}
 ])
{% endhighlight %}
 
 * Listando os dados 
{% highlight python %}
> db.times.find() # ou db.times.find({})
{ "_id" : ObjectId("5e627dc3bc5eb4b14d51a416"), "nome" : "Athletico Paranaense", "cidade" : "Curitiba", "estado" : "Paraná" }

# utilizando o `pretty()` para retornar no formato json.
> db.times.find().pretty()
{
        "_id" : ObjectId("5e627dc3bc5eb4b14d51a416"),
        "nome" : "Athletico Paranaense",
        "cidade" : "Curitiba",
        "estado" : "Paraná"
}
...
{% endhighlight %}

Vamos retornar os dados selecionando apenas as chaves que queremos exibir. Nossa estrutura se manteve `db.collection.funcao({})`, porém adicionamos ao final uma nova condição em que passamos `'chave': 1 ou true` para exibir e `'chave': 0 ou false` para ocultar. No caso informamos para exibir a chave _'nome'_ e ocultar a chave _'_id'_.
{% highlight python %}
> db.times.find({}, {'nome': 1, '_id': 0})
{ "nome" : "Athletico Paranaense" }
{ "nome" : "Atlético Goianiense" }
...
{% endhighlight %}

Para retornar os dados filtrando por um valor específico a sintaxe básica é `db.collection.find({chave: valor})`.
{% highlight python %}
> db.times.find({'cidade': 'Porto Alegre'})
{ "_id" : ObjectId("5e627dccbc5eb4b14d51a422"), "nome" : "Grêmio", "cidade" : "Porto Alegre", "estado" : "Rio Grande do Sul" }
{ "_id" : ObjectId("5e627dccbc5eb4b14d51a423"), "nome" : "Internacional", "cidade" : "Porto Alegre", "estado" : "Rio Grande do Sul" }
{% endhighlight %}

Podemos observar que estamos incluindo todo o nome no valor da chave, se tentarmos retornar apenas com fragmento do nome não conseguiríamos, por exemplo: `db.times.find({'nome': 'Vasco'})`. Para isso temos que utilizar expressão regular para realizar a consulta
{% highlight python %}
> db.times.find({'nome': /Vasco/}, {'_id': false})
{ "nome" : "Vasco da Gama", "cidade" : "Rio de Janeiro", "estado" : "Rio de Janeiro" }

# ou

> db.times.find({'nome': {$regex: 'Vasco'}}, {'_id': false, 'nome': 1, 'estado': true})
{ "nome" : "Vasco da Gama", "estado" : "Rio de Janeiro" }
{% endhighlight %}

Se tentarmos realizar a busca com a letra minúscula no nome, `db.times.find({'nome': /vasco/}`, não teria o retorno. Para normalizar passamos o parâmetro `i` ou incluímos o parâmetro `$options: 'i'`
{% highlight python %}
> db.times.find({'nome': /vasco/i}, {'_id': 0})
{ "nome" : "Vasco da Gama", "cidade" : "Rio de Janeiro", "estado" : "Rio de Janeiro" }

# ou 

> db.times.find({'nome': {'$regex': 'vasco', '$options': 'i'}}, {'_id': 0})
{ "nome" : "Vasco da Gama", "cidade" : "Rio de Janeiro", "estado" : "Rio de Janeiro" }
{% endhighlight %}

Realizando update nos dados
{% highlight python %}
> db.times.update(
    {'nome': "Atlético Mineiro"}, # filtrando pelo nome
    {'$set': {'cidade': 'BH'}}
)
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
{% endhighlight %}

Para consultas mais complexas temos que utilizar os operadores
* Lógico
    * $and
    * $not
    * $or
        
* Comparação
    $gt - maior que
    $gte - maior ou igual que
    $lt - menor que
    $lte - menor ou igual que
    $in - esteja entre uma faixa de valores
    $not - não seja o valor especificado

Note que a estrutura da sintaxe é um pouco diferente.
{% highlight python %}
> db.times.find({
    '$or': [
        {'cidade': 'BH'},
        {'cidade': 'Porto Alegre'}
    ]
})
{% endhighlight %}

## Python com MongoDB

Veremos agora como utilizar o _Python_ com _Mongo_. Temos a parte básica que é a conexão com o banco
{% highlight python %}
from pymongo import MongoClient
import pprint  # Mesmo resultado do `pretty()`

client = MongoClient('localhost', 27017)
db = client['portfolio']
collection = db['times']
{% endhighlight %}

A sintaxe que utilizamos no _Mongo_ será identica a que utilizaremos em _Python_, na maioria das vezes.

* Retornando os dados
{% highlight python %}
query = collection.find()

for n in query:  # iterando os dados
    print(n)
{% endhighlight %}

* Utilizando operador lógico
{% highlight python %}
query = collection.find({
    '$or': [
        {'cidade': 'BH'},
        {'cidade': 'Porto Alegre'}
    ]
})
{% endhighlight %}

* Utilizando expressão regular
{% highlight python %}
query = collection.find(
    {'nome': 
        {'$regex': 'Nac', '$options': 'i'}
    },
    {'_id': 0}
)
{% endhighlight %}

Para realizarmos o update através do _Python_ utilizamos `update_one()` ou `update_many()`, caso utilizamos apenas `update()` recebemos a mensagem de que essa função foi descontinuada.
{% highlight python %}
query = collection.update_one(
    {'cidade': 'BH'},
    {'$set': {'cidade': 'Belo Horizonte'}}
)
{% endhighlight %}

Então é isso, pessoal. Claro que não abordamos todas as funções relacionadas ao _MongoDB_, pois ficaria muito extenso e esse não era nosso intuito. 

Nos vemos em uma próxima, até logo!
