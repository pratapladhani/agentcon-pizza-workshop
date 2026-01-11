# Tool Calling – Making Your Agent Act

In the previous chapters you gave your agent instructions and grounded it in your own data with File Search (RAG).  

Now, let's enable your agent to **take actions** by calling **tools** — small, well-defined functions your agent can invoke to perform tasks (e.g., calculations, lookups, API calls).

## What Are Tools (Function Calling)?

**Tools** let your agent call *your code* with structured inputs.  
When a user asks for something that matches a tool's purpose, the agent will select that tool, pass validated arguments, and use the tool's result to craft a final answer.

### Why this matters
- **Deterministic actions:** offload precise work (math, lookup, API calls) to your code.  
- **Safety & control:** you define what the agent is allowed to do.  
- **Better UX:** the agent can provide concrete, actionable answers.



## Adding the Pizza Size Calculator Tool

We'll add a tool that, given a **number of people**, recommends how many pizzas to order.

### 1) Update Your Imports

Update your imports to include `FunctionTool` and the OpenAI types for function calling:

```python
import json
import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, FunctionTool, Tool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
```


### 2) Define the Function Tool

Add this after your File Search code and before creating the toolset:

```python
## -- Function Calling Tool -- ##
func_tool = FunctionTool(
    name="get_pizza_quantity",
    parameters={
        "type": "object",
        "properties": {
            "people": {
                "type": "integer",
                "description": "The number of people to order pizza for",
            },
        },
        "required": ["people"],
        "additionalProperties": False,
    },
    description="Get the quantity of pizza to order based on the number of people.",
    strict=True,
)

def get_pizza_quantity(people: int) -> str:
    """Calculate the number of pizzas to order based on the number of people.
        Assumes each pizza can feed 2 people.
    Args:
        people (int): The number of people to order pizza for.
    Returns:
        str: A message indicating the number of pizzas to order.
    """
    print(f"[FUNCTION CALL:get_pizza_quantity] Calculating pizza quantity for {people} people.")
    return f"For {people} you need to order {people // 2 + people % 2} pizzas."
## -- Function Calling Tool -- ##
```

::: info
This function uses a simple calculation: 1 pizza per 2 people, rounded up.
:::


### 3) Add the Function Tool to the Toolset

Update your toolset to include the function tool:

```python
## Define the toolset for the agent
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))
toolset.append(func_tool)
```


### 4) Handle Function Calls in the Chat Loop

Update your chat loop to handle function calls. Replace your existing chat loop with:

```python
while True:
    # Get the user input
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat.")
        break

    # Get the agent response
    response = openai_client.responses.create(
        conversation=conversation.id,
        input=user_input,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    # Handle function calls in the response
    input_list: ResponseInputParam = []
    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_pizza_quantity":
                # Execute the function logic for get_pizza_quantity
                pizza_quantity = get_pizza_quantity(**json.loads(item.arguments))
                # Provide function call results to the model
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

    # Print the agent response
    print(f"Assistant: {response.output_text}")
```


## Trying It Out

Run your agent and ask a question that should trigger the tool:

```
We are 7 people. How many pizzas should we order?
```

The agent should call `get_pizza_quantity` and reply with the recommendation it returns.



## Tips & Best Practices

- **Schema first:** define clear types, required fields, and descriptions.  
- **Validate inputs:** the tool should handle bad or missing data gracefully.  
- **Single-purpose tools:** small, focused tools are easier for the agent to choose and combine.  
- **Explainability:** name and describe tools so the agent knows when to use them.



## Recap

In this chapter you:
- Created a **pizza calculator function** directly in your script.  
- Exposed it as a **FunctionTool** the agent can call.  
- Added it to your existing toolset (alongside File Search).  
- Implemented **function call handling** in the chat loop.  
- Verified tool calling by prompting your agent.



## Final code sample

```python 
<!--@include: ./codesamples/agent_5_tools.py-->
```
