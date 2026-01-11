# Agregar una Herramienta Personalizada (Llamada de Función)

En este capítulo, agregarás una **herramienta personalizada** a tu agente usando **llamadas de función**.


## ¿Por Qué Agregar una Herramienta Personalizada?

A veces, tu agente necesita hacer cosas más allá de solo hablar, como:

- Buscar datos de usuario
- Consultar un sistema de backend
- Ejecutar lógica específica del negocio

Las **llamadas de función** te permiten exponer código Python al agente, para que pueda llamar a tus funciones cuando sea necesario.


## Paso 1 - Actualizar Tus Importaciones

```python
import os
import json
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, FunctionTool, Tool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
```


## Paso 2 - Definir Tu Función

```python
## -- LLAMADA DE FUNCIÓN -- ##

# Implementación de la herramienta de consulta
def get_customer_by_phone(phone_number: str) -> str:
    customers = {
        "1234567890": {"name": "John Doe", "email": "john@example.com"},
        "0987654321": {"name": "Jane Doe", "email": "jane@example.com"},
    }
    customer = customers.get(phone_number, None)
    if customer:
        return json.dumps(customer)
    return json.dumps({"error": "Cliente no encontrado"})
```


## Paso 3 - Crear la Especificación de la Herramienta

```python
tools_spec = {
    "get_customer_by_phone": {
        "function": get_customer_by_phone,
        "spec": {
            "type": "function",
            "name": "get_customer_by_phone",
            "description": "Recupera información del cliente basado en su número de teléfono.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_number": {
                        "type": "string",
                        "description": "El número de teléfono del cliente"
                    }
                },
                "required": ["phone_number"],
                "additionalProperties": False,
            },
        },
    },
}
## -- LLAMADA DE FUNCIÓN -- ##
```


## Paso 4 - Agregar la Herramienta al Conjunto de Herramientas

```python
## Definir el conjunto de herramientas para el agente
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))
toolset.append(FunctionTool(functions=[tools_spec["get_customer_by_phone"]["spec"]]))
```


## Paso 5 - Manejar Llamadas de Función en el Bucle de Chat

El bucle de chat ahora necesita manejar llamadas de función:

```python
while True:
    user_input = input("Usuario: ")
    if user_input.lower() == "salir":
        break

    input_items: list[ResponseInputParam] = []
    input_items.append({"type": "message", "role": "user", "content": user_input})

    while True:
        response = openai_client.responses.create(
            input=input_items,
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            extra_body={
                "agent": {
                    "definition": agent.definition.model_dump(mode="json", exclude_none=True),
                }
            },
        )

        # Procesar la respuesta del agente y manejar llamadas de función
        if response.status == "incomplete" and response.incomplete_details.reason == "tool_calls":
            for output in response.output:
                input_items.append(output)
                if output.type == "function_call":
                    tool_result = tools_spec[output.name]["function"](**json.loads(output.arguments))
                    call_output: FunctionCallOutput = {
                        "type": "function_call_output",
                        "call_id": output.call_id,
                        "output": tool_result,
                    }
                    input_items.append(call_output)
        else:
            for output in response.output:
                if output.type == "message":
                    print("Agente:", output.content[0].text)
            break
```


## Paso 6 - Ejecutar el Agente

```bash
python agent.py
```


## Resumen

En este capítulo, tú:
- Creaste una **función Python personalizada**
- La expusiste como una **FunctionTool** para tu agente
- Manejaste **llamadas de función** en tu bucle de chat


## Muestra de código final

```python
<!--@include: ../codesamples/es/agent_5_tools.py-->
```

*Traducido usando GitHub Copilot.*
