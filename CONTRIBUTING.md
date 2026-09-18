# Contributing

Este documento define o fluxo de desenvolvimento do **Personal Finance Manager**.

## Fluxo de trabalho

### 1. Escolha uma issue

Antes de começar, escolha uma issue disponível no projeto e mova para o status correspondente ao início do desenvolvimento.

Evite trabalhar em uma tarefa que já esteja sendo desenvolvida por outra pessoa.

### 2. Atualize a `main`

```bash
git checkout main
git pull
```

### 3. Crie uma branch

Crie uma branch a partir da `main` atualizada.

Exemplos:

```bash
git checkout -b feature/add-transactions-page
git checkout -b fix/purchase-edit
git checkout -b refactor/purchase-modal
```

Use nomes curtos e descritivos.

### 4. Desenvolva

Faça alterações relacionadas somente à issue escolhida.

Quando houver regra de negócio, validação ou operação de banco, priorize TDD:

```text
Teste → Implementação → Refatoração
```

Antes de finalizar, execute:

```bash
pytest
```

Também valide manualmente as telas afetadas quando necessário.

### 5. Faça o commit

Use mensagens de commit em inglês, curtas e descritivas.

Exemplos:

```bash
git commit -m "Add: transaction validation"
git commit -m "Fix: purchase date formatting"
git commit -m "Refactor: purchase modal scripts"
```

### 6. Envie a branch

```bash
git push -u origin nome-da-branch
```

### 7. Abra um Pull Request

Abra um Pull Request da sua branch para `main`.

O PR deve explicar de forma breve:

* o que foi alterado;
* como validar;
* qual issue está relacionada.

### 8. Revisão

Sempre que possível, outra pessoa deve revisar o Pull Request.

Quem criou o PR não deve fazer o merge antes da revisão quando houver outro colaborador disponível.

Se forem solicitadas alterações, faça os ajustes na mesma branch e envie novos commits.

### 9. Merge

Após aprovação e validação, faça o merge na `main`.

Depois do merge:

* exclua a branch;
* confirme que a issue foi concluída;
* atualize o status da tarefa no projeto.

## Princípios

* Mantenha as alterações simples.
* Evite mudanças fora do escopo da issue.
* Não misture refatoração e correção de bugs sem necessidade.
* Preserve código simples quando uma abstração não trouxer benefício real.
* Faça pequenas entregas incrementais.

> Feito é melhor que perfeito.
