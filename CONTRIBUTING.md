# Contribuindo

Este documento define o fluxo de trabalho utilizado no desenvolvimento do projeto.

## 1. Escolhendo uma tarefa

- Escolha uma issue com status `Ready`.
- Priorize as tarefas na ordem: `P0` → `P1` → `P2`.
- Verifique se a tarefa não depende de outra que ainda esteja em desenvolvimento.
- Atribua a issue a você.
- Mova a issue para `In Progress`.

## 2. Iniciando o desenvolvimento

- Atualize sua branch `main`.
- Crie uma nova branch a partir da `main`.
- Utilize um dos seguintes padrões:

```text
feature/nome-da-feature
fix/nome-da-correcao
refactor/nome-da-refatoracao
```

## 3. Durante o desenvolvimento

- Mantenha as alterações dentro do escopo da issue.
- Faça commits pequenos e coerentes.
- Escreva as mensagens de commit em inglês.
- Mantenha os testes existentes passando.
- Adicione testes para novas regras de negócio, validações e alterações no banco quando necessário.

## 4. Finalizando uma tarefa

Antes de abrir o Pull Request:

- Execute os testes.
- Faça uma verificação manual da funcionalidade quando necessário.
- Faça o push da branch para o GitHub.
- Abra um Pull Request para a `main`.
- Vincule a issue correspondente ao Pull Request.
- Mova a issue para `In Review`.
- Solicite a revisão do outro desenvolvedor.

## 5. Code Review

- O Pull Request deve ser revisado pelo desenvolvedor que não realizou a implementação.
- Verifique se a implementação atende aos critérios de aceite da issue.
- Verifique se não existem alterações desnecessárias fora do escopo.
- Verifique se os testes estão passando.
- Caso sejam necessárias alterações, o autor deve realizá-las na mesma branch e atualizar o Pull Request.
- Quando estiver tudo correto, o Pull Request pode ser aprovado.

## 6. Merge

Após a aprovação:

- Faça o merge do Pull Request na `main`.
- Exclua a branch utilizada.
- Mova a issue para `Done`.

Depois disso, o desenvolvedor pode escolher uma nova tarefa com status `Ready` e repetir o fluxo.
