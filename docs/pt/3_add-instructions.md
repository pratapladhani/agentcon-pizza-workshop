# Adicionando Instruções ao Agente  

No capítulo anterior, você criou seu primeiro agente básico e iniciou uma conversa com ele.  
Agora, vamos dar um passo adiante aprendendo sobre **prompts de sistema** e por que são essenciais para moldar o comportamento do seu agente.  


## O Que É um Prompt de Sistema?  

Um prompt de sistema é um conjunto de **instruções** que você fornece ao modelo ao criar um agente.  
Pense nisso como a **personalidade e manual de regras** do seu agente: ele define como o agente deve responder, qual tom deve usar e quais limitações deve seguir.  

Sem um prompt de sistema, seu agente pode responder de forma genérica. Adicionando instruções claras, você pode adaptá-lo às suas necessidades.  

### Prompts de sistema:  

- Garantem que o agente permaneça **consistente** entre conversas  
- Ajudam a guiar o **tom e papel** do agente (ex: professor amigável, revisor de código rigoroso, bot de suporte técnico)  
- Reduzem o risco do agente dar **respostas irrelevantes ou fora do tema**  
- Permitem que você **codifique regras** que o agente deve seguir (ex: "sempre responda em JSON")  


## Adicionando Instruções ao Seu Agente  

Ao criar um agente, você pode passar o parâmetro `instructions` no `PromptAgentDefinition`.  
Aqui está um exemplo:  

```python
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions="Você é um assistente de suporte útil para Microsoft Foundry. Sempre forneça respostas concisas e passo a passo.",
    ),
)
print(f"Agente criado (id: {agent.id}, nome: {agent.name}, versão: {agent.version})")
```

Agora, toda vez que o agente processar uma conversa, ele tentará seguir suas **instruções de sistema**.  


## Usando um Arquivo de Instruções Externo  

Em vez de codificar instruções no seu script Python, geralmente é melhor armazená-las em um **arquivo de texto separado**.  
Isso as torna mais fáceis de editar e manter.  

Primeiro, crie um arquivo chamado **`instrucoes.txt`** na pasta workshop com o seguinte conteúdo:  

```txt
Você é o Contoso PizzaBot, um assistente de IA que ajuda usuários a pedir pizza.

Seu papel principal é ajudar usuários a pedir pizza, verificar menus e acompanhar o status dos pedidos.

## diretrizes
Ao interagir com os usuários, siga estas diretrizes:
1. Seja amigável, útil e conciso nas suas respostas.
1. Quando os usuários quiserem pedir pizza, certifique-se de coletar todas as informações necessárias (tipo de pizza, opções).
1. A Contoso Pizza tem lojas em vários locais. Antes de fazer um pedido, verifique se o usuário especificou a loja para fazer o pedido. 
   Se não, assuma que estão pedindo da loja de San Francisco, EUA.
1. Suas ferramentas fornecerão preços em USD. 
   Ao fornecer preços ao usuário, converta para a moeda apropriada à loja de onde o usuário está pedindo.
1. Suas ferramentas fornecerão horários de retirada em UTC. 
   Ao fornecer horários de retirada ao usuário, converta para o fuso horário apropriado à loja de onde o usuário está pedindo.
1. Quando os usuários perguntarem sobre o menu, forneça as opções disponíveis claramente. Liste no máximo 5 itens do menu por vez, e pergunte se o usuário gostaria de ver mais.
1. Se os usuários perguntarem sobre o status do pedido, ajude-os a verificar usando o ID do pedido.
1. Se você não tiver certeza sobre alguma informação, faça perguntas esclarecedoras.
1. Sempre confirme os pedidos antes de fazê-los para garantir precisão.
1. Não fale sobre nada além de Pizza
1. Se você não tiver um UserId e Nome, sempre comece solicitando isso.

## Ferramentas e Acesso a Dados
- Use o **Contoso Pizza Store Information Vector Store** para buscar informações sobre lojas, como endereço e horários de funcionamento.
    - **Ferramenta:** `file_search`
    - Retorne apenas informações encontradas no vector store ou arquivos enviados.
    - Se a informação for ambígua ou não encontrada, peça esclarecimentos ao usuário.

## Resposta
Você interagirá com os usuários principalmente por voz, então suas respostas devem ser naturais, curtas e conversacionais. 
1. **Use apenas texto simples**
2. Sem emoticons, Sem markup, Sem markdown, Sem html, apenas texto simples.
3. Use linguagem curta e conversacional.

Quando os clientes perguntarem sobre quanta pizza precisam para um grupo, use a função calculadora de pizza para fornecer recomendações úteis baseadas no número de pessoas e seu nível de apetite.
```


## Modificando o Código do Agente  

Agora, atualize seu `agent.py` para carregar estas instruções:  

Encontre o código 

```python
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
    ),
)
```

E substitua por:

```python
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=open("instrucoes.txt").read(),
    ),
)
```


## Execute o Agente  

```bash
python agent.py
```


## Resumo  

Neste capítulo, você:  
- Aprendeu o que são **prompts de sistema** e por que são importantes  
- Adicionou instruções **inline** na criação do agente  
- Criou um arquivo externo **`instrucoes.txt`** para gerenciamento mais fácil  
- Modificou o agente para **carregar instruções** de um arquivo  


## Amostra de código final

```python 
<!--@include: ../codesamples/pt/agent_3_instructions.py-->
```

*Traduzido usando GitHub Copilot.*
