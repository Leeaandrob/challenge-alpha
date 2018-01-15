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

__Nota__: Não foi possível realizar a implementação para a moeda _ETH_, pois não foi encontrado um webservice que 
retorne essa informação. O valor da cotação dessa moeda poderia ser obtido através do método _screen scrapping_, porém 
foi decidido deixá-la para um segundo momento e focar nas outras moedas. 

A aplicação foi construída utilizando a seguinte stack

__Backend__

* [Django 2.0.1](https://www.djangoproject.com)

A escolha do framework _Django_ se deu pela sua simplicidade, comodidade, agilidade no desenvolvimento e escalabilidade 
que o mesmo proporciona. O framework propõe um modelo para estruturação do projeto de forma que as camadas model, view 
e controller sejam construídas de forma desacoplada. Além disso, ao iniciar um projeto com _Django_, o projeto já vem 
com o setup pronto para construção de testes unitários e um mini servidor web, o que torna o desenvolvimento do 
aplicativo mais simples, pois neste momento o desenvolvedor não precisa se preocupar com a configuração de um servidor 
para a aplicação. 

* [PostgreSQL](https://www.postgresql.org)

O banco de dados _PostgreSQL_ vem se destacando por ser um banco de dados muito robusto e veloz. Além disso, é uma 
ferramenta free e que tem uma comunidade muito vasta.

__Frontend__

* [Bootstrap 4](https://v4-alpha.getbootstrap.com/)
* [Font Awesome](https://fontawesome.com/)

Esses dois frameworks foram utilizados nos layouts da aplicação. O _Bootstrap 4_ tem a sua própria proposta de layout,
contendo estilos, componentes e um sistema de grid. Já o _Font Awesome_ possui uma vasta variedade de ícones, que podem
ser utilzados para melhorar a usabilidade das páginas web. Os dois frameworks são free. 

## Dependências de ambiente

* Python >= 3.6 - Visitar página de [download](https://www.python.org/downloads/)
* Pipenv ```pip install pipenv```
* PostgreSQL >= 9.3 - Visitar página de [download](https://www.postgresql.org/download/)

## Instalando a aplicação localmente

Assumindo que as [Dependências de ambiente](https://github.com/hengling/challenge-alpha#dependências-de-ambiente) já 
tenham sido resolvidas, siga os seguintes passos para instalar e rodar a aplicação localmente.

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
acesada pelo endereço [https://amh-currency-watcher.herokuapp.com/currencies](https://amh-currency-watcher.herokuapp.com/currencies)


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
GET /convertAndDownload?from=USD&to=EUR&amount=123.45&type=csv
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