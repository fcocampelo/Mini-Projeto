# Backlog do MVP

## Release 1 - Core

- [ ] RF01 - Criar tarefa
  - Criterios de aceite:
    - [ ] Deve permitir criar uma tarefa com titulo, descricao, status e prioridade.
    - [ ] Deve retornar o identificador da tarefa criada.
    - [ ] Deve validar campos obrigatorios.
    - [ ] Deve retornar erro adequado para payload invalido.

- [ ] RF02 - Listar tarefas
  - Criterios de aceite:
    - [ ] Deve retornar a lista de tarefas cadastradas.
    - [ ] Deve retornar lista vazia quando nao houver tarefas.
    - [ ] Cada item deve conter identificador, titulo, status e prioridade.

- [ ] RF03 - Consultar tarefa por ID
  - Criterios de aceite:
    - [ ] Deve retornar os dados completos de uma tarefa existente.
    - [ ] Deve retornar erro 404 quando a tarefa nao existir.

- [ ] RF04 - Atualizar tarefa
  - Criterios de aceite:
    - [ ] Deve permitir atualizar titulo, descricao, status e prioridade.
    - [ ] Deve retornar os dados atualizados da tarefa.
    - [ ] Deve retornar erro 404 quando a tarefa nao existir.
    - [ ] Deve validar valores permitidos para status e prioridade.

- [ ] RF05 - Remover tarefa
  - Criterios de aceite:
    - [ ] Deve permitir remover uma tarefa existente.
    - [ ] Deve retornar sucesso ao remover.
    - [ ] Deve retornar erro 404 quando a tarefa nao existir.

- [ ] RT01 - Endpoint de health check
  - Criterios de aceite:
    - [ ] Deve expor `GET /health`.
    - [ ] Deve retornar HTTP 200.
    - [ ] Deve retornar `status` com valor `ok`.
    - [ ] Deve retornar `timestamp` em formato ISO 8601.

## Release 2 - Qualidade

- [ ] RT02 - Modelos tipados com validacao
  - Criterios de aceite:
    - [ ] Deve usar modelos Pydantic para entradas e saidas da API.
    - [ ] Deve validar campos obrigatorios.
    - [ ] Deve validar valores permitidos para status.
    - [ ] Deve validar valores permitidos para prioridade.

- [ ] RT03 - Testes automatizados minimos
  - Criterios de aceite:
    - [ ] Deve conter teste para `GET /health`.
    - [ ] Deve conter testes para criacao de tarefa.
    - [ ] Deve conter testes para listagem de tarefas.
    - [ ] Deve conter teste para consulta de tarefa inexistente.
    - [ ] Todos os testes devem executar com um unico comando.

- [ ] RT04 - Organizacao da estrutura do projeto
  - Criterios de aceite:
    - [ ] Deve separar rotas, modelos e regras basicas de negocio.
    - [ ] Deve manter `app/main.py` como ponto de entrada da aplicacao.
    - [ ] Deve evitar logica de dominio concentrada diretamente em `main.py`.

- [ ] RT05 - Documentacao de execucao local
  - Criterios de aceite:
    - [ ] README deve informar como criar e ativar ambiente virtual.
    - [ ] README deve informar como instalar dependencias.
    - [ ] README deve informar como executar a API localmente.
    - [ ] README deve informar como acessar `/docs` e `/health`.

- [ ] RT06 - Padronizacao de versionamento
  - Criterios de aceite:
    - [ ] Commits devem seguir Conventional Commits.
    - [ ] Arquivos locais, caches e ambiente virtual nao devem ser versionados.
    - [ ] O projeto deve conter `.gitignore` adequado para Python/FastAPI.

## Release 3 - Entrega Final

- [ ] RF06 - Priorizacao manual de tarefas
  - Criterios de aceite:
    - [ ] Deve permitir definir prioridade como baixa, media, alta ou critica.
    - [ ] Deve permitir listar tarefas ordenadas por prioridade.
    - [ ] Deve rejeitar prioridades invalidas.

- [ ] RF07 - Status de tarefa
  - Criterios de aceite:
    - [ ] Deve permitir definir status como pendente, em andamento, concluida ou cancelada.
    - [ ] Deve permitir filtrar tarefas por status.
    - [ ] Deve rejeitar status invalidos.

- [ ] RF08 - Preparacao para priorizacao assistida por IA
  - Criterios de aceite:
    - [ ] Deve existir contrato definido para futura sugestao de prioridade.
    - [ ] Deve documentar criterios previstos para priorizacao assistida.
    - [ ] Deve manter a integracao real com IA fora do MVP inicial.

- [ ] RT07 - Revisao final da documentacao
  - Criterios de aceite:
    - [ ] README deve refletir a estrutura real do projeto.
    - [ ] Documento de escopo deve estar alinhado com o backlog.
    - [ ] Backlog deve conter releases, IDs e criterios de aceite.
    - [ ] Instrucoes de execucao devem ter sido validadas localmente.

- [ ] RT08 - Validacao final da API
  - Criterios de aceite:
    - [ ] API deve iniciar sem erro.
    - [ ] `/health` deve responder corretamente.
    - [ ] `/docs` deve abrir a documentacao interativa.
    - [ ] Testes automatizados minimos devem passar.
