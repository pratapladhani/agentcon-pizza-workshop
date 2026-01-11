import json
import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, FunctionTool, Tool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam

load_dotenv()

vector_store_id = ""  # Defina o ID do seu vector store se já tiver um

## Configurar Cliente do Projeto
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()


## -- BUSCA DE ARQUIVOS -- ##

if vector_store_id:
    vector_store = openai_client.vector_stores.retrieve(vector_store_id)
    print(f"Usando vector store existente (id: {vector_store.id})")
else:
    # Criar vector store para busca de arquivos
    vector_store = openai_client.vector_stores.create(name="ContosoPizzaStores")
    print(f"Vector store criado (id: {vector_store.id})")

    # Fazer upload de arquivo para o vector store
    for file_path in glob.glob("documents/*.md"):
        file = openai_client.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id, file=open(file_path, "rb")
        )
        print(f"Arquivo enviado para o vector store (id: {file.id})")
## -- BUSCA DE ARQUIVOS -- ##


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


## Definir o toolset para o agente
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))
toolset.append(func_tool)


## Criar um Foundry Agent
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=open("instrucoes.txt").read(),
        tools=toolset,
    ),
)
print(f"Agente criado (id: {agent.id}, nome: {agent.name}, versão: {agent.version})")


## Criar uma conversa para a interação do agente
conversation = openai_client.conversations.create()
print(f"Conversa criada (id: {conversation.id})")

## Conversar com o agente

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
