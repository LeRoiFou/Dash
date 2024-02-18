"""
Lien : https://www.youtube.com/watch?v=LO8c7oXG32M
Site Charming : https://charming-data.circle.so/c/langchain-education/gpt4-vision-to-text-model
Cours : Plotly Graph Insights with LangChain & OpenAI

Dans ce tuto on a recours au LLM pour analyser un graphique

Mais l'analyse d'un graphique par LLM a certaines limites et a un coût :
https://platform.openai.com/docs/guides/vision/limitations

Concernant le type d'image à analyser :
https://platform.openai.com/docs/guides/vision/low-or-high-fidelity-image-understanding
Ici l'image est analysée à partir d'un encodage base 64 (image chargé en local)

Date : 18-02-24
"""
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
import time
import plotly.graph_objects as go
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import find_dotenv, load_dotenv
# pip install kaleido==0.1.0.post1

# BACK END -------------------------------------------------------------

# Récupération du fichier .env pour accès au site OpenAI
dotenv_path = find_dotenv()

# Chargement de la clé enregistrée dans le fichier .env
load_dotenv(dotenv_path)

# function for decoding graph image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/LangChain/Graph-Insights/domain-notable-ai-system.csv")

# 1er filtre opéré sur la DF à partir du champ 'Entity'
df = df[df.Entity != "Not specified"]

# 2ème filtre opéré sur la DF à partir du champ 'Year'
df = df[df['Year'] > 1999]

# Recoupement de la DF filtrée ci-avant à partir du champ 'Entity'
df = df[df['Entity'].isin(['Multimodal', 'Language'])]

# CONFIGURATION DES COMPANTS ----------------------------------------------

# Configuration du graphique linéaire
line_graph = px.line(df, # DF
                    x='Year', # Axe des abscisses
                    y='Annual number of AI systems by domain', # Axe des ordonnées
                    color='Entity', # Couleurs des lignes avec le champ 'Entity'
                    template='plotly_dark', # Affichage mode 'dark'
                    )
line_graph.update_layout(legend_title=None) # Pas de titre

# FRONT END ---------------------------------------------------------------

# Instanciation de la librairie Dash et thème appliqué
app = Dash(external_stylesheets=[dbc.themes.CYBORG])

# Configuration de la page @
app.layout = dbc.Container(
    [
        dcc.Markdown(
            "## Domain of notable AI systems, by year of publication\n" # Texte H2
            "###### Specific field, area, or category in which an AI system \
                is designed to operate or solve problems.",
                ), # Texte H5
        
        # Ligne n° 2
        dbc.Row(
            [   
                # Colonne unique
                dbc.Col(
                    [   
                        # Graphique linéaire sur le champ 'Entity'
                        dcc.Graph(id='line-graph', # pour le callback
                                  figure=line_graph, # config ci-avant
                                  ),
                        
                        # Menu déroulant sur le champ 'Entity'
                        dcc.Dropdown(
                            id="domain-slct", # Non utilisé pour le callback
                            multi=True, # multi-affichage
                            options=sorted(df['Entity'].unique()), # contenu
                            value=['Multimodal', 'Language', 'Games'], # valeurs affichées
                            ),
                        
                        # Texte
                        html.Div(
                            "This is a fake dropdown, just here for demo purposes.")
                    ],
                    width=6 # Largeur de la colonne
                ),
            ]
        ),
        
        # Ligne n° 3
        dbc.Row(
            [   
                # Colonne unique
                dbc.Col(
                    
                    # Bouton d'exécution
                    dbc.Button(
                        id='btn', # pour le callback
                        children='Insights', # texte
                        className='my-2',), 
                    width=1 # Largeur de la colonne
                    )
            ],
        ),
        
        # Ligne n° 4
        dbc.Row(
            [   
                # Colonne unique
                dbc.Col(
                    
                    # Sablier
                    dbc.Spinner(
                        
                        # Zone de texte (données vides)
                        html.Div(
                            id='content', # pour le callback
                            children='' # données vides
                            ), fullscreen=False), 
                    width=6 # Largeur de la colonne
                    )
            ],
        ),
    ]
)

# INTERACTION DES COMPOSANTS --------------------------------------------

# Recours au LLM pour analyse le graphique linéaire chargé en tant que fichier .png
@callback(
    Output('content','children'), # Sortie : 
    Input('btn','n_clicks'), # Entrée : bouton d'exécution
    State('line-graph','figure'), # State : graphique linéaire
    prevent_initial_call=True # Evite une erreur en cas de relance de la page @
)
def graph_insights(_, fig): # Numéro de chargement (bouton d'exécution), graphique
    
    # Récupération du graphique linéaire
    fig_object = go.Figure(fig)
    
    # Enregistrement du graphique dans un fichier PNG selon le chemin suivant :
    # à chaque fois qu'on appuye sur le bouton d'exécution, le nom de fichier
    # est complété du numéro du chargement : fig1.png, fig2.png, ...
    fig_object.write_image(f"images/fig{_}.png")
    
    # Temps de pause
    time.sleep(1)

    # Configuration du modèle OpenAI et du nombre max de jetons
    chat = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=256)
    
    # Instanciation du fichier .png contenant l'image
    image_path = f"images/fig{_}.png"
    
    # Encodage de l'image en base 64
    base64_image = encode_image(image_path)
    
    # Recours au LLM pour analyser le graphique
    result = chat.invoke(
        [
            # SystemMessage(
            #     content="You are an expert in data visualization that reads \
            #     images of graphs and describes the data trends in those images. \
            #     The graphs you will read are line charts that have\
            #     multiple lines in them. Please pay careful attention to the \
            #     legend color of each line and match them to the line color \
            #     in the graph. The legend colors must match the line colors \
            #     in the graph correctly."
            # ),
            HumanMessage(
                content=[
                    {"type": "text", 
                     "text": "What data insight can we get from this graph? \
                         Response in french."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "auto", # détail : low, high ou auto
                        },
                    },
                ]
            )
        ]
    )
    
    # MAJ du texte de réponse sur la page @
    return result.content


if __name__ == '__main__':
    app.run_server(debug=True)
