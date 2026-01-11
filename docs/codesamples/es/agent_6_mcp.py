import json
import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, FunctionTool, MCPTool, Tool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam

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


## -- Herramienta de Llamada a Función -- ##
func_tool = FunctionTool(
    name="get_pizza_quantity",
    parameters={
        "type": "object",
        "properties": {
            "people": {
                "type": "integer",
                "description": "El número de personas para las que pedir pizza",
            },
        },
        "required": ["people"],
        "additionalProperties": False,
    },
    description="Obtener la cantidad de pizza a pedir basado en el número de personas.",
    strict=True,
)

def get_pizza_quantity(people: int) -> str:
    """Calcular el número de pizzas a pedir basado en el número de personas.
        Asume que cada pizza puede alimentar a 2 personas.
    Args:
        people (int): El número de personas para las que pedir pizza.
    Returns:
        str: Un mensaje indicando el número de pizzas a pedir.
    """
    print(f"[LLAMADA A FUNCIÓN:get_pizza_quantity] Calculando cantidad de pizza para {people} personas.")
    return f"Para {people} personas necesitas pedir {people // 2 + people % 2} pizzas."
## -- Herramienta de Llamada a Función -- ##


## -- MCP -- ##
mcpTool = MCPTool(
    server_label="contoso-pizza-mcp",
    server_url="https://pizza-mcp-server.prouddune-f79ccb2b.westeurope.azurecontainerapps.io/mcp",
    require_approval="never"
)
## -- MCP -- ##


## Definir el conjunto de herramientas para el agente
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))
toolset.append(func_tool)
toolset.append(mcpTool)


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

    # Manejar las llamadas a funciones en la respuesta
    input_list: ResponseInputParam = []
    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_pizza_quantity":
                # Ejecutar la lógica de la función para get_pizza_quantity
                pizza_quantity = get_pizza_quantity(**json.loads(item.arguments))
                # Proporcionar los resultados de la llamada a función al modelo
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

    # Imprimir la respuesta del agente
    print(f"Asistente: {response.output_text}")
