import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

## Configurar Cliente do Projeto
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()


## Criar um Foundry Agent
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
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
