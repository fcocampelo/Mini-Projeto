# Escopo do MVP

## Objetivo

Construir uma micro-API para gestao de tarefas de uma equipe interna, permitindo registrar, consultar, atualizar e acompanhar tarefas de forma simples. O MVP deve priorizar uma base tecnica clara, endpoints essenciais e estrutura preparada para evoluir com priorizacao assistida por IA.

## Requisitos Funcionais

### RF01 - Criar tarefa

A API deve permitir o cadastro de uma nova tarefa com, no minimo:

- Titulo
- Descricao
- Status
- Prioridade
- Data de criacao

### RF02 - Listar tarefas

A API deve permitir listar tarefas cadastradas.

A listagem deve retornar os principais dados da tarefa, incluindo:

- Identificador
- Titulo
- Status
- Prioridade
- Data de criacao

### RF03 - Consultar tarefa por ID

A API deve permitir consultar os detalhes de uma tarefa especifica a partir de seu identificador.

### RF04 - Atualizar tarefa

A API deve permitir atualizar dados de uma tarefa existente, incluindo:

- Titulo
- Descricao
- Status
- Prioridade

### RF05 - Remover tarefa

A API deve permitir remover uma tarefa existente a partir de seu identificador.

### RF06 - Controlar status da tarefa

A API deve permitir classificar uma tarefa por status.

Status minimos previstos:

- Pendente
- Em andamento
- Concluida
- Cancelada

### RF07 - Definir prioridade da tarefa

A API deve permitir definir prioridade manual para uma tarefa.

Prioridades minimas previstas:

- Baixa
- Media
- Alta
- Critica

### RF08 - Verificar saude da API

A API deve disponibilizar um endpoint de health check para validar se o servico esta ativo.

Endpoint previsto:

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

### RF09 - Preparar priorizacao assistida por IA

A API deve ser estruturada para permitir, em release futura, a sugestao automatica de prioridade com base em criterios como:

- Prazo
- Impacto
- Esforco
- Dependencias
- Contexto informado na descricao da tarefa

## Requisitos Nao Funcionais

### RNF01 - Linguagem e framework

A API deve ser desenvolvida em Python com FastAPI.

### RNF02 - Contratos tipados

Os modelos de entrada e saida devem utilizar tipagem explicita e validacao de dados.

### RNF03 - Documentacao automatica

A API deve expor documentacao interativa via OpenAPI/Swagger.

Endpoint padrao esperado:

```http
GET /docs
```

### RNF04 - Execucao local simples

O projeto deve permitir execucao local com ambiente virtual Python e instalacao de dependencias via `requirements.txt`.

### RNF05 - Organizacao do projeto

O codigo deve seguir uma estrutura simples e evolutiva, separando responsabilidades conforme o crescimento do MVP.

Estrutura inicial prevista:

```text
app/
└── main.py
```

### RNF06 - Versionamento

O projeto deve ser versionado com Git e seguir mensagens de commit no padrao Conventional Commits.

### RNF07 - Configuracoes locais

Arquivos de ambiente virtual, caches, variaveis locais e configuracoes de editor nao devem ser versionados.

### RNF08 - Observabilidade minima

A API deve possuir endpoint de health check para uso em validacao local, automacao e deploy futuro.

### RNF09 - Compatibilidade

O projeto deve ser compativel com Python 3.14.

### RNF10 - Seguranca basica

Informacoes sensiveis, como chaves de API, tokens e credenciais, nao devem ser armazenadas no repositorio.

## Fora de Escopo

Os itens abaixo nao fazem parte do MVP inicial:

- Interface web ou mobile
- Autenticacao de usuarios
- Controle de permissoes por perfil
- Integracao real com servicos de IA
- Persistencia em banco de dados externo
- Historico detalhado de alteracoes
- Notificacoes por e-mail, Slack ou outros canais
- Upload de arquivos anexos as tarefas
- Metricas avancadas de produtividade
- Deploy em ambiente de producao
- Pipeline de CI/CD
- Multi-tenant ou suporte a multiplas organizacoes
- Integracao com ferramentas externas de gestao de projetos
