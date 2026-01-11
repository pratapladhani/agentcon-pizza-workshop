# Chamada de Ferramentas – Fazendo Seu Agente Agir

Nos capítulos anteriores, você deu instruções ao seu agente e o fundamentou em seus próprios dados com File Search (RAG).  

Agora, vamos habilitar seu agente a **executar ações** chamando **ferramentas** — funções pequenas e bem definidas que seu agente pode invocar para realizar tarefas (ex: cálculos, buscas, chamadas de API).

## O Que São Ferramentas (Chamada de Função)?

**Ferramentas** permitem que seu agente chame *seu código* com inputs estruturados.  
Quando um usuário pede algo que corresponde ao propósito de uma ferramenta, o agente selecionará essa ferramenta, passará argumentos validados e usará o resultado da ferramenta para criar uma resposta final.

### Por que isso importa
- **Ações determinísticas:** delegue trabalho preciso (matemática, busca, chamadas de API) ao seu código.  
- **Segurança e controle:** você define o que o agente pode fazer.  
- **Melhor UX:** o agente pode fornecer respostas concretas e acionáveis.



## Adicionando a Ferramenta Calculadora de Tamanho de Pizza

Vamos adicionar uma ferramenta que, dado um **número de pessoas**, recomenda quantas pizzas pedir.

### 1) Atualizar Seus Imports

Atualize seus imports para incluir `FunctionTool` e os tipos OpenAI para chamada de função:

```python
import json
import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, FunctionTool, Tool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
```


### 2) Definir a Ferramenta de Função

Adicione isso após seu código de File Search e antes de criar o toolset:

```python
## -- Ferramenta de Chamada de Função -- ##
func_tool = FunctionTool(
    name="get_pizza_quantity",
    parameters={
        "type": "object",
        "properties": {
            "people": {
                "type": "integer",
                "description": "O número de pessoas para pedir pizza",
            },
        },
        "required": ["people"],
        "additionalProperties": False,
    },
    description="Obtém a quantidade de pizza a pedir baseado no número de pessoas.",
    strict=True,
)

def get_pizza_quantity(people: int) -> str:
    """Calcula o número de pizzas a pedir baseado no número de pessoas.
        Assume que cada pizza alimenta 2 pessoas.
    Args:
        people (int): O número de pessoas para pedir pizza.
    Returns:
        str: Uma mensagem indicando o número de pizzas a pedir.
    """
    print(f"[CHAMADA DE FUNÇÃO:get_pizza_quantity] Calculando quantidade de pizza para {people} pessoas.")
    return f"Para {people} você precisa pedir {people // 2 + people % 2} pizzas."
## -- Ferramenta de Chamada de Função -- ##
```

::: info
Esta função usa um cálculo simples: 1 pizza por 2 pessoas, arredondando para cima.
:::


### 3) Adicionar a Ferramenta de Função ao Toolset

Atualize seu toolset para incluir a ferramenta de função:

```python
## Definir o toolset para o agente
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))
toolset.append(func_tool)
```


### 4) Tratar Chamadas de Função no Loop de Chat

Atualize seu loop de chat para tratar chamadas de função. Substitua seu loop de chat existente por:

```python
while True:
    # Obter a entrada do usuário
    user_input = input("Você: ")

    if user_input.lower() in ["exit", "quit", "sair"]:
        print("Saindo do chat.")
        break

    # Obter a resposta do agente
    response = openai_client.responses.create(
        conversation=conversation.id,
        input=user_input,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    # Tratar chamadas de função na resposta
    input_list: ResponseInputParam = []
    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_pizza_quantity":
                # Executar a lógica da função para get_pizza_quantity
                pizza_quantity = get_pizza_quantity(**json.loads(item.arguments))
                # Fornecer resultados da chamada de função ao modelo
                input_list.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=item.call_id,
                        output=json.dumps({"pizza_quantity": pizza_quantity}),
                    )
                )

    if input_list:
        response = openai_client.responses.create(
            previous_response_id=response.id,
            input=input_list,
            extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
        )    

    # Imprimir a resposta do agente
    print(f"Assistente: {response.output_text}")
```


## Experimentando

Execute seu agente e faça uma pergunta que deve acionar a ferramenta:

```
Somos 7 pessoas. Quantas pizzas devemos pedir?
```

O agente deve chamar `get_pizza_quantity` e responder com a recomendação que ela retorna.



## Dicas e Melhores Práticas

- **Esquema primeiro:** defina tipos claros, campos obrigatórios e descrições.  
- **Valide inputs:** a ferramenta deve tratar dados ruins ou ausentes graciosamente.  
- **Ferramentas de propósito único:** ferramentas pequenas e focadas são mais fáceis para o agente escolher e combinar.  
- **Explicabilidade:** nomeie e descreva ferramentas para que o agente saiba quando usá-las.



## Resumo

Neste capítulo você:
- Criou uma **função calculadora de pizza** diretamente no seu script.  
- A expôs como uma **FunctionTool** que o agente pode chamar.  
- Adicionou ao seu toolset existente (junto com File Search).  
- Implementou **tratamento de chamada de função** no loop de chat.  
- Verificou a chamada de ferramenta testando seu agente.



## Amostra de código final

```python 
<!--@include: ../codesamples/pt/agent_5_tools.py-->
```

*Traduzido usando GitHub Copilot.*
