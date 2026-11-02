# Prompt 1: geração de cenários funcionais de integração

**Tipo:** prompt contextualizado e orientado a cenários, com análise de equivalência e valores-limite.
**LLM utilizada:** ChatGPT.
**Aplicação real:** Mini-Projeto / FastAPI.

## Prompt enviado

> Você é um especialista em QA e testes de integração de APIs REST. Use exclusivamente os contratos deste Mini-Projeto, composto por FastAPI `app/api/task_routes.py`, Pydantic `app/models/task.py`, `TaskService` e `TaskRepository` em memória. Os endpoints disponíveis são POST /tasks (201), GET /tasks (200), GET /tasks/{id} (200/404), PUT /tasks/{id} (200/404) e DELETE /tasks/{id} (204/404). Em POST, `auto_priority` é falso por padrão. O título tem de 3 a 120 caracteres, a descrição até 1000; os status são pendente, em_andamento, concluida, cancelada; as prioridades são baixa, media, alta, critica. A saída inclui id, created_at e updated_at.
>
> Proponha OITO casos de teste de INTEGRAÇÃO entre rota HTTP, validação, serviço e repositório, evitando testes unitários isolados. Cubra criação/consulta, listagem, atualização parcial, exclusão/consulta posterior, limites de título (3 e 120), normalização do título e preservação de prioridade manual mesmo com palavras urgentes quando `auto_priority=false`.
>
> Para cada teste, apresente ID IT-F01 a IT-F08, pré-condição, chamada HTTP com payload, status HTTP, resposta/estado esperado e uma chamada posterior de verificação (quando houver). Não invente front-end, banco SQL, endpoints adicionais, automações nem resultados de teste executado. Faça cada caso independente e reproduzível com estado isolado.

## Refinamentos aplicados

1. O pedido inicial “gere testes do CRUD” foi detalhado com endpoints e expectativas HTTP explícitas.
2. Foi acrescentada a exigência de uma segunda requisição HTTP para confirmar a persistência em memória.
3. Foram explicitados os limites Pydantic e a exclusão de recursos que a aplicação não possui.
4. Os testes receberam IDs próprios para facilitar rastreabilidade e evitar repetição entre prompts.

**Resultado:** casos IT-F01 a IT-F08 descritos em `../casos_teste_integracao.md` e automatizados em `../../../tests/test_integracao_unidade_iii.py`.
