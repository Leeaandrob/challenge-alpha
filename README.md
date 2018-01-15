# Currency Watcher - Desafio Alpha

## Sumário

* [Introdução](https://github.com/hengling/challenge-alpha#introdução)
* [Dependências de ambiente](https://github.com/hengling/challenge-alpha#dependências-de-ambiente)
* [Instalando a aplicação localmente](https://github.com/hengling/challenge-alpha#instalando-a-aplicação-localmente)
* [Instalando a aplicação como container Docker](https://github.com/hengling/challenge-alpha#instalando-a-aplicação-como-container-docker)
* [Acessando a aplicação no Heroku](https://github.com/hengling/challenge-alpha#acessando-a-aplicação-no-heroku)
* [API - Serviços disponíveis](https://github.com/hengling/challenge-alpha#api---serviços-dispon%C3%ADveis)

## Introdução

_Currency Watcher_ é uma API para conversão monetária. As taxas de conversão entre as moedas suportadas pela aplicação 
são atualizadas uma vez por dia e depois armazenadas no banco de dados. Essas taxas de conversão são consumidas da
API [Currency Layer](https://currencylayer.com). 

As moedas suportadas são:
- USD
- BRL
- EUR
- BTC


Ex: USD para BRL, USD para BTC, EUR para BRL, etc...

A aplicação foi construída utilizando o framework [Django 2.0.1](https://www.djangoproject.com) e banco de dados 
[PostgreSQL](https://www.postgresql.org). O layout dos templates utiliza os frameworks 
[Bootstrap 4](https://v4-alpha.getbootstrap.com/) e [Font Awesome](https://fontawesome.com/).

## Dependências de ambiente

* Python >= 3.6 - Visitar página de [download](https://www.python.org/downloads/)
* Pipenv ```pip install pipenv```
* PostgreSQL >= 9.3 - Visitar página de [download](https://www.postgresql.org/download/)

## Instalando a aplicação localmente

Assumindo que as [Dependências de ambiente]() já tenham sido resolvidas, siga os seguintes passos para instalar e rodar
a aplicação localmente.

Defina as seguintes variáveis de ambiente:

| Variável              | Descrição                                                                     | Exemplo                                  |
| --------------------- | ----------------------------------------------------------------------------- | ---------------------------------------- |
| CURR_LAYER_ACCESS_KEY | Chave de acesso para a API que fornece a taxa de conversão das moedas.        | 52671idbvc526eqq34f                      |
| DATABASE_URL          | Url de acesso ao banco que contém host, porta, usuário, senha e nome do banco | postgres://user:passwd@host:port/db_name |

Clone o repositório e entre na pasta do projeto
```
git clone https://github.com/hengling/challenge-alpha.git
cd challenge-alpha
```

Instale as dependências do projeto
```
pipenv install
```

Execute os testes unitários
```
python manage.py test
```

Execute o programa
```
python manage.py runserver
```

Se as configurações padrão não tiverem sido alteradas, o sistema estará disponível no endereço 
[http://127.0.0.1:8000/currencies/](http://127.0.0.1:8000/currencies/)

## Instalando a aplicação como container Docker

_TODO_

## Acessando a aplicação no Heroku

A aplicação também foi liberada utilizando o provedor de cloud computing [Heroku](https://heroku.com) e pode ser
acesada pelo endereço [https://amh-currency-watcher.herokuapp.com/currencies/](https://amh-currency-watcher.herokuapp.com/currencies/)


## API - Serviços disponíveis

__Serviço para conversão de valores com retorno em Json__
```
GET /convert?from=USD&to=EUR&amount=123.45
```

Parâmetros

* from: moeda de origem
* to: moeda final
* amount: valor a ser convertido

Resposta
```
{
    "from": "USD",
    "to": "EUR",
    "originalValue": 123.45,
    "convertedValue": 101.2038162,
    "ratesLastUpdatedAt": "14/01/2018 21:24"
}
```

* from: moeda de origem
* to: moeda final
* originalValue: valor na moeda de origem
* convertedValue: valor na moeda final
* ratesLastUpdatedAt: data da última atualização das taxas de conversão 

__Serviço para conversão de valores com retorno em arquivo__

```
GET /convertAndDownload?from=BTC&to=EUR&amount=123.45&type=csv
```

Parâmetros

* from: moeda de origem
* to: moeda final
* amount: valor a ser convertido
* type: formato do arquivo (csv | pdf)

Resposta

Download do arquivo com as informações.

__Listagem das moedas com a cotação atual (em BRL)__

```
GET /currencies
```

Resposta

Página com a listagem das moedas, cotação em _BRL_ e data da última atualização das taxas de conversão.