# Crea Tu Primer Agente  

En este capítulo, recorreremos el proceso de crear tu primer agente de IA utilizando el **Foundry Agent Service**.  
Al final, tendrás un agente simple ejecutándose localmente con el que podrás interactuar en tiempo real.  

Primero vuelve al entorno de Github codespace que creaste anteriormente. Asegúrate de que el panel de terminal todavía esté abierto en la carpeta **workshop**.


## Iniciar Sesión en Azure  

Antes de poder usar el Foundry Agent Service, necesitas iniciar sesión en tu suscripción de Azure.  

Ejecuta el siguiente comando y sigue las instrucciones en pantalla. Usa credenciales que tengan acceso a tu recurso de Microsoft Foundry:  

```shell
az login --use-device-code
```



## Instalar los Paquetes Requeridos  

A continuación, instala los paquetes de Python necesarios para trabajar con Microsoft Foundry y gestionar variables de entorno:  

```shell
pip install openai azure-identity azure-ai-projects==2.0.0b1 jsonref python-dotenv
```


### Crear un Archivo `.env`  

Almacenaremos secretos (como el endpoint de tu proyecto) en un archivo de entorno por seguridad y flexibilidad.  

1. **Crea un archivo llamado `.env` en la raíz del directorio de tu proyecto.**

2. **Agrega las siguientes líneas al archivo:**

    ```env
    PROJECT_ENDPOINT="https://<tu-recurso-foundry>.services.ai.azure.com/api/projects/<nombre-tu-proyecto>"
    MODEL_DEPLOYMENT_NAME="gpt-4o"
    ```

Reemplaza `https://<tu-recurso-foundry>.services.ai.azure.com/api/projects/<nombre-tu-proyecto>` con los valores reales de tu proyecto de Microsoft Foundry. 

![](/public/foundry/foundry-project-string.png)  


3. **Dónde encontrar tu endpoint:**

   - Ve al **portal de Microsoft Foundry**
   - Navega a tu proyecto
   - Haz clic en **Descripción general**
   - El endpoint se mostrará en la página de inicio de tu proyecto



### 📝 Notas

- Asegúrate de que **no haya espacios** alrededor del signo `=` en el archivo `.env`.



## Crear un Agente Básico  

Ahora crearemos un script básico de Python que define y ejecuta un agente.  

- Comienza creando un nuevo archivo llamado: **`agent.py`** en la carpeta **workshop**



### Agregar Importaciones a `agent.py`  

Estas importaciones traen el SDK de Azure, manejo de entorno y clases auxiliares:  

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
```

### Cargar el Archivo `.env`  

Carga las variables de entorno en tu script agregando esta línea a `agent.py`:  

```python
load_dotenv()
```



### Crear el Cliente del Proyecto  

Este cliente conecta tu script al servicio de Microsoft Foundry usando el endpoint y tus credenciales de Azure.  

```python
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()
```



### Crear el Agente  

Ahora, creemos el agente en sí. Usaremos `create_version` para crear un Agente Foundry con un `PromptAgentDefinition`.  

```python
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
    ),
)
print(f"Agente creado (id: {agent.id}, nombre: {agent.name}, versión: {agent.version})")
```



### Crear una Conversación  

Los agentes interactúan dentro de conversaciones. Una conversación es como un contenedor que almacena todos los mensajes intercambiados entre el usuario y el agente.  

```python
conversation = openai_client.conversations.create()
print(f"Conversación creada (id: {conversation.id})")
```



### Chatear con el Agente  

Este bucle te permite enviar mensajes al agente. Escribe en el terminal y el mensaje se enviará al agente.  

```python
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
```



## Ejecutar el Agente  

Finalmente, ejecuta el script de Python:  

```shell
python agent.py
```

Ahora puedes chatear con tu agente directamente en el terminal. Escribe `salir` o `terminar` para detener la conversación.  

## Depuración 

Si obtienes un error (el principal `*****-****-***-****-*****`) **no tiene permiso** para crear asistentes en tu proyecto de Microsoft Foundry. Específicamente, le falta la acción de datos **`Microsoft.CognitiveServices/accounts/AIServices/agents/write`**.

Aquí está cómo solucionarlo:

1. **Ve al Portal de Azure**: [https://portal.azure.com](https://portal.azure.com)

2. **Navega a tu recurso de Microsoft Foundry**:
   - Puedes encontrarlo buscando el nombre de tu recurso de Foundry (por ejemplo, `mi-nombre-foundry`).

3. **Abre el panel "Control de acceso (IAM)"**:
   - En el menú de la izquierda del recurso, haz clic en **Control de acceso (IAM)**.

4. **Haz clic en "Agregar asignación de rol"**:
   - Elige **Agregar → Agregar asignación de rol**
   - Selecciona un rol que incluya la acción de datos requerida:
     - Recomendado: **Colaborador de Cognitive Services** o un **rol personalizado** que incluya `Microsoft.CognitiveServices/accounts/AIServices/agents/write`

5. **Asigna el rol a tu principal**:
   - Usa el ID de objeto o nombre del principal: `******-****-***-********`
   - Esto podría ser un principal de servicio, usuario o identidad administrada dependiendo de tu configuración.

6. **Guarda y confirma**:
   - Una vez asignado, espera unos minutos para que el permiso se propague.
   - Vuelve a intentar la operación para crear el asistente.



## Resumen  

En este capítulo, has:  

- Iniciado sesión en Azure  
- Recuperado un endpoint del proyecto  
- Separado secretos del código usando `.env`  
- Creado un agente básico con el Foundry Agent Service  
- Iniciado una conversación con el agente  


## Muestra de código final

```python 
<!--@include: ../codesamples/es/agent_2.py-->
```

*Traducido usando GitHub Copilot.*
