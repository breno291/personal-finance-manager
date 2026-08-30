# personal-finance-manager

A personal finance management application developed with Python, Flask and SQLite for learning and portfolio purposes.

O sistema tem como objetivo centralizar compras, parcelas, responsabilidades entre pessoas, formas de pagamento, vencimentos e estados de pagamento, substituindo gradualmente o controle realizado em planilha.

## Stack inicial

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript

A aplicação inicialmente será executada em `localhost`, através do servidor do próprio Python/Flask.

Futuramente, o projeto poderá ser empacotado como `.exe` para execução no Windows.

---

# Desenvolvimento

O projeto será desenvolvido de forma incremental utilizando **TDD (Test-Driven Development)**.

Fluxo principal:

1. Criar teste
2. Fazer o teste falhar
3. Implementar o necessário
4. Refatorar
5. Repetir

Cada etapa deve ser concluída antes de avançar para a próxima.

---

# ETAPA 1 — Banco de dados

## 1.1 Criar banco

Utilizar SQLite.

O banco será responsável por armazenar os dados da aplicação e será a fonte principal dos dados.

A planilha existente poderá ser importada futuramente.

## 1.2 Criar tabelas

### `purchases`

Representa a compra original realizada.

| Campo                | Descrição                                     |
| -------------------- | --------------------------------------------- |
| `id`                 | Identificador único                           |
| `description`        | Descrição da compra                           |
| `purchase_date`      | Data em que a compra foi realizada            |
| `value`              | Valor total da compra, armazenado em centavos |
| `total_installments` | Quantidade total de parcelas                  |
| `payment_method_id`  | Forma de pagamento utilizada                  |
| `category_id`        | Categoria da compra                           |
| `subcategory_id`     | Subcategoria da compra                        |
| `created_at`         | Data/hora de criação                          |
| `updated_at`         | Data/hora da última atualização               |
| `removed`            | Indica soft delete                            |

---

### `transactions`

Representa quanto cada pessoa é responsável por pagar em cada parcela de uma compra.

| Campo          | Descrição                                  |
| -------------- | ------------------------------------------ |
| `id`           | Identificador único                        |
| `purchase_id`  | Compra à qual pertence                     |
| `person_id`    | Pessoa responsável pelo lançamento         |
| `installment`  | Número da parcela                          |
| `value`        | Valor que a pessoa deve pagar, em centavos |
| `due_date`     | Data de vencimento                         |
| `payment_date` | Data em que foi efetivamente pago          |
| `status`       | Estado do lançamento                       |
| `removed`      | Indica soft delete                         |

### Status do lançamento

* `0` → não pago
* `1` → pago
* `2` → separado

`atrasado` não será armazenado. Será determinado pela aplicação quando a data de vencimento tiver passado e o lançamento ainda não estiver pago.

---

### `people`

Representa pessoas ou entidades que participam financeiramente das compras.

Exemplo: uma pessoa da família, outra pessoa ou a própria "Casa".

| Campo     | Descrição               |
| --------- | ----------------------- |
| `id`      | Identificador único     |
| `name`    | Nome da pessoa/entidade |
| `removed` | Indica soft delete      |

---

### `payment_methods`

Representa a forma utilizada para realizar uma compra.

| Campo          | Descrição                           |
| -------------- | ----------------------------------- |
| `id`           | Identificador único                 |
| `description`  | Nome da forma de pagamento          |
| `payment_type` | Tipo da forma de pagamento          |
| `closing_day`  | Dia de fechamento, quando aplicável |
| `due_day`      | Dia de vencimento, quando aplicável |
| `removed`      | Indica soft delete                  |

### Tipos iniciais

* `1` → à vista
* `2` → cartão

Os valores serão definidos como constantes no código para facilitar alterações futuras.

---

# Relacionamento principal

A estrutura conceitual é:

```text
Compra
  │
  ├── Forma de pagamento
  │
  └── Lançamentos
        │
        ├── Pessoa
        └── Parcela
```

Uma compra possui pelo menos um lançamento.

Uma compra pode possuir vários lançamentos.

Uma mesma compra pode possuir diferentes pessoas em diferentes parcelas.

Exemplo:

```text
Compra: R$ 500

Parcelas: 2

Parcela 1
    Pessoa A → R$ 100
    Pessoa B → R$ 150

Parcela 2
    Pessoa A → R$ 250
```

Total dos lançamentos:

`R$ 500`

A divisão não precisa ser igual entre pessoas ou entre parcelas.

---

# Regras de negócio

## `purchases`

* Toda compra possui pelo menos um lançamento.
* O valor total dos lançamentos deve corresponder ao valor da compra.
* `total_installments` pertence à compra.
* O número da parcela pertence ao lançamento.
* Uma compra pode ter diferentes divisões entre pessoas em cada parcela.

## Pagamentos

O status pertence somente aos lançamentos.

