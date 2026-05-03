# Roteiro De Apresentacao Do MVP - 5 Minutos

## 0:00 - 0:30 | Contexto

Objetivo do MVP:

- Micro-API de tarefas em FastAPI.
- CRUD de tarefas.
- Priorizacao assistida por IA opcional.
- Fallback local sem custo quando nao houver chave de API.
- Testes automatizados cobrindo service, rotas, app principal e advisor.

Comando:

```bash
git log --oneline -5
```

## 0:30 - 1:10 | Estrutura Do Projeto

Mostrar camadas principais:

```bash
tree /F app tests docs
```

Se `tree` nao estiver disponivel:

```bash
dir app /s
dir tests /s
```

Pontos para comentar:

- `app/api`: rotas HTTP.
- `app/models`: contratos Pydantic.
- `app/services`: regras de negocio e prioridade.
- `app/repositories`: persistencia em memoria.
- `tests`: cobertura automatizada.
- `docs`: escopo, backlog e diagrama.

## 1:10 - 1:50 | Testes Automatizados

Rodar a suite completa:

```bash
python -m pytest
```

Resultado esperado:

```text
31 passed
```

Pontos para comentar:

- CRUD de tarefas.
- Casos `201`, `200`, `204`, `404` e `422`.
- Fallback do `PriorityAdvisor`.
- Registro das rotas no app principal.
- Health check.

## 1:50 - 2:20 | Subir API

Rodar a API:

```bash
python -m uvicorn app.main:app --reload
```

Abrir documentacao interativa:

```text
http://127.0.0.1:8000/docs
```

Health check em outro terminal:

```bash
curl http://127.0.0.1:8000/health
```

## 2:20 - 3:20 | Fluxo CRUD

Criar tarefa manual:

```bash
curl -X POST http://127.0.0.1:8000/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Preparar release\",\"description\":\"Validar testes\",\"priority\":\"alta\"}"
```

Listar tarefas:

```bash
curl http://127.0.0.1:8000/tasks
```

Atualizar tarefa:

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"status\":\"concluida\"}"
```

Consultar tarefa:

```bash
curl http://127.0.0.1:8000/tasks/1
```

Remover tarefa:

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

Validar remocao:

```bash
curl http://127.0.0.1:8000/tasks/1
```

Resultado esperado:

```json
{"detail":"Task not found"}
```

## 3:20 - 4:10 | Prioridade Assistida

Criar tarefa com prioridade automatica:

```bash
curl -X POST "http://127.0.0.1:8000/tasks?auto_priority=true" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Bug urgente em producao\",\"description\":\"Falha critica bloqueia o time\",\"priority\":\"media\"}"
```

Resultado esperado:

```json
"priority": "critica"
```

Pontos para comentar:

- Sem `OPENAI_API_KEY`, usa heuristica local.
- Com `OPENAI_API_KEY`, tenta LLM.
- Timeout, erro HTTP ou resposta invalida caem no fallback local.
- O MVP nao depende de custo externo para funcionar.

Mostrar variaveis:

```bash
type .env.example
```

## 4:10 - 4:40 | Reprodutibilidade

Mostrar comandos padronizados:

```bash
type Makefile
```

Comentar:

- `make install`
- `make run`
- `make test`

Alternativa sem Make:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
python -m pytest
```

## 4:40 - 5:00 | Limites E Proximos Passos

Limites atuais:

- Persistencia em memoria.
- Sem autenticacao.
- Sem banco externo.
- Sem historico de alteracoes.
- Heuristica simples por palavras-chave.

Proximos passos:

- SQLite ou outro banco.
- Autenticacao para uso interno.
- Filtros por status e prioridade.
- Logs estruturados.
- Separar dependencias de desenvolvimento.
