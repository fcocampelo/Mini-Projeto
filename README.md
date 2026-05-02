# Mini-Projeto

MVP de uma micro-API de tarefas em FastAPI, com CRUD, persistencia em memoria e sugestao opcional de prioridade assistida por IA.

## Objetivo

Validar uma base simples para gestao interna de tarefas, separando responsabilidades entre API, regras de negocio, persistencia e componente de recomendacao de prioridade.

O projeto foi desenhado para rodar localmente sem custo de API externa. Quando `OPENAI_API_KEY` nao estiver configurada, a prioridade sugerida usa apenas uma heuristica local.

## Stack

- Python
- FastAPI
- Pydantic v2
- Uvicorn
- Pytest
- Git

## Funcionalidades

- Criar tarefas
- Listar tarefas
- Consultar tarefa por ID
- Atualizar tarefas
- Remover tarefas
- Validar campos com modelos Pydantic
- Sugerir prioridade com heuristica local
- Usar LLM opcionalmente quando houver `OPENAI_API_KEY`
- Aplicar fallback seguro quando a chamada externa falhar
- Expor health check da API

## Arquitetura

O projeto segue uma organizacao em camadas:

```text
app/
+-- api/
|   +-- task_routes.py
+-- models/
|   +-- task.py
+-- repositories/
|   +-- task_repository.py
+-- services/
|   +-- priority_advisor.py
|   +-- task_service.py
+-- main.py
```

### Camadas

- `app/main.py`: ponto de entrada da aplicacao FastAPI e health check.
- `app/api/task_routes.py`: rotas HTTP de tarefas.
- `app/models/task.py`: contratos de entrada e saida com Pydantic.
- `app/services/task_service.py`: regras de negocio e orquestracao do CRUD.
- `app/services/priority_advisor.py`: sugestao de prioridade com heuristica local e LLM opcional.
- `app/repositories/task_repository.py`: persistencia inicial em memoria.

O fluxo principal e:

```text
Cliente HTTP -> FastAPI Router -> TaskService -> PriorityAdvisor
                                      |
                                      v
                              TaskRepository
```

O diagrama Mermaid versionado esta em:

```text
docs/componentes-fluxo-dados.mmd
```

## Instalacao

Clone o repositorio e acesse a pasta do projeto:

```bash
git clone <url-do-repositorio>
cd Mini-Projeto
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Para executar os testes, instale tambem o Pytest caso ele ainda nao esteja no ambiente:

```bash
pip install pytest
```

## Execucao

Inicie a API localmente:

```bash
uvicorn app.main:app --reload
```

A API ficara disponivel em:

```text
http://127.0.0.1:8000
```

Documentacao interativa:

```text
http://127.0.0.1:8000/docs
```

Health check:

```http
GET /health
```

Resposta esperada:

```json
{
  "status": "ok",
  "timestamp": "2026-05-02T12:00:00+00:00"
}
```

## Endpoints de tarefas

As rotas de tarefas ficam agrupadas em `/tasks`.

### Criar tarefa

```http
POST /tasks
```

Exemplo de corpo:

```json
{
  "title": "Implementar endpoint de tarefas",
  "description": "Criar fluxo inicial de cadastro",
  "status": "pendente",
  "priority": "alta"
}
```

Resposta esperada:

```http
201 Created
```

### Criar tarefa com prioridade automatica

```http
POST /tasks?auto_priority=true
```

Quando `auto_priority=true`, o `TaskService` solicita uma sugestao ao `PriorityAdvisor`. Se nao houver chave de API ou se a chamada externa falhar, a heuristica local sera usada.

### Listar tarefas

```http
GET /tasks
```

Resposta esperada:

```http
200 OK
```

### Consultar tarefa por ID

```http
GET /tasks/{task_id}
```

Respostas esperadas:

```http
200 OK
404 Not Found
```

### Atualizar tarefa

```http
PUT /tasks/{task_id}
```

Exemplo de corpo:

```json
{
  "title": "Implementar CRUD de tarefas",
  "status": "em_andamento",
  "priority": "critica"
}
```

Respostas esperadas:

```http
200 OK
404 Not Found
```

### Remover tarefa

```http
DELETE /tasks/{task_id}
```

Respostas esperadas:

```http
204 No Content
404 Not Found
```

## Modelos principais

### Status permitidos

- `pendente`
- `em_andamento`
- `concluida`
- `cancelada`

### Prioridades permitidas

- `baixa`
- `media`
- `alta`
- `critica`

## Uso da IA

O componente `PriorityAdvisor` funciona em dois modos.

### Sem chave de API

Se `OPENAI_API_KEY` nao estiver configurada, o sistema usa apenas heuristica local.

Exemplos de criterios:

- termos como `urgente`, `producao`, `bloqueio` e `seguranca` tendem a gerar prioridade `critica`;
- termos como `bug`, `cliente`, `prazo`, `hoje` e `release` tendem a gerar prioridade `alta`;
- termos como `documentacao`, `refatorar` e `melhoria` tendem a gerar prioridade `baixa`;
- quando nenhum criterio se aplica, a prioridade informada na tarefa e preservada.

### Com chave de API

Configure a chave antes de iniciar a aplicacao:

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="sua-chave"
```

Linux/macOS:

```bash
export OPENAI_API_KEY="sua-chave"
```

Variaveis opcionais:

```text
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TIMEOUT_SECONDS=5
```

Mesmo com chave configurada, a aplicacao mantem fallback obrigatorio para a heuristica local em caso de timeout, erro HTTP, falha de rede ou resposta invalida.

## Testes

Execute todos os testes:

```bash
pytest
```

Ou execute um arquivo especifico:

```bash
pytest tests/test_task_service.py
pytest tests/test_priority_advisor.py
pytest tests/test_task_routes.py
```

Coberturas principais:

- CRUD no `TaskService`;
- heuristica e fallback do `PriorityAdvisor`;
- rotas `/tasks` com status `201`, `200`, `204` e `404`.

## Documentacao do projeto

Arquivos complementares:

- `docs/escopo-mvp.md`: escopo funcional e nao funcional do MVP.
- `docs/backlog.md`: backlog organizado por releases.
- `docs/componentes-fluxo-dados.mmd`: diagrama Mermaid de componentes e fluxo de dados.

## Limitacoes

- A persistencia e em memoria; os dados sao perdidos ao reiniciar a aplicacao.
- Nao ha autenticacao ou autorizacao.
- Nao ha banco de dados externo.
- Nao ha historico de alteracoes de tarefas.
- Nao ha paginacao, filtros avancados ou ordenacao por prioridade.
- A heuristica local e simples e baseada em palavras-chave.
- A chamada a LLM e opcional e deve ser usada apenas quando houver chave configurada.

## Proximos passos

- Incluir o router de tarefas no ponto de entrada principal da aplicacao, caso ainda nao esteja registrado.
- Adicionar `pytest` ao `requirements.txt` ou separar dependencias de desenvolvimento.
- Implementar persistencia com banco de dados.
- Criar filtros por status e ordenacao por prioridade.
- Adicionar testes de integracao da aplicacao completa.
- Melhorar observabilidade com logs estruturados.
- Adicionar autenticacao para uso interno por equipe.
- Preparar configuracao de deploy.

## Versionamento

O projeto usa Git e mensagens no padrao Conventional Commits.

Exemplos:

```text
feat: adiciona rotas de tarefas
test: adiciona testes do service de tarefas
docs: atualiza README do projeto
```
