# Adicionando Conhecimento com Busca de Arquivos  

Nos capítulos anteriores, você criou um agente básico e deu instruções através de um prompt de sistema.  
Agora é hora de **tornar seu agente mais inteligente** fundamentando-o em **seus próprios dados**.  



## Por Que Adicionar Conhecimento?  

Por padrão, o modelo só sabe o que foi treinado - não tem acesso às informações privadas ou específicas do domínio da sua organização.  
Para preencher essa lacuna, usaremos **Geração Aumentada por Recuperação (RAG)**.  

- **RAG** permite que o agente busque informações relevantes dos seus próprios dados antes de gerar uma resposta.  
- Isso garante que as respostas do seu agente sejam **precisas, atualizadas e fundamentadas** em informações reais.  
- No Microsoft Foundry, usaremos o recurso **File Search** para implementar isso.  

Neste capítulo, você usará uma pasta chamada **`./documents`** que contém informações sobre **lojas da Contoso Pizza** - como localizações, horários de funcionamento e menus.  

Vamos fazer upload desses arquivos para um **vector store** e conectar esse store ao agente usando uma **ferramenta de File Search**.  


## Passo 1 - Atualizar Seus Imports  

Primeiro, atualize seus imports no topo do `agent.py` para incluir as classes necessárias:  

```python
import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, Tool
```

## Passo 2 - Criar o Vector Store  

Adicione este código após criar seu `openai_client` para criar um vector store e fazer upload dos documentos:  

```python
vector_store_id = ""  # Defina o ID do seu vector store se já tiver um

## -- BUSCA DE ARQUIVOS -- ##

if vector_store_id:
    vector_store = openai_client.vector_stores.retrieve(vector_store_id)
    print(f"Usando vector store existente (id: {vector_store.id})")
else:
    # Criar vector store para busca de arquivos
    vector_store = openai_client.vector_stores.create(name="ContosoPizzaStores")
    print(f"Vector store criado (id: {vector_store.id})")

    # Fazer upload de arquivo para o vector store
    for file_path in glob.glob("documents/*.md"):
        file = openai_client.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id, file=open(file_path, "rb")
        )
        print(f"Arquivo enviado para o vector store (id: {file.id})")
## -- BUSCA DE ARQUIVOS -- ##
```

**Por quê:**  
- Um vector store armazena e indexa embeddings de documentos para busca semântica.
- Na primeira vez que você executar o script, ele cria um novo vector store e faz upload de todos os documentos.
- Nas execuções subsequentes, você pode definir `vector_store_id` para reutilizar o store existente.

**Dica:** Após a primeira execução, copie o ID do vector store da saída e defina na variável `vector_store_id` para evitar recriá-lo toda vez.


## Passo 3 - Adicionar a Ferramenta de File Search  

Agora adicione a ferramenta File Search ao toolset do seu agente. Adicione isso antes de criar o agente:  

```python
## Definir o toolset para o agente
toolset: list[Tool] = []
toolset.append(FileSearchTool(vector_store_ids=[vector_store.id]))
```


## Passo 4 - Atualizar a Criação do Agente  

Modifique a criação do seu agente para incluir o toolset:  

```python
## Criar um Foundry Agent
agent = project_client.agents.create_version(
    agent_name="hello-world-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=open("instrucoes.txt").read(),
        tools=toolset,
    ),
)
print(f"Agente criado (id: {agent.id}, nome: {agent.name}, versão: {agent.version})")
```



## Passo 5 - Executar o Agente  

Experimente:  

```bash
python agent.py
```

Faça perguntas como:  
> "Quais lojas da Contoso Pizza estão abertas após as 20h?"  
> "Onde fica a loja Contoso Pizza mais próxima?"  

Digite `exit` ou `quit` ou `sair` para parar a conversa.  



## Resumo  

Neste capítulo, você:  
- Aprendeu como **RAG** fundamenta seu agente com seus próprios dados  
- Criou e populou um **vector store** diretamente no seu script  
- Adicionou uma **ferramenta de File Search** ao seu agente  


## Amostra de código final

```python 
<!--@include: ../codesamples/pt/agent_4_rag.py-->
```

*Traduzido usando GitHub Copilot.*
