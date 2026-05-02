# Mini-Projeto

MVP de uma micro-API de tarefas em FastAPI, com CRUD, persistencia em memoria e sugestao opcional de prioridade assistida por IA.

## Objetivo

Validar uma base simples para gestao interna de tarefas, separando responsabilidades entre API, regras de negocio, persistencia e componente de recomendacao de prioridade.

O projeto roda localmente sem chave de API externa. Quando `OPENAI_API_KEY` nao estiver configurada, a prioridade sugerida usa apenas uma heuristica local, sem custo.

## Requisitos

- Python 3.14 ou versao compativel com as dependencias do projeto
- Git
- Make opcional

## Stack

- Python
- FastAPI
- Pydantic v2
- Uvicorn
- Pytest
- HTTPX

## Funcionalidades

- Criar, listar, consultar, atualizar e remover tarefas.
- Validar contratos de entrada e saida com Pydantic.
- Sugerir prioridade por heuristica local.
- Usar LLM opcionalmente quando `OPENAI_API_KEY` existir.
- Aplicar fallback seguro quando a chamada externa falhar.
- Expor health check em `/health`.

## Arquitetura

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

Responsabilidades:

- `app/main.py`: cria a aplicacao FastAPI, registra rotas e expoe `/health`.
- `app/api/task_routes.py`: define os endpoints HTTP de `/tasks`.
- `app/models/task.py`: define modelos Pydantic, status e prioridades validas.
- `app/services/task_service.py`: concentra regras de negocio de tarefas.
- `app/services/priority_advisor.py`: sugere prioridade por heuristica local ou LLM opcional.
- `app/repositories/task_repository.py`: guarda tarefas em memoria.

Fluxo principal:

```text
Cliente HTTP -> FastAPI Router -> TaskService -> TaskRepository
                                      |
                                      v
                              PriorityAdvisor
```

Diagrama Mermaid:

```text
docs/componentes-fluxo-dados.mmd
```

## Setup Em Maquina Limpa

Clone o repositorio:

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
python -m pip install -r requirements.txt
```

Configure variaveis opcionais:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Valide a instalacao:

```bash
python -m pytest
```

Resultado esperado:

```text
31 passed
```

## Comandos

Com Make:

```bash
make install
make run
make test
```

Sem Make:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
python -m pytest
```

## Execucao

Inicie a API:

```bash
python -m uvicorn app.main:app --reload
```

A API fica disponivel em:

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

## Uso Como Cliente

Criar tarefa:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Preparar release\",\"description\":\"Validar testes\",\"priority\":\"alta\"}"
```

Criar tarefa com prioridade automatica:

```bash
curl -X POST "http://127.0.0.1:8000/tasks?auto_priority=true" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Bug urgente em producao\",\"description\":\"Falha critica bloqueia o time\",\"priority\":\"media\"}"
```

Listar tarefas:

```bash
curl http://127.0.0.1:8000/tasks
```

Consultar por ID:

```bash
curl http://127.0.0.1:8000/tasks/1
```

Atualizar tarefa:

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"concluida\"}"
```

Remover tarefa:

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Endpoints

- `GET /health`: verifica se a API esta ativa.
- `POST /tasks`: cria tarefa e retorna `201 Created`.
- `POST /tasks?auto_priority=true`: cria tarefa usando sugestao de prioridade.
- `GET /tasks`: lista tarefas e retorna `200 OK`.
- `GET /tasks/{task_id}`: consulta por ID e retorna `200 OK` ou `404 Not Found`.
- `PUT /tasks/{task_id}`: atualiza tarefa e retorna `200 OK` ou `404 Not Found`.
- `DELETE /tasks/{task_id}`: remove tarefa e retorna `204 No Content` ou `404 Not Found`.

## Modelos

Status validos:

- `pendente`
- `em_andamento`
- `concluida`
- `cancelada`

Prioridades validas:

- `baixa`
- `media`
- `alta`
- `critica`

## Uso Da IA

A IA e opcional. A API funciona normalmente sem `OPENAI_API_KEY`.

Variaveis:

```text
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TIMEOUT_SECONDS=5
```

Comportamento:

- Sem chave: usa apenas heuristica local.
- Com chave: tenta consultar a LLM.
- Em timeout, erro HTTP, falha de rede ou resposta invalida: usa fallback local.
- Respostas da LLM so sao aceitas quando indicam uma prioridade valida.

Exemplo local sem custo:

```json
{
  "title": "Bug urgente em producao",
  "description": "Falha critica bloqueia o time",
  "priority": "media"
}
```

Com `auto_priority=true`, termos como `urgente`, `producao`, `falha critica` e `bloqueia` tendem a resultar em prioridade `critica`.

## Testes

Rodar tudo:

```bash
python -m pytest
```

Rodar por camada:

```bash
python -m pytest tests/test_task_service.py
python -m pytest tests/test_priority_advisor.py
python -m pytest tests/test_task_routes.py
python -m pytest tests/test_app.py
```

Cobertura atual:

- Service de tarefas.
- Repository em memoria via service.
- Advisor de prioridade com heuristica, resposta LLM simulada e fallback.
- Endpoints de `/tasks` com `201`, `200`, `204`, `404` e `422`.
- Registro das rotas no app principal.
- Health check.

## Como Evoluir

- Nova regra de negocio: altere `app/services/task_service.py`.
- Nova validacao de contrato: altere `app/models/task.py`.
- Nova rota HTTP: altere ou crie arquivos em `app/api/`.
- Nova forma de persistencia: substitua `app/repositories/task_repository.py`.
- Nova estrategia de prioridade: altere `app/services/priority_advisor.py`.

## Limitacoes

- Persistencia em memoria; dados somem ao reiniciar a API.
- Sem autenticacao.
- Sem banco de dados externo.
- Sem historico de alteracoes.
- Sem paginacao ou filtros avancados.
- Heuristica local baseada em palavras-chave.

## Proximos Passos

- Separar dependencias de desenvolvimento.
- Implementar banco de dados.
- Criar filtros por status e ordenacao por prioridade.
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
