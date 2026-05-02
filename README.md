# Mini-Projeto

MVP de uma micro-API para gestao de tarefas com priorizacao assistida por IA.

## Objetivo

Este projeto tem como objetivo fornecer uma API simples para cadastro, consulta, atualizacao e priorizacao de tarefas. A proposta do MVP e validar um fluxo basico de gestao de tarefas, com suporte futuro de IA para sugerir prioridade com base em criterios como prazo, impacto, esforco e contexto da tarefa.

## Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- Ambiente virtual com `venv`
- Git para versionamento

## Funcionalidades previstas no MVP

- Criar tarefas
- Listar tarefas
- Consultar tarefa por ID
- Atualizar tarefa
- Remover tarefa
- Definir prioridade manualmente
- Preparar estrutura para priorizacao assistida por IA

## Como rodar localmente

### 1. Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd Mini-Projeto
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install fastapi uvicorn
```

### 5. Rodar a API

```bash
uvicorn main:app --reload
```

A API ficara disponivel em:

```text
http://127.0.0.1:8000
```

A documentacao interativa ficara disponivel em:

```text
http://127.0.0.1:8000/docs
```

## Estrutura inicial sugerida

```text
Mini-Projeto/
├── main.py
├── README.md
├── .gitignore
└── .venv/
```

## Roadmap de releases

### Release 0.1.0 - Estrutura inicial

- Configuracao inicial do projeto
- Criacao do repositorio Git
- Configuracao do `.gitignore`
- Criacao do README
- Setup basico com FastAPI

### Release 0.2.0 - CRUD de tarefas

- Criar endpoint para cadastro de tarefas
- Criar endpoint para listagem de tarefas
- Criar endpoint para consulta por ID
- Criar endpoint para atualizacao de tarefas
- Criar endpoint para remocao de tarefas

### Release 0.3.0 - Priorizacao manual

- Adicionar campo de prioridade
- Permitir classificacao por prioridade
- Permitir filtro por status
- Melhorar validacoes com Pydantic

### Release 0.4.0 - Priorizacao assistida por IA

- Criar endpoint para sugestao de prioridade
- Definir criterios de priorizacao
- Integrar servico de IA
- Registrar justificativa da prioridade sugerida

### Release 0.5.0 - Persistencia

- Adicionar banco de dados
- Criar camada de repositorio
- Implementar migracoes
- Persistir tarefas e historico de alteracoes

### Release 1.0.0 - MVP estavel

- Consolidar endpoints principais
- Adicionar testes automatizados
- Revisar documentacao
- Preparar ambiente para deploy
