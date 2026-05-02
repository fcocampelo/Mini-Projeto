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
- HTTPX
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

## Execucao

Inicie a API localmente:

```bash
uvicorn app.main:app --reload
```

A API ficara disponivel em `http://127.0.0.1:8000`.

Documentacao interativa:

```text
http://127.0.0.1:8000/docs
```

Health check:

```http
GET /health
```

## Endpoints de tarefas

As rotas de tarefas ficam agrupadas em `/tasks`.

- `POST /tasks`: cria tarefa e retorna `201 Created`.
- `POST /tasks?auto_priority=true`: cria tarefa com prioridade sugerida.
- `GET /tasks`: lista tarefas e retorna `200 OK`.
- `GET /tasks/{task_id}`: consulta por ID e retorna `200 OK` ou `404 Not Found`.
- `PUT /tasks/{task_id}`: atualiza tarefa e retorna `200 OK` ou `404 Not Found`.
- `DELETE /tasks/{task_id}`: remove tarefa e retorna `204 No Content` ou `404 Not Found`.

## Uso da IA

Sem `OPENAI_API_KEY`, o sistema usa heuristica local. Com chave configurada, tenta consultar a LLM e usa fallback local em caso de timeout, erro HTTP, falha de rede ou resposta invalida.

Variaveis opcionais:

```text
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TIMEOUT_SECONDS=5
```

## Testes

Execute todos os testes:

```bash
pytest
```

Ou execute arquivos especificos:

```bash
pytest tests/test_task_service.py
pytest tests/test_priority_advisor.py
pytest tests/test_task_routes.py
```

## Limitacoes

- Persistencia em memoria.
- Sem autenticacao.
- Sem banco de dados externo.
- Sem historico de alteracoes.
- Sem paginacao ou filtros avancados.
- Heuristica local baseada em palavras-chave.

## Proximos passos

- Registrar o router de tarefas no ponto de entrada principal, caso ainda nao esteja registrado.
- Separar dependencias de desenvolvimento.
- Implementar banco de dados.
- Criar filtros por status e ordenacao por prioridade.
- Adicionar testes de integracao.
- Melhorar logs e observabilidade.
- Adicionar autenticacao.
- Preparar deploy.

## Versionamento

O projeto usa Conventional Commits:

```text
feat: adiciona rotas de tarefas
test: adiciona testes do service de tarefas
docs: atualiza README do projeto
```
