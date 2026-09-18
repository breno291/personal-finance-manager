# Personal Finance Manager

Sistema de gerenciamento financeiro pessoal desenvolvido para aprendizado e portfólio.

O projeto centraliza compras, parcelas, responsáveis, formas de pagamento e pagamentos, substituindo gradualmente o controle feito em planilhas.

## Tecnologias

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript
* Pytest
* DataTables

## Funcionalidades

Atualmente o sistema permite gerenciar:

* pessoas;
* formas de pagamento;
* compras;
* parcelas e responsáveis por cada compra.

Uma compra é composta pelos seus lançamentos. Ao cadastrar uma compra, também são definidos os lançamentos responsáveis pela distribuição do seu valor.

Exemplo:

```text
Compra: R$ 300,00
Parcelas: 2

Parcela 1
Breno   → R$ 100,00
Luciana → R$ 50,00

Parcela 2
Breno   → R$ 150,00
```

A soma dos lançamentos deve corresponder ao valor total da compra.

## Regras principais

* Valores monetários são armazenados em centavos.
* Registros utilizam soft delete quando aplicável.
* Uma compra deve possuir pelo menos um lançamento.
* O valor distribuído nos lançamentos deve corresponder ao valor da compra.
* Cada parcela pode ser dividida entre diferentes pessoas.
* Formas de pagamento podem possuir fechamento e vencimento.
* Compras realizadas no dia do fechamento do cartão entram na próxima fatura.
* O status de pagamento pertence aos lançamentos.

### Status dos lançamentos

```text
0 → Não pago
1 → Pago
2 → Separado
```

Um lançamento vencido e ainda não pago é considerado atrasado pela aplicação.

## Estrutura

```text
app/
├── database/     # Acesso e operações no banco
├── routes/       # Rotas Flask
├── services/     # Validações e formatação
├── static/       # CSS, JavaScript e imagens
└── templates/    # Templates HTML

tests/            # Testes automatizados
```

## Executando o projeto

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
flask --app app run
```

Depois acesse:

```text
http://127.0.0.1:5000
```

## Testes

O projeto utiliza Pytest:

```bash
pytest
```

As regras de negócio e operações de banco são desenvolvidas de forma incremental utilizando TDD.

```text
Teste → Implementação → Refatoração → Próxima funcionalidade
```

## Desenvolvimento

O projeto prioriza soluções simples e incrementais.

Novas funcionalidades e regras são adicionadas conforme necessidades reais surgem durante o desenvolvimento.

> Feito é melhor que perfeito.

Para detalhes sobre o fluxo de contribuição e desenvolvimento, consulte `CONTRIBUTING.md`.
