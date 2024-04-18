"""
Lien : https://www.youtube.com/watch?v=UARyjYaCekM
Cours : Build a Langchain Agent that Can Search the Web with frontend in Dash

Dans ce cours, on utilise la librairie TavilySearchResults qui permet d'obtenir
les données actuelles sur le web
On utilise également le composant 'store' qui permet de conserver les mots principaux
dans la question posée, afin de les récupérer éventuellement si une autre question
est posée et est en relation avec la question précédente

Date : 18-04-24
"""

from dotenv import find_dotenv, load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.load import dumps, loads
from dash import Dash, dcc, html, callback, Output, Input, State, no_update
# pip install -r requirements.txt -> saisi dans le terminal pour MAJ des librairies

# BACK END --------------------------------------------------------------

# Activation des clés API
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Configuration du LLM avec un degré de précision au plus près
llm = ChatOpenAI(temperature=0)

# Librairie pour obtenir les données @ actuelles et configuration
tavily_tool = TavilySearchResults()
tools = [tavily_tool]

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant. Make sure to use the tavily_search_results_json tool for information"),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True, # commentaire dans le terminal de la discussion
)

def process_chat(agent_executor, user_input, chat_history):
    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    return response["output"]

# FRONT END --------------------------------------------------------------

# Sous-librairie Dash
app = Dash()

# Configuration de la page @
app.layout = html.Div([
    
    # Titre de la page @
    html.H2("Ask me anything. I'm your personal assistant that can search the web"),
    
    # Zone de saisie
    dcc.Input(id="my-input", # pour le callback
              type="text", # type texte
              debounce=True, # fin de saisie du texte avant exécution
              style={"width":500, "height":30}, # largeur / longueur
              ),
    
    # Saut de ligne
    html.Br(),
    
    # Bouton d'exécution
    html.Button(
        "Submit", # Texte
        id="submit-query", # Pour le callback
        style={"backgroundColor":"blue", "color":"white"}, # couleurs
        ),
    
    # Conservation des données
    dcc.Store(id="store-it", # pour le callback
              data=[], # données vides
              ),
    
    # Libellé (vide)
    html.P(),
    
    # Zone de réponse
    html.Div(id="response-space", # pour le callback
             )
])

# INTERACTION DES COMPOSANTS ---------------------------------------------------

@callback(
    Output("response-space", "children"), # Zone de réponse
    Output("store-it","data"), # Récupération des données conservées
    Input("submit-query", "n_clicks"), # Bouton d'exécution
    State("my-input", "value"), # Zone de saisie
    State("store-it","data"), # Récupération des données conservées
    prevent_initial_call=True # Evite affichage erreur lors du lancement page @
)
def interact_with_agent(n, user_input, chat_history):
    
    # S'il y a une donnée conservée (mot(s) de la question posée)
    if len(chat_history) > 0:
        chat_history = loads(chat_history) # deserialize the chat_history (convert json to object)
    print(chat_history)

    response = process_chat(agent_executor, user_input, chat_history)
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response))

    history = dumps(chat_history)  # serialize the chat_history (convert the object to json)

    return f"Assistant: {response}", history

if __name__ == '__main__':
    app.run_server(debug=True)
