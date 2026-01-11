# Configurar Microsoft Foundry  

Nesta seção, você configurará o recurso Microsoft Foundry e implantará seu primeiro modelo para que esteja pronto para o workshop. Antes de começar o workshop, certifique-se de ter lido [como obter Azure](./get-azure) e [configurar seu ambiente de desenvolvimento](./dev-environment). 

## Passos  

1. **Fazer login no Azure**  
   - Faça login no [Portal Azure](https://portal.azure.com).  

---

2. **Criar um Recurso Microsoft Foundry**  
   - Navegue até o serviço [Microsoft Foundry](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/overview).  
   - Clique em **Create a resource**.  
   ![](/public/foundry/001.png)  

---

3. **Inserir os detalhes do recurso**  
   Preencha o formulário com os seguintes valores, depois clique em **Next**:  

   | Campo | Valor |  
   | -- | -- |  
   | **Subscription:** | Selecione a assinatura fornecida para este workshop |  
   | **Resource group:** | Clique em `Create new` e dê um nome descritivo ao seu grupo de recursos, ex: `pizza_workshop-RG` |  
   | **Name:** | Digite um nome único, ex: `pizza-foundry-resource-7yud` |  
   | **Region:** | Selecione **West US** (⚠️ Não selecione outra região) |  
   | **Project Name:** | `Pizza-Workshop` |  

   ![](/public/foundry/002.png)  

---

4. **Implantar o recurso**  
   - Clique em **Next** nas etapas restantes até chegar em **Review + Create**.  
   - Clique em **Create** para implantar o recurso.  
   - Aguarde 1–5 minutos para o recurso terminar de ser implantado.  

---

5. **Abrir Microsoft Foundry**  
   - Navegue até [AI.Azure.com](https://ai.azure.com).  
   - Agora você deve ver os projetos Microsoft Foundry vinculados à sua assinatura.  
   ![](/public/foundry/003.png)  
   - Clique no seu projeto, ex: **Pizza-Workshop**.  

---

6. **Implantar um modelo base**  
   - No projeto, vá para **Model + endpoints**.  
   ![](/public/foundry/004.png)  
   - Clique em **Deploy model** → **Deploy base model**.  
   ![](/public/foundry/005.png)  
   - Selecione o modelo **gpt-4o** e clique em **Confirm**.  
   ![](/public/foundry/006.png)  
   - Deixe todas as outras configurações com seus valores padrão e clique em **Deploy**.  
   ![](/public/foundry/007.png)  

   Isso tornará o modelo disponível no seu projeto para uso pelos seus agentes.  

---

7. **Testar o modelo**  
   - Quando a implantação estiver completa, clique em **Open in Playground**.  
   ![](/public/foundry/008.png)  
   - Na janela de chat, digite:  

     ```
     Hello world
     ```  

   - Você deve ver uma resposta do modelo **gpt-4o**. 🎉  

## Resumo  

Nesta seção de configuração, você:  
- Fez login no Portal Azure  
- Criou um **recurso Microsoft Foundry**  
- Implantou um **modelo base GPT-4o** no seu projeto  
- Testou o modelo no **Playground**  

Seu ambiente Azure agora está pronto para construir o **agente PizzaBot** nos próximos capítulos.  

*Traduzido usando GitHub Copilot.*
