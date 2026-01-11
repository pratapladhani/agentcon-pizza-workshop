# Agregar un Servidor MCP  

En este capítulo final, agregarás un **servidor MCP (Model Context Protocol)** a tu agente.

MCP permite que tu agente se conecte a herramientas y servicios externos de forma estandarizada.


## ¿Por Qué Usar MCP?

- **Integración estandarizada** con herramientas externas
- **Extensibilidad** - conecta a cualquier servidor compatible con MCP
- **Separación de responsabilidades** - las herramientas viven fuera de tu código de agente


## Paso 1 - Actualizar Tus Importaciones

```python
import os
import json
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, FunctionTool, MCPTool, Tool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
```


## Paso 2 - Agregar la Herramienta MCP

```python
## Definir el conjunto de herramientas para el agente
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))
toolset.append(FunctionTool(functions=[tools_spec["get_customer_by_phone"]["spec"]]))
toolset.append(MCPTool(server_label="pizza-mcp", server_url=os.environ["MCP_SERVER_URL"], require_approval="never"))
```


## Paso 3 - Actualizar Tu Archivo .env

Agrega la URL del servidor MCP a tu archivo `.env`:

```
MCP_SERVER_URL=https://tu-servidor-mcp.example.com/sse
```


## Paso 4 - Ejecutar el Agente

```bash
python agent.py
```


## Resumen

En este capítulo, tú:
- Aprendiste sobre **MCP (Model Context Protocol)**
- Agregaste una **MCPTool** a tu conjunto de herramientas
- Conectaste tu agente a un **servidor MCP externo**


## Muestra de código final

```python
<!--@include: ../codesamples/es/agent_6_mcp.py-->
```

*Traducido usando GitHub Copilot.*
