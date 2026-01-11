import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, Tool

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


## Definir o toolset para o agente
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))


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

    # Imprimir a resposta do agente
    print(f"Assistente: {response.output_text}")
