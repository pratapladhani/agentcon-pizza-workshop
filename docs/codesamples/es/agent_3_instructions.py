import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

## Configurar el Cliente del Proyecto
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()


## Crear un Agente Foundry
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=open("instrucciones.txt").read(),
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
