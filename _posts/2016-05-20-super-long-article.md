---
layout: post
title: "Comandos uteis em MongoDB e Python"
featured-img: shane-rounce-205187
categories: [Python, MongoDB]
---

Quem nunca esqueceu um código e perdeu algum tempo para conseguir encontar como fazer aquilo funcionar? Pois bem, também me vi assim em relação ao _MongoDB_ e utilizando o _Python_ para extrair essas informações. Com isso resolvi criar esse post com os principais comandos, borá lá? 

Começaremos explorando os comandos do _MongoDB_ e depois do _Python_, usando a bibloteca `pymongo`.

A sintaxe base que utilizaremos na maior parte do tempo é `db.collection.funcao()`

* Listando os bancos já existentes
{% highlight python %}
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
{% endhighlight %}

* Criando ou selecionando um banco já existente (Comando é o mesmo)
{% highlight python %}
> use portfolio
switched to db portfolio
{% endhighlight %}

* Criando a collecion
{% highlight python %}
# _Passando o parâmetro do createCollection('nome_collection')
> db.createCollection("times")
{ "ok" : 1 }

# _Já inserindo os dados na collection
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
{ "_id" : ObjectId("5e627dccbc5eb4b14d51a417"), "nome" : "Atlético Goianiense", "cidade" : "Goiânia", "estado" : "Goiás" }
...
{% endhighlight %}

Quando executamos o código acima ele nos trás os dados em linha, mas podemos utilizar `pretty()` para identar o retorno.
{% highlight python %}
> db.times.find().pretty()
{
        "_id" : ObjectId("5e627dc3bc5eb4b14d51a416"),
        "nome" : "Athletico Paranaense",
        "cidade" : "Curitiba",
        "estado" : "Paraná"
}
...
{% endhighlight %}

Perceba que, quando inserimos os dados em nossa _collection_ utilizamos apenas as chaves `nome`, `cidade` e `estado`, porém agora está aparecendo um novo campo `_id`. Esse campo o _Mongo_ se encarrega de colocar implicitamente, caso não o informamos. Para adicionar um `id` é bem simples
{% highlight python %}
> db.dados.insert({'_id': 1, 'nome': 'Fulano'})
WriteResult({ "nInserted" : 1 })
> db.dados.find()
{ "_id" : 1, "nome" : "Fulano" }
{% endhighlight %}

Agora vamos retornar os dados selecionando apenas as chaves que queremos exibir. Nossa estrutura se manteve `db.collection.funcao({})`, porém adicionamos ao final uma nova condição em que passamos `'chave': 1 ou true` para exibir e `'chave': 0 ou false` para ocultar. No caso informamos para exibir a chave _'nome'_ e ocultar a chave _'_id'_.
{% highlight python %}
> db.times.find({}, {'nome': 1, '_id': 0})
{ "nome" : "Athletico Paranaense" }
{ "nome" : "Atlético Goianiense" }
...
{% endhighlight %}

Para retornar os dados filtrando por um valor específico a sintaxe básica é `db.collection.find({chave: valor})`.
{% highlight python %}
> db.times.find({'nome': 'Atlético Mineiro'})
{ "_id" : ObjectId("5e627dccbc5eb4b14d51a418"), "nome" : "Atlético Mineiro", "cidade" : "Belo Horizonte", "estado" : "Minas Gerais" }

> db.times.find({'cidade': 'Porto Alegre'})
{ "_id" : ObjectId("5e627dccbc5eb4b14d51a422"), "nome" : "Grêmio", "cidade" : "Porto Alegre", "estado" : "Rio Grande do Sul" }
{ "_id" : ObjectId("5e627dccbc5eb4b14d51a423"), "nome" : "Internacional", "cidade" : "Porto Alegre", "estado" : "Rio Grande do Sul" }
{% endhighlight %}

Podemos observar que estamos incluindo todo o nome no valor da chave, se tentarmos retornar apenas com fragmento do nome não conseguiríamos.
{% highlight python %}
> db.times.find({'nome': 'Vasco'})
>
{% endhighlight %}

Para isso temos que utilizar expressão regular para realizar a consulta
{% highlight python %}
> db.times.find({'nome': /Vasco/}, {'_id': false})
{ "nome" : "Vasco da Gama", "cidade" : "Rio de Janeiro", "estado" : "Rio de Janeiro" }

# ou

> db.times.find({'nome': {$regex: 'Vasco'}}, {'_id': false, 'nome': 1, 'estado': true})
{ "nome" : "Vasco da Gama", "estado" : "Rio de Janeiro" }
{% endhighlight %}
