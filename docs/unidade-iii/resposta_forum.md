## Testes de integração com GenAI — Mini-Projeto

Para a atividade, utilizei meu Mini-Projeto, uma API de tarefas desenvolvida com Python e FastAPI: https://github.com/fcocampelo/Mini-Projeto.

Escolhi como cenário a integração entre a API REST, o serviço responsável pelas regras das tarefas, o repositório em memória e o componente que sugere prioridades com apoio de IA.

**1. Prompt de cenários funcionais:** pedi ao ChatGPT que analisasse o fluxo de criação, consulta, listagem, atualização e exclusão de tarefas. O prompt também abordou dados de entrada, valores-limite e verificação do estado da tarefa após as operações. Dessa abordagem surgiram oito casos de teste (IT-F01 a IT-F08).

**2. Prompt de casos de erro e resiliência:** pedi cenários com títulos inválidos, prioridades e status fora do contrato, tarefas inexistentes e falhas simuladas de comunicação com a IA. Essa abordagem gerou mais oito casos (IT-R01 a IT-R08), incluindo a utilização do mecanismo local de sugestão de prioridade quando a integração externa falha.

O primeiro prompt ajudou a organizar os fluxos principais, enquanto o segundo ampliou a diversidade dos testes com situações que nem sempre aparecem no uso normal da aplicação. Percebi que instruções muito genéricas não deixam claro o que deve ser verificado. Por isso, refinei os prompts, informando endpoints, respostas HTTP esperadas, componentes existentes e a necessidade de consultar o estado da tarefa após cada operação.

Outro cuidado foi pedir que a LLM não inventasse funcionalidades que não existem, como banco de dados ou front-end, e que as falhas externas fossem simuladas sem depender de uma chamada real. Os prompts e os 16 casos foram documentados na pasta `docs/unidade-iii/`, junto com uma proposta de testes automatizados com Pytest.

Concluí que a GenAI ajuda bastante a explorar casos de integração e encontrar cenários que eu poderia deixar passar. Porém, a revisão do código e a execução dos testes continuam sendo necessárias para confirmar se o comportamento esperado realmente acontece.
