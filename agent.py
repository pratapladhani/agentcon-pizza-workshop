import json
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import (
    PromptAgentDefinition, FileSearchTool, FunctionTool, MCPTool, Tool
)
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
from dotenv import load_dotenv
from tools import calculate_pizza_for_people

load_dotenv(override=True)

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)
openai_client = project_client.get_openai_client()

# Create the File Search tool
vector_store_id = "vs_hCdBuIqvgB1vWT9ineq6Uqk2"
file_search = FileSearchTool(vector_store_ids=[vector_store_id])

# Create the Function tool
func_tool = FunctionTool(
    name="calculate_pizza_for_people",
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
    description="Calculate the number of pizzas to order based on the number of people.",
    strict=True,
)

# Add MCP tool so the agent can call Contoso Pizza microservices
mcp_tool = MCPTool(
    server_label="contoso_pizza",
    server_url="https://ca-pizza-mcp-sc6u2typoxngc.graypond-9d6dd29c.eastus2.azurecontainerapps.io/sse",
    require_approval="never"
)

# Define the toolset for the agent
toolset: list[Tool] = []
toolset.append(file_search)
toolset.append(func_tool)
toolset.append(mcp_tool)

# Create a Foundry Agent
agent = project_client.agents.create_version(
    agent_name="contoso-pizza-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=open("instructions.txt").read(),
        tools=toolset,
    ),
)
print(
    f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# Create a conversation for the agent interaction
conversation = openai_client.conversations.create()
print(f"Created conversation (id: {conversation.id})")

try:
    while True:
        # Get the user input
        user_input = input("You: ")

        # Break out of the loop
        if user_input.lower() in ["exit", "quit"]:
            break

        # Get the agent response
        response = openai_client.responses.create(
            conversation=conversation.id,
            input=user_input,
            extra_body={"agent": {"name": agent.name,
                                  "type": "agent_reference"}},
        )

        # Handle function calls in the response
        input_list: ResponseInputParam = []
        for item in response.output:
            if item.type == "function_call":
                if item.name == "calculate_pizza_for_people":
                    # Execute the function logic
                    result = calculate_pizza_for_people(
                        **json.loads(item.arguments))
                    # Provide function call results to the model
                    input_list.append(
                        FunctionCallOutput(
                            type="function_call_output",
                            call_id=item.call_id,
                            output=json.dumps({"result": result}),
                        )
                    )

        if input_list:
            response = openai_client.responses.create(
                previous_response_id=response.id,
                input=input_list,
                extra_body={"agent": {"name": agent.name,
                                      "type": "agent_reference"}},
            )

        # Print the agent response
        print(f"Assistant: {response.output_text}")
finally:
    print("\nExiting...")
