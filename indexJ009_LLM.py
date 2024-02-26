"""
Lien : https://www.youtube.com/watch?v=qzrkhDrFcJs
Cours : I Built a Document Summarizer with LangChain Quickstart Retrieval Chapter

Récupération d'une url ou d'un PDF puis poser une question sur le document chargé
(résumé, recherche d'un point particulier…)

Documentation sur le thème présenté ci-avant :
LangChain Quickstart Retrieval Chain: https://python.langchain.com/docs/get_started/quickstart#retrieval-chain

Documentation sur le chargement d'url avec langchain
https://python.langchain.com/docs/integrations/document_loaders/web_base

Documentation sur le chargement de pdf avec langchain :
https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf

Modules installés :
pip install langchain-community
pip install langchain

Date : 26-02-24 
"""

from dash import Dash, dcc, html, Input, Output, State, callback
import dash_mantine_components as dmc
from dotenv import find_dotenv, load_dotenv
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain

# BACK END -------------------------------------------------------------

# Récupération du fichier .env pour accès au site OpenAI
dotenv_path = find_dotenv()

# Chargement de la clé enregistrée dans le fichier .env
load_dotenv(dotenv_path)

# Configuration du modèle OenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo") 

# Configuration du prompt
prompt = ChatPromptTemplate.from_template(
    """Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# Chain the LLM to the prompt
document_chain = create_stuff_documents_chain(llm, prompt)  

# FRONT END ---------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash()

# Configuration de la page @
app.layout = html.Div(
    [   
        # Contenu des composants
        dmc.Container(
            children=[
                
                # Titre principal de la page @
                dmc.Title(order=1, children="Online Document Summarizer"),
                
                # Zone de saisie : page @ ou pdf à alimenter
                dmc.TextInput(
                    label="Summarize Doc", # Titre
                    placeholder="Enter the webpage or pdf...", # Texte affiché
                    id="input-1", # pour le callback
                    ),
                
                # Zone de saisie : question à poser
                dmc.TextInput(
                    label="Ask your question", # Titre
                    placeholder="Ask away...", # Texte affiché
                    id="input-2", # pour le callback
                    ),
                
                # Zone de réponse
                dcc.Loading(html.Div(id='answer-space', # pour le callback
                                     )),
                
                # Bouton d'exécution
                dmc.Button(children="Submit", # Texte du bouton
                           id="submit-btn", # pour le callback
                           mt="md",
                           )
            ],
            style={"maxWidth": "500px", "margin": "0 auto"},
        )
    ]
)

# INTERACTION DES COMPOSANTS -------------------------------------------

@callback(
    Output('answer-space', 'children'), # Sortie : zone de réponse
    Input('submit-btn', 'n_clicks'), # Entrée : bouton d'exécution
    State('input-1', 'value'), # State : pdf ou page url copiée
    State('input-2', 'value'), # State : question à poser
    prevent_initial_call=True # Evite une erreur lors du chargement de la page @
)
def update_output(n_clicks, input1, input2):
    
    # Si c'est un pdf chargé (ignore min/maj de 'pdf')
    if bool(re.search(r'\.pdf$', input1, re.IGNORECASE)):
        
        # Chargement du pdf avec la librairie langchain, exemple de fichier chargé :
        # https://image-us.samsung.com/SamsungUS/tv-ci-resources/2018-user-manuals/2018_UserManual_Q9FNSeries.pdf
        # https://arxiv.org/pdf/2304.03271.pdf
        loader = PyPDFLoader(input1)   
        docs = loader.load_and_split()
    
    # Si c'est une URL
    else:
        
        # Chargement de l'url avec la librairie langchain, exemple d'url chargé :
        # https://en.wikipedia.org/wiki/Paris
        loader = WebBaseLoader(input1)  
        docs = loader.load()

    # Transformation du texte en vecteurs (représentation sémantique du texte, 
    # cad capturer le sens  et la relation entre les mots, phrases ou documents au
    # lieu de traiter le texte comme une séquence de mots)
    embeddings = OpenAIEmbeddings()
    
    # Division du texte en morceaux -> utilité notamment lorsqu'on a 
    # des milliers de mots à traiter... pour une manipulation "fine" du texte
    text_splitter = RecursiveCharacterTextSplitter()

    # Division des documents en textes plus petits en utilisant 
    # un séparateur spécifié
    documents = text_splitter.split_documents(docs)

    # Cette instruction permet de stocker dans une BDD et et d'indexer efficacement 
    # les intégrations de documents pour des opérations de recherche 
    # et de récupération ultérieures : une fois les documents indexés, on peut 
    # interroger la base de données FAISS pour retrouver des documents pertinents 
    # en fonction des requêtes spécifiées.
    vector = FAISS.from_documents(documents, embeddings)

    # Recherche et récupération de documents pertinents en réponse à une requête
    # de l'utilisateur
    retriever = vector.as_retriever()
    
    # Permet de créer une chaîne de récupération qui extrait des documents 
    # et les transmettre ensuite. Cette fonction permet de mettre en place 
    # un processus où les documents sont récupérés en réponse à une requête, puis 
    # ces documents sont combinés et traités pour générer une réponse pertinente.
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    # What was Paris architecture like in the 19th century
    # How can I fix my remote control?
    # How many litters of water did google consume in 2022?
    # How does AI use water?
    
    # En utilisant cette fonction, on peut déclencher le processus de récupération 
    # des documents pertinents en réponse à une requête spécifique, 
    # puis traiter ces documents pour produire une réponse significative. 
    response = retrieval_chain.invoke(
        {"input": input2})

    # Récupération de la valeur concernant la clé "answer"
    return response["answer"]


if __name__ == '__main__':
    app.run_server(debug=True)