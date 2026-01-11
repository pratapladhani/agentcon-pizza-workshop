# Agregar Instrucciones al Agente  

En el capítulo anterior, creaste tu primer agente básico e iniciaste una conversación con él.  
Ahora, daremos un paso más al aprender sobre **prompts del sistema** y por qué son esenciales para dar forma al comportamiento de tu agente.  


## ¿Qué es un Prompt del Sistema?  

Un prompt del sistema es un conjunto de **instrucciones** que proporcionas al modelo al crear un agente.  
Piensa en él como la **personalidad y el libro de reglas** para tu agente: define cómo debe responder el agente, qué tono debe usar y qué limitaciones debe seguir.  

Sin un prompt del sistema, tu agente puede responder de manera genérica. Al agregar instrucciones claras, puedes adaptarlo a tus necesidades.  

### Los prompts del sistema:  

- Aseguran que el agente se mantenga **consistente** a través de las conversaciones  
- Ayudan a guiar el **tono y rol** del agente  
- Reducen el riesgo de que el agente dé **respuestas irrelevantes o fuera de tema**  
- Te permiten **codificar reglas** que el agente debe seguir  


## Agregar Instrucciones a Tu Agente  

Al crear un agente, puedes pasar el parámetro `instructions` en el `PromptAgentDefinition`.  
Aquí hay un ejemplo:  

```python
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions="Eres un asistente de soporte útil para Microsoft Foundry. Siempre proporciona respuestas concisas, paso a paso.",
    ),
)
print(f"Agente creado (id: {agent.id}, nombre: {agent.name}, versión: {agent.version})")
```


## Usar un Archivo de Instrucciones Externo  

En lugar de codificar las instrucciones en tu script de Python, a menudo es mejor almacenarlas en un **archivo de texto separado**.  

Primero, crea un archivo llamado **`instrucciones.txt`** en la carpeta workshop con el contenido apropiado para tu PizzaBot.


## Modificar el Código del Agente  

Ahora, actualiza tu `agent.py` para cargar estas instrucciones:  

```python
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=open("instrucciones.txt").read(),
    ),
)
print(f"Agente creado (id: {agent.id}, nombre: {agent.name}, versión: {agent.version})")
```


## Ejecutar el Agente  

Prueba el Agente:  

```shell
python agent.py
```


## Resumen  

En este capítulo, has:  

- Aprendido qué es un **prompt del sistema**  
- Comprendido por qué agregar **instrucciones** es importante  
- Creado un agente con un **prompt del sistema personalizado**  
- Usado un **archivo de instrucciones externo**  


## Muestra de código final

```python 
<!--@include: ../codesamples/es/agent_3_instructions.py-->
```

*Traducido usando GitHub Copilot.*