Uma compra é considerada paga quando todos os seus lançamentos ativos estão pagos.

Não haverá campo `paid` na tabela `purchases`.

Uma compra ou parcela poderá futuramente ser marcada como paga de uma só vez, fazendo a aplicação atualizar os lançamentos correspondentes.

## Separado

"Separado" significa que o dinheiro já foi reservado para aquele lançamento, mas ele ainda não foi efetivamente pago.

Será possível futuramente comparar:

* valor total dos lançamentos separados;
* valor disponível no cofrinho/reserva.

## Atrasado

Um lançamento será considerado atrasado quando:

* possuir data de vencimento;
* a data de vencimento já tiver passado;
* não estiver pago.

Não será criado um campo `overdue`.

## Datas

`purchase_date` representa o dia em que a compra aconteceu.

`due_date` representa o dia em que determinado lançamento deve ser pago.

`payment_date` representa o dia em que o pagamento realmente aconteceu.

Compras podem possuir data de vencimento mesmo quando não são realizadas com cartão.

## Cartões

Cartões possuem:

* dia de fechamento;
* dia de vencimento.

A compra realizada no próprio dia de fechamento pertence à próxima fatura.

A primeira parcela terá seu vencimento calculado com base na regra da fatura.

As parcelas seguintes terão vencimento no mesmo dia nos meses seguintes.

Não será criada uma tabela específica para faturas inicialmente.

---

# ETAPA 2 — Camada de acesso ao banco

Criar funções reutilizáveis para trabalhar com o banco.

Operações inicialmente previstas:

* Insert
* Select
* Update
* Delete

A ideia é criar uma camada de acesso aos dados que possa ser utilizada pelas funcionalidades da aplicação, evitando espalhar operações de banco pelo restante do sistema.

O formato definitivo dessas funções será definido durante a implementação.

O soft delete será utilizado nas entidades que possuem o campo `removed`.

Não é necessário implementar todas as operações imediatamente se alguma delas ainda não tiver utilidade.

---

# ETAPA 3 — Frontend básico

Nesta etapa o objetivo é criar somente a estrutura visual inicial.

Ainda não é necessário implementar as funcionalidades.

## Navegação inicial

Criar um menu com as principais áreas da aplicação:

* Lançamentos
* Compras
* Cartões
* Pessoas
* Formas de pagamento
* Gráficos

As páginas inicialmente podem conter somente seus respectivos títulos.

Exemplo:

```text
Lançamentos
```

```text
Compras
```

```text
Cartões
```

etc.

## Tela de Lançamentos

Criar inicialmente:

* título da página;
* botão "Adicionar compra";
* tabela/listagem visual dos lançamentos;
* ações de editar e excluir representadas por ícones.

Nesta etapa os botões ainda não precisam possuir funcionalidade.

## Cadastro de compra

Posteriormente, o botão "Adicionar compra" abrirá o formulário de cadastro.

O formulário deverá permitir informar:

* descrição;
* valor;
* data da compra;
* quantidade de parcelas;
* forma de pagamento;
* categoria;
* subcategoria;
* quantidade de pessoas;
* pessoa(s);
* valor de cada pessoa em cada parcela.

A divisão será inicialmente manual.

Funcionalidades como divisão igual automática e preenchimento automático de parcelas serão implementadas posteriormente.

## Edição

A edição utilizará inicialmente o mesmo formulário utilizado para criar uma compra, preenchido com os dados existentes.

A primeira versão não tentará resolver alterações complexas na estrutura dos lançamentos.

Melhorias futuras poderão tratar casos como:

* adicionar/remover pessoas;
* adicionar/remover parcelas;
* alterar responsabilidades de parcelas já existentes.

---

# TDD

Todas as funcionalidades relevantes deverão ser desenvolvidas seguindo TDD.

## Ordem geral

```text
Teste
  ↓
Implementação mínima
  ↓
Teste passando
  ↓
Refatoração
  ↓
Próximo teste
```

O TDD será aplicado principalmente às regras de negócio e à camada de acesso ao banco.

O frontend poderá ser desenvolvido de forma incremental, adicionando testes conforme fizer sentido para cada funcionalidade.

---

# Futuras funcionalidades

Estas funcionalidades não fazem parte da primeira versão:

* divisão automática igual entre pessoas;
* preenchimento automático de parcelas;
* edição complexa de lançamentos;
* dashboard;
* gráficos;
* controle de limites por categoria/subcategoria;
* comparação de dinheiro separado com reserva/cofrinho;
* importação da planilha atual;
* exportação de dados;
* execução como `.exe`;
* possibilidade de acesso aos dados por outros dispositivos;
* banco remoto para sincronização.

---

# Princípio do projeto

Priorizar uma implementação simples e funcional antes de tentar resolver todos os casos possíveis.

> Feito é melhor que perfeito.

Novas regras e melhorias devem ser adicionadas conforme necessidades reais surgirem durante o desenvolvimento.
