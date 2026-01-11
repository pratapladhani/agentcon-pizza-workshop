import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, Tool

load_dotenv()

vector_store_id = ""  # Establece el ID de tu vector store si ya tienes uno

## Configurar el Cliente del Proyecto
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()


## -- BÚSQUEDA DE ARCHIVOS -- ##

if vector_store_id:
    vector_store = openai_client.vector_stores.retrieve(vector_store_id)
    print(f"Usando vector store existente (id: {vector_store.id})")
else:
    # Crear vector store para búsqueda de archivos
    vector_store = openai_client.vector_stores.create(name="ContosoPizzaStores")
    print(f"Vector store creado (id: {vector_store.id})")

    # Subir archivos al vector store
    for file_path in glob.glob("documentos/*.md"):
        file = openai_client.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id, file=open(file_path, "rb")
        )
        print(f"Archivo subido al vector store (id: {file.id})")
## -- BÚSQUEDA DE ARCHIVOS -- ##


## Definir el conjunto de herramientas para el agente
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))


## Crear un Agente Foundry
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=open("instrucciones.txt").read(),
        tools=toolset,
    ),
)
print(f"Agente creado (id: {agent.id}, nombre: {agent.name}, versión: {agent.version})")


## Crear una conversación para la interacción con el agente
conversation = openai_client.conversations.create()
print(f"Conversación creada (id: {conversation.id})")

## Chatear con el agente

while True:
    # Obtener la entrada del usuario
    user_input = input("Tú: ")

    if user_input.lower() in ["salir", "terminar"]:
        print("Saliendo del chat.")
        break

    # Obtener la respuesta del agente
    response = openai_client.responses.create(
        conversation=conversation.id,
        input=user_input,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    # Imprimir la respuesta del agente
    print(f"Asistente: {response.output_text}")
