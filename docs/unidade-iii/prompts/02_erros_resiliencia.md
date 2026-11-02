# Prompt 2: geração de casos negativos e resiliência

**Tipo:** prompt baseado em riscos e contratos, voltado a casos de erro, integração com dependência externa e fallback.
**LLM utilizada:** ChatGPT.
**Aplicação real:** Mini-Projeto / FastAPI / PriorityAdvisor.

## Prompt enviado

> Aja como QA especializado em falhas de integração. Considere o mesmo Mini-Projeto FastAPI e seu fluxo HTTP -> TaskService -> (TaskRepository, PriorityAdvisor). Quando POST /tasks usa `auto_priority=true`, o PriorityAdvisor tenta a OpenAI Responses API apenas se houver `OPENAI_API_KEY`; sem chave, usa heurística local. O fallback local também é usado se a chamada externa lançar erros HTTP, URL, timeout ou devolver resposta inválida. A heurística classifica termo `urgente` como critica, `erro` como alta e `documentacao` como baixa. Com `auto_priority=false` preserva-se a prioridade fornecida. Payloads fora do contrato Pydantic retornam 422; identificadores não encontrados retornam 404.
>
> Gere OITO casos de teste de integração, IT-R01 a IT-R08, complementares aos funcionais: título menor que 3, título maior que 120, enum prioridade inválido, atualização com status inválido sem alterar a tarefa, recursos inexistentes com 404, sugestão local com chave ausente, timeout externo simulado com fallback e resposta JSON externa inválida simulada com fallback.
>
> Cada teste deve conter setup isolado, requisição, payload, status e corpo esperados e comprovação do estado após a operação por uma nova requisição. Nos cenários externos, use monkeypatch para interceptar `urlopen`, chave fictícia e PROÍBA requisições reais à OpenAI. Não invente regras de negócio; resultados não executados devem ser marcados como *esperados*, não *aprovados*. Não duplique os oito casos funcionais.

## Refinamentos aplicados

1. Substituição de “simule erro na IA” pela injeção determinística de timeout e resposta JSON inválida em `urlopen`.
2. Inclusão de validação do estado pós-falha: a tarefa não é criada nos 422 e mantém os campos anteriores após PUT inválido.
3. Diferenciação entre HTTP 404 e 422 de acordo com o contrato existente.
4. Remoção de hipóteses de banco indisponível ou front-end sem suporte no código.

**Resultado:** casos IT-R01 a IT-R08 descritos em `../casos_teste_integracao.md` e automatizados em `../../../tests/test_integracao_unidade_iii.py`.
