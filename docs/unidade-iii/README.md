# Atividade do Fórum: Unidade III — testes de integração com GenAI

Foram elaborados com ChatGPT dois tipos de prompts e uma matriz de 16 cenários com base no código real do **Mini-Projeto**, uma API FastAPI de tarefas.

## Conteúdo

- `prompts/01_fluxos_funcionais.md`: instrução e ajustes para oito casos de integração dos fluxos CRUD.
- `prompts/02_erros_resiliencia.md`: instrução e ajustes para oito casos negativos e de fallback.
- `casos_teste_integracao.md`: matriz de 16 casos com requisições, resultados esperados e verificações de estado.
- `../../tests/test_integracao_unidade_iii.py`: proposta de implementação automatizada que cobre os 16 IDs.
- `resposta_forum.md`: texto pronto para publicação após commit dos arquivos.

## Execução

Na raiz do projeto, com dependências do `requirements.txt` instaladas:

```powershell
python -m pytest tests/test_integracao_unidade_iii.py -v
```

**Rastreabilidade:** as especificações foram geradas e revisadas no ChatGPT. Nenhuma suíte pode ser declarada aprovada sem o resultado real de Pytest no checkout do repositório. Os scripts de automação são disponibilizados para execução, mas não substituem a comprovação por logs e commit publicado.

## Limites do cenário

A aplicação armazena tarefas em memória e não possui banco SQL, front-end ou autenticação. O PriorityAdvisor tem integração opcional com LLM; os testes não dependem de conta externa, porque simulam chamadas com monkeypatch.
