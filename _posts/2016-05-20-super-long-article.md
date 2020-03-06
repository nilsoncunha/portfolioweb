---
layout: post
title: "Comandos uteis em MongoDB e Python"
featured-img: shane-rounce-205187
categories: [Python, MongoDB]
---

Quem nunca esqueceu um código e perdeu algum tempo para conseguir encontar como fazer aquilo funcionar? Pois bem, também me vi assim em relação ao _MongoDB_ e utilizando o _Python_ para extrair essas informações. Com isso resolvi criar esse post com os principais comandos, borá lá? 

Começaremos explorando os comandos do _MongoDB_ e depois do _Python_, mais especificamente usando a bibloteca `pymongo`.

A sintaxe base é `db.collection.funcao()` o restante veremos mais a baixo.

* Listando os bancos já existentes
```
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
```

* Criando ou selecionando um banco já existente (Comando é o mesmo)
```
> use portfolio
switched to db portfolio
```

* Criando a collecion
    1. _Passando o parâmetro do createCollection('nome_collection')
    2. _Já inserindo os dados na collection
```
> db.createCollection("times")
{ "ok" : 1 }

> db.dados.insert({"nome": "Ciclano", "rua": "Logo ali", "bairro": "Bom começo"})
WriteResult({ "nInserted" : 1 })
```

* Consultando as collections criadas
```
> show collections
dados
times
```

* Excluindo uma collection
```
> db.dados.drop()
true
```

* Inserindo dados em uma collection
    1. _Único dado
    2. _Vários dados em uma mesma collection. Passamos uma lista de dados.
```
> db.times.insert({'nome': 'Athletico Paranaense', 'cidade': 'Curitiba', 'estado': 'Paraná'})
WriteResult({ "nInserted" : 1 })

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
 ```
 
 * Listando os dados 
 ```
 db.times.find() ou db.times.find({})
 ```
