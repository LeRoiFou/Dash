"""
Lien : https://www.youtube.com/watch?v=QJFsbIYwvHw&list=PLh3I780jNsiQWkxk05ek4M7rbLocVQaAb&index=7
Cours : Enhance your Dashboard App with Lottie (small gifs)

Nouveau composant : de.Lottie, qui est une image animée (gifs) chargée à partir d'un
fichier JSON récupéré d'une URL

Liens pour les images animées :
https://lottiefiles.com/featured
https://lottiefiles.com/animations/i-love-it-7zyxHAK8nD

Date : 17-11-2023
"""

from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_extensions as de  # pip install dash-extensions

# BACK END ------------------------------------------------------------------------

# Lotties: Emil at https://github.com/thedirtyfew/dash-extensions
url = "https://assets1.lottiefiles.com/private_files/lf30_WdTEui.json"
url2 = "https://assets9.lottiefiles.com/packages/lf20_CYBIbn.json"
options = dict(loop=True, # False : Si image cliquée, l'anim ne se relance plus
               autoplay=True, # Lecture automatique
               rendererSettings=dict(preserveAspectRatio='xMidYMid slice')
               )

# Récupération du fichier plotly
df = px.data.gapminder()

# FRONT END ----------------------------------------------------------

# Instanciation de la librairie Dash et mise en page @
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Carte : cadre
card_main = dbc.Card(
    [
        # Cartes
        dbc.CardBody(
            [
                html.Div(
                    
                    # Image animée
                    de.Lottie(
                        options=options, # configuration back-end
                        width="50%", # Largeur
                        height="50%", # Hauteur
                        url=url, # URL téléchargement fichier JSON
                        )),
                
                # Titre H4
                html.H4(
                    "Learn Dash with Charming Data", 
                    className="card-title",
                    ),
                
                # Titre H6
                html.H6(
                    "Lesson 1:", 
                    className="card-subtitle"),
                
                # Libellé
                html.P(
                    "Choose the year you would like to see on the bubble chart.",
                    className="card-text",
                ),
                
                # Menu déroulant : récupération des années de la DF
                dcc.Dropdown(
                    id='user_choice', # pour le callback
                    options=[{'label': yr, "value": yr} # valeurs du menu déroulant
                             for yr in df.year.unique()],
                    value=2007, # affichage par défaut
                    clearable=False, # valeur affiché non supprimable
                    style={"color": "#000000"}, # couleur du composant
                    ),
            ]
        ),
    ],
    color="success", # Couleur de la carte
    inverse=True,   # Couleur inversée (texte de couleur blanc)
    outline=False,  # True = supprime la couleur de fond de la carte
    className="mt-3" # Espacement marge haut
)

# Carte : cadre
card_question = dbc.Card(
    [   
        # Carte
        dbc.CardBody([
            
            html.Div(
                
                # Image animée
                de.Lottie(
                    options=options, # configuration back-end
                    width="50%", # Largeur
                    height="50%", # Hauteur
                    url=url2, # URL Lien du téléchargement du fichier JSON
                    speed=1, # Vitesse d'animation
                    )),
            
            # Titre H4
            html.H4("Question 1", 
                    className="card-title",
                    ),
            
            # Texte
            html.P("What was India's life expectancy in 1952?", 
                   className="card-text"),
            
            # Liste groupe avec ses composants de liste ci-après
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("A. 55 years"),
                    dbc.ListGroupItem("B. 37 years"),
                    dbc.ListGroupItem("C. 49 years"),
                ], flush=True)
        ]),
    ], 
    color="warning", # Couleur de fond de la carte
    className="mt-3" # Espacement marge haut
)

# Carte : cadre
card_graph = dbc.Card(
        
        # Graphique (données vides)
        dcc.Graph(
            id='my_bar', # pour le callback
            figure={}, # Données vide
            ), 
        body=True, # Bordure présente
        color="secondary", # Couleur de fond de la carte
        className="mt-3" # Espacement marge haut
)

# Configuration de la page @
app.layout = html.Div([
    dbc.Row([dbc.Col(card_main, width=3),
             dbc.Col(card_question, width=3),
             dbc.Col(card_graph, width=5)], 
            justify="around"),  # justify="start", "center", "end", "between", "around"

])

# INTERACTION DES COMPOSANTS -------------------------------------------------

# MAJ du graphique nuage de points selon la valeur affichée au menu déroulant
@callback(
    Output("my_bar", "figure"), # Sortie : graphique
    [Input("user_choice", "value")] # Entrée : menu déroulant
)
def update_graph(value):
    
    # Configuration du graphique : nuage de points
    fig = px.scatter(
        df.query("year=={}".format(str(value))), # Filtre selon l'année 
        x="gdpPercap", # Données axe des abscisses
        y="lifeExp", # Données axe des ordonnées
        size="pop", # Taille des bulles selon ce champ
        color="continent", # Couleur selon ce champ
        title=str(value), # Titre : année affichée du menu déroulant
        hover_name="country", # Survol : titre selon ce champ
        log_x=True, # Echelle logarithmique pour l'axe des abscisses
        size_max=60, # Taille max des bulles
        ).update_layout(showlegend=True, # Légende à afficher
                        title_x=0.5, # Titre du graphique centré
                        )
    
    # MAJ du nuage de points
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
