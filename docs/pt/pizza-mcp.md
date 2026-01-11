
# Servidor MCP de Pizza

Para este workshop usamos o exemplo Open Source [Pizza MCP Agent](https://github.com/Azure-Samples/pizza-mcp-agents).

::: danger
Isso só é relevante a partir do capítulo 6 do workshop.
:::

Este projeto demonstra como construir agentes de IA que podem interagir com APIs do mundo real usando o Model Context Protocol (MCP). Ele apresenta um sistema completo de pedidos de pizza com uma API serverless, interfaces web e um servidor MCP que permite que agentes de IA naveguem menus, façam pedidos e acompanhem o status dos pedidos.

O sistema consiste em múltiplos serviços interconectados:
- **Servidor MCP de Pizza:** Servidor MCP que habilita interações de agentes de IA
- **Aplicativo web de Pizza:** Painel de pedidos ao vivo, mostrando status de pedidos de pizza em tempo real
- **Sistema de registro:** Registro de usuário para acessar o sistema de pedidos de pizza

|  Nome | Descrição |
|-----------|-------------|
| Servidor MCP de Pizza | [<!--@include: ./variables/mcp-url.md-->](<!--@include: ./variables/mcp-url.md-->)|
| Aplicativo web de Pizza | [<!--@include: ./variables/pizza-dashboard.md-->](<!--@include: ./variables/pizza-dashboard.md-->)|
| Sistema de registro | [<!--@include: ./variables/customer-registration.md-->](<!--@include: ./variables/customer-registration.md-->) |


## Visão Geral

Este é o servidor MCP de Pizza, expondo a API de Pizza como um servidor Model Context Protocol (MCP). O servidor MCP permite que LLMs interajam com o processo de pedidos de pizza através de ferramentas MCP.

Este servidor suporta os seguintes tipos de transporte:
- **HTTP Streamable**
- **SSE** (legado, não recomendado para novas aplicações)

## Ferramentas MCP

O servidor MCP de Pizza fornece as seguintes ferramentas:

| Nome da Ferramenta | Descrição |
|-----------|-------------|
| get_pizzas | Obtém uma lista de todas as pizzas no menu |
| get_pizza_by_id | Obtém uma pizza específica pelo seu ID |
| get_toppings | Obtém uma lista de todas as coberturas no menu |
| get_topping_by_id | Obtém uma cobertura específica pelo seu ID |
| get_topping_categories | Obtém uma lista de todas as categorias de coberturas |
| get_orders | Obtém uma lista de todos os pedidos no sistema |
| get_order_by_id | Obtém um pedido específico pelo seu ID |
| place_order | Faz um novo pedido com pizzas (requer `userId`) |
| delete_order_by_id | Cancela um pedido se ainda não foi iniciado (status deve ser `pending`, requer `userId`) |

## Testar com MCP inspector

Primeiro, você precisa iniciar a API de Pizza e o servidor MCP de Pizza localmente.

1. Em uma janela de terminal, inicie o MCP Inspector:
    ```bash
    npx -y @modelcontextprotocol/inspector
    ```
2. Ctrl+clique para carregar o aplicativo web MCP Inspector a partir da URL exibida pelo aplicativo (ex: http://127.0.0.1:6274)
3. No MCP Inspector, defina o tipo de transporte para **SSE** e 
3. Coloque `<!--@include: ./variables/mcp-url.md-->` no campo URL e clique no botão **Connect**.
4. Na aba **Tools**, selecione **List Tools**. Clique em uma ferramenta e selecione **Run Tool**.

> [!NOTE]
> Esta aplicação também fornece um endpoint SSE se você usar `/sse` em vez de `/mcp` no campo URL. 

*Traduzido usando GitHub Copilot.*
