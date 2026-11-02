# Unidade III: matriz de casos de teste de integração gerados com GenAI

**Repositório base:** https://github.com/fcocampelo/Mini-Projeto
**Cenário:** cliente HTTP -> FastAPI -> TaskService -> TaskRepository (memória) + PriorityAdvisor (heurística ou LLM opcional).
**LLM:** ChatGPT. **Data:** 02/11/2026.
**Estado:** cenários gerados com apoio de LLM e revisados contra o código do projeto. Os resultados a seguir são **esperados**, não um relatório de testes executados.
**Artefato de automação proposto:** `tests/test_integracao_unidade_iii.py` (Pytest + FastAPI TestClient). Os testes existentes no repositório são independentes deste material.

## Grupo 1: fluxo funcional (prompt 01)

| ID | Objetivo / pré-condição | Ação HTTP / dados de entrada | Resultado e verificação esperada |
| --- | --- | --- | --- |
| IT-F01 | Criar tarefa e verificar persistência; estado limpo | `POST /tasks` `{"title":"Preparar relatorio"}`; depois `GET /tasks/{id}` | `201` com `id`, `created_at`, `status=pendente`, `priority=media`; GET `200`, mesmos dados. |
| IT-F02 | Listar duas tarefas; estado limpo | Dois `POST /tasks` válidos; `GET /tasks` | Cada POST `201`; GET `200` com dois IDs distintos e os dois títulos. |
| IT-F03 | Atualização parcial preserva outros campos; uma tarefa criada | `PUT /tasks/{id}` `{"status":"concluida"}`; depois GET | PUT `200`; GET `200`, status alterado, título, descrição e prioridade originais preservados, `updated_at` preenchido. |
| IT-F04 | Excluir tarefa existente; estado limpo | Criar, `DELETE /tasks/{id}`, depois `GET /tasks/{id}` | DELETE `204` sem corpo; GET `404` `Task not found`. |
| IT-F05 | Limite mínimo e máximo de título; estado limpo | `POST /tasks` com títulos de exatamente 3 e 120 caracteres | Ambos `201`; GET de cada ID confirma o título integral. |
| IT-F06 | Normalizar título com espaços; estado limpo | `POST /tasks` com `{"title":"  Tarefa ajustada  "}`; depois GET | `201`; título retornado e persistido sem espaços externos. |
| IT-F07 | Preservar descrição e prioridade ao atualizar só título; uma tarefa criada | `PUT /tasks/{id}` `{"title":"Titulo revisado"}`; depois GET | `200`; GET mostra novo título e mantém descrição e prioridade. |
| IT-F08 | Não sobrescrever prioridade manual; sem chamada externa | `POST /tasks?auto_priority=false` `{"title":"Resolver urgente","priority":"baixa"}`; depois GET | `201`; prioridade continua `baixa`, apesar de palavra urgente. |

## Grupo 2: negativos e resiliência (prompt 02)

| ID | Objetivo / pré-condição | Ação HTTP / dados de entrada | Resultado e verificação esperada |
| --- | --- | --- | --- |
| IT-R01 | Rejeitar título de 2 caracteres; estado limpo | `POST /tasks` `{"title":"ab"}`; depois `GET /tasks` | `422`; lista permanece vazia. |
| IT-R02 | Rejeitar título de 121 caracteres; estado limpo | `POST /tasks` com `title` de 121 letras; depois GET lista | `422`; nenhuma tarefa criada. |
| IT-R03 | Rejeitar prioridade fora do enum; estado limpo | `POST /tasks` `{"title":"Revisar demanda","priority":"extrema"}`; GET lista | `422`; sem persistência. |
| IT-R04 | Não modificar estado diante de PUT inválido; tarefa existente | `PUT /tasks/{id}` `{"status":"parada"}`; GET por ID | `422`; título, status e prioridade permanecem inalterados. |
| IT-R05 | Recursos inexistentes; repositório vazio | `GET`, `PUT` e `DELETE /tasks/99999` | Três respostas `404`, detalhe `Task not found`; `GET /tasks` continua vazio. |
| IT-R06 | Fallback local sem chave; remover variável OPENAI_API_KEY | `POST /tasks?auto_priority=true` `{"title":"Incidente urgente"}`; depois GET | `201`; prioridade `critica` persistida sem rede. |
| IT-R07 | Timeout da IA não interrompe criação; chave fictícia e monkeypatch de `urlopen` lançando TimeoutError | `POST /tasks?auto_priority=true` `{"title":"Erro no sistema"}`; depois GET | `201`; fallback local define `alta`; GET confirma, sem chamada real externa. |
| IT-R08 | Resposta JSON inválida da IA aciona fallback; chave fictícia e monkeypatch retornando JSON inválido | `POST /tasks?auto_priority=true` `{"title":"Atualizar documentacao"}`; depois GET | `201`; fallback define `baixa`; GET confirma, sem chamada real externa. |

## Critérios de aceitação para automatização

- Todos os testes devem criar e isolar seu próprio TaskRepository, sem IDs fixos para registros criados.
- As verificações devem atravessar a rota HTTP e consultar o estado persistido através de nova requisição.
- Nos testes de IA, a dependência externa deve ser simulada, com `OPENAI_API_KEY` fictícia ou ausente. Sem consumo de serviço real.
- Cada teste possui ID estável em comentário/docstring e não depende de ordenação de execução.
- Executar em checkout local do projeto com `python -m pytest tests/test_integracao_unidade_iii.py -v`. Registrar saída e commit SHA antes de declarar sucesso.

## Comparação da utilidade dos prompts

O primeiro direcionou a cobertura da jornada CRUD e das verificações persistidas entre requisições. O segundo ampliou a diversidade para entradas rejeitadas, ausência de objetos e falhas recuperáveis de serviço externo, sem inventar componentes ausentes. A revisão do código e o detalhamento de status, dados e observabilidade tornaram os resultados mais verificáveis que um pedido genérico de “gerar testes de API”.
