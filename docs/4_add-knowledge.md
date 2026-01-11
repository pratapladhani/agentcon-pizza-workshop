# Adding Knowledge with File Search  

In the previous chapters, you created a basic agent and gave it instructions through a system prompt.  
Now it's time to **make your agent smarter** by grounding it in **your own data**.  



## Why Add Knowledge?  

By default, the model only knows what it was trained on - it doesn't have access to your organization's private or domain-specific information.  
To bridge this gap, we'll use **Retrieval-Augmented Generation (RAG)**.  

- **RAG** lets the agent fetch relevant information from your own data before generating a response.  
- This ensures your agent's answers are **accurate, up-to-date, and grounded** in real information.  
- In Microsoft Foundry, we'll use the **File Search** feature to implement this.  

In this chapter, you'll use a folder called **`./documents`** that contains information about **Contoso Pizza stores** - such as locations, opening hours, and menus.  

We'll upload these files to a **vector store** and connect that store to the agent using a **File Search tool**.  


## Step 1 - Update Your Imports  

First, update your imports at the top of `agent.py` to include the necessary classes:  

```python
import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, Tool
```

## Step 2 - Create the Vector Store  

Add this code after creating your `openai_client` to create a vector store and upload documents:  

```python
vector_store_id = ""  # Set to your vector store ID if you already have one

## -- FILE SEARCH -- ##

if vector_store_id:
    vector_store = openai_client.vector_stores.retrieve(vector_store_id)
    print(f"Using existing vector store (id: {vector_store.id})")
else:
    # Create vector store for file search
    vector_store = openai_client.vector_stores.create(name="ContosoPizzaStores")
    print(f"Vector store created (id: {vector_store.id})")

    # Upload file to vector store
    for file_path in glob.glob("documents/*.md"):
        file = openai_client.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id, file=open(file_path, "rb")
        )
        print(f"File uploaded to vector store (id: {file.id})")
## -- FILE SEARCH -- ##
```

**Why:**  
- A vector store stores and indexes document embeddings for semantic search.
- The first time you run the script, it creates a new vector store and uploads all documents.
- On subsequent runs, you can set `vector_store_id` to reuse the existing store.

**Tip:** After the first run, copy the vector store ID from the output and set it in the `vector_store_id` variable to avoid recreating it each time.


## Step 3 - Add the File Search Tool  

Now add the File Search tool to your agent's toolset. Add this before creating the agent:  

```python
## Define the toolset for the agent
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))
```


## Step 4 - Update the Agent Creation  

Modify your agent creation to include the toolset:  

```python
## Create a Foundry Agent
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=open("instructions.txt").read(),
        tools=toolset,
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```



## Step 5 - Run the Agent  

Try it out:  

```bash
python agent.py
```

Ask questions like:  
> "Which Contoso Pizza stores are open after 8pm?"  
> "Where is the nearest Contoso Pizza store?"  

Type `exit` or `quit` to stop the conversation.  



## Recap  

In this chapter, you:  
- Learned how **RAG** grounds your agent with your own data  
- Created and populated a **vector store** directly in your script  
- Added a **File Search tool** to your agent  
- Extended your PizzaBot to answer questions about **Contoso Pizza stores**  


## Final code sample

```python 
<!--@include: ./codesamples/agent_4_rag.py-->
```
