# Desafio Alpha

Construa uma API, que responda JSON, para conversão monetária. Ela deve ter uma moeda de lastro (USD) e fazer conversões entre diferentes moedas com cotações de verdade e atuais.

A API deve converter entre as seguintes moedas:
- USD
- BRL
- EUR
- BTC
- ETH


Ex: USD para BRL, USD para BTC, ETH para BRL, etc...

A primeira requisição deve receber como parâmetros: A moeda de origem, o valor a ser convertido e a moeda final.

Ex: `?from=BTC&to=EUR&amount=123.45`

A segunda requisição deve receber um get e gerar um download conforme mime-type passado como parâmetro: A moeda de origem, o valor a ser convertido, a moeda final e o mime-type.

Ex: `?from=BTC&to=EUR&amount=123.45&type=csv`

A terceira requisição é construir um listview que vai listar a cotação do dia das moedas aqui pedidas.

Você precisa usar:
- Python

Você pode usar qualquer _framework_. Se a sua escolha for por um _framework_ que resulte em _boilerplate code_, por favor assinale no README qual pedaço de código foi escrito por você. Quanto mais código feito por você, mais conteúdo teremos para avaliar.

## Requisitos
- Forkar esse desafio e criar o seu projeto (ou workspace) usando a sua versão desse repositório, tão logo acabe o desafio, submeta um *pull request*.
- O código precisa rodar em macOS ou Ubuntu (preferencialmente como container Docker)
- Para executar seu código, deve ser preciso apenas rodar os seguintes comandos:
  - git clone $seu-fork
  - cd $seu-fork
  - comando para instalar dependências
  - comando para executar a aplicação
- A API precisa suportar um volume de 1000 requisições por segundo em um teste de estresse.
- Por fim você precisa fazer o deploy dessa aplicação no heroku.


## Critério de avaliação

- **Organização do código**: Separação de módulos, view e model, back-end e front-end
- **Clareza**: O README explica de forma resumida qual é o problema e como pode rodar a aplicação?
- **Acertividade**: A aplicação está fazendo o que é esperado? Se tem algo faltando, o README explica o porquê?
- **Legibilidade do código** (incluindo comentários)
- **Segurança**: Existe alguma vulnerabilidade clara?
- **Cobertura de testes** (Não esperamos cobertura completa)
- **Histórico de commits** (estrutura e qualidade)
- **UX**: A interface é de fácil uso e auto-explicativa? A API é intuitiva?
- **Escolhas técnicas**: A escolha das bibliotecas, banco de dados, arquitetura, etc, é a melhor escolha para a aplicação?

## Dúvidas

Quaisquer dúvidas que você venha a ter, consulte as [_issues_](https://github.com/Leeaandrob/challenge-alpha/issues) para ver se alguém já não a fez e caso você não ache sua resposta, abra você mesmo uma nova issue!

Boa sorte e boa viagem! ;)
