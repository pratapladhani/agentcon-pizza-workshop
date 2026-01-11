# Agregar Conocimiento con Búsqueda de Archivos  

En los capítulos anteriores, creaste un agente básico y le diste instrucciones a través de un prompt del sistema.  
Ahora es el momento de **hacer que tu agente sea más inteligente** al fundamentarlo en **tus propios datos**.  


## ¿Por Qué Agregar Conocimiento?  

Por defecto, el modelo solo sabe lo que fue entrenado para saber. Usaremos **Generación Aumentada por Recuperación (RAG)**.  

- **RAG** permite al agente obtener información relevante de tus propios datos antes de generar una respuesta.  
- Esto asegura que las respuestas de tu agente sean **precisas, actualizadas y fundamentadas** en información real.  

En este capítulo, usarás una carpeta llamada **`./documentos`** que contiene información sobre **tiendas de Contoso Pizza**.


## Paso 1 - Actualizar Tus Importaciones  

```python
import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, Tool
```


## Paso 2 - Crear el Vector Store  

Agrega este código después de crear tu `openai_client`:

```python
vector_store_id = ""  # Establece el ID de tu vector store si ya tienes uno

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
```


## Paso 3 - Agregar la Herramienta de Búsqueda de Archivos  

```python
## Definir el conjunto de herramientas para el agente
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))
```


## Paso 4 - Actualizar la Creación del Agente  

```python
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=open("instrucciones.txt").read(),
        tools=toolset,
    ),
)
```


## Paso 5 - Ejecutar el Agente  

```bash
python agent.py
```


## Resumen  

En este capítulo, tú:  
- Aprendiste cómo **RAG** fundamenta tu agente con tus propios datos  
- Creaste y poblaste un **vector store** directamente en tu script  
- Agregaste una **herramienta de Búsqueda de Archivos** a tu agente  


## Muestra de código final

```python 
<!--@include: ../codesamples/es/agent_4_rag.py-->
```

*Traducido usando GitHub Copilot.*
