"""
Lien : https://www.youtube.com/watch?v=aEz1-72PKwc&list=PLh3I780jNsiS3xlk-eLU2dpW3U-wCq4LW&index=4
Cours : Bootstrap with Cards - Dash Plotly

Documentation sur les "cartes" :
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/

Documentation sur la mise en forme page @ :
https://bootswatch.com/default/

Présentation des cartes pour lesquelles on peut insérer différents composants

Date : 26-10-2023
"""

from dash import Dash, dcc, html, Output, Input       
import dash_bootstrap_components as dbc               
import plotly.express as px                     

# Récupération du fichier de la librairie plotly express
df = px.data.gapminder()

# CONFIGURATION DES COMPOSANTS -----------------------------------------------

# Configuration de la 1ère carte
card_main = dbc.Card(
    [   
        # Configuration de la photo rattachée à la carte
        dbc.CardImg(src="/assets/ball_of_sun.png", # Chemin et fichier récupéré
                    top=True, # Photo en haut des composants ci-après
                    bottom=False, # Photo n'est pas en bas des composants ci-après
                    title="Image by unknow", # survol (pour les malvoyants)
                    alt='Learn Dash Bootstrap Card Component', 
                    # alternatif : si la photo ne se charge pas, texte affiché
                    ),
        
        # Configuration de la carte
        dbc.CardBody(
            [   
                # Titre H4
                html.H4("Learn Dash with Charming Data", 
                        className="card-title"),
                
                # Titre H6
                html.H6("Lesson 1:", 
                        className="card-subtitle"),
                
                # Texte
                html.P("Choose the year you would like to see on the bubble chart.",
                       className="card-text",
                ),
                
                # Menu déroulant
                dcc.Dropdown(id='user_choice', # pour le callback
                             options=[{'label': yr, "value": yr} # valeurs : années
                                      for yr in df.year.unique()],
                             value=2007, # valeur affichée par défaut
                             clearable=False, # valeur affichée non supprimable
                             style={"color": "#000000"}, # couleur
                             ),
                
                # Bouton
                # dbc.Button(
                    # "Press me", # Texte du bouton
                    # color="primary", # Couleur du bouton
                    # ),
                    
                # Lien
                # dbc.CardLink("GirlsWhoCode", # Texte affiché
                #              href="https://girlswhocode.com/", # URL
                #              target="_blank", # Ouverture d'un autre onglet
                #     ),
            ]
        ),
    ],
    color="dark", # Couleur de fond de la carte
    inverse=True, # True : couleur du texte inversé (donc blanc ici)
    outline=False,
    # True : supprime les couleurs de l'arrière-plan et de l'en-tête
)

# Configuration de la 2ème carte
card_question = dbc.Card(
    [   
        # Configuration de la carte
        dbc.CardBody([
            
            # Titre H4
            html.H4("Question 1", 
                    className="card-title"),
            
            # Texte
            html.P("What was India's life expectancy in 1952?", 
                   className="card-text"),
            
            # Zone de liste de données
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("A. 55 years"),
                    dbc.ListGroupItem("B. 37 years"),
                    dbc.ListGroupItem("C. 49 years"),
                ], flush=True, # Séparation des listes ci-avant 
                )
        ]),
    ], color="warning", # Couleur de fond de la carte
)

# Configuration de la 3ème carte
card_graph = dbc.Card(
    
    # Graphique (vide)
    dcc.Graph(id='my_bar', # pour le callback
              figure={}, # données vides
              ), 
    
    body=True, # True : épaisseur de la bordure présente
    color="secondary", # Couleur de fond de la carte
)

# FRONT END ---------------------------------------------------------------------

# Instanciation de la librairie Dash
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configuration de la page @
app.layout = html.Div([
    dbc.Row([
        
        dbc.Col(
            
            # Titre principal de la page @
            html.H1("Bootstrap with Cards - Dash Plotly",
                    className='text-center text-primary'
        ))
    ]),
    
    dbc.Row([
        
        # 1ère carte
        dbc.Col(card_main, width=3), # large sur la page : 3/11ème
        
        # 2ème carte
        dbc.Col(card_question, width=3), # large sur la page : 3/11ème
        
        # 3ème carte
        dbc.Col(card_graph, width=5)], # large sur la page : 5/11ème
            
            justify="around"),  
            # justify="start" # position gauche de la page @
            # justify="center", # position centrée de la page @
            # justify="end", # position droite de la page @
            # justify="between", # position élargie de la page @
            # justify="around" # position justifiée, cohérente de la page @

    # Cartes les unes à côtés des autres avec une même largeur et une même hauteur
    # dbc.CardGroup([card_main, card_question, card_graph])   

])

# INTERACTION DES COMPOSANTS ----------------------------------------------

# Graphique nuage de points adapté selon l'année sélectionnée dans le menu déroulant
@app.callback(
    Output("my_bar", "figure"), # Sortie : graphique
    [Input("user_choice", "value")] # Entrée : menu déroulant
)
def update_graph(value):
    
    # MAJ du graphique : nuage de points
    fig = px.scatter(
        # DF filtrée selon l'année sélectionnée dans le menu déroulant
        df.query("year=={}".format(str(value))), 
        x="gdpPercap", # Axe des abscisses
        y="lifeExp", # Axe des ordonnées
        size="pop", # Taille des bulles selon les valeurs du champ 'pop'
        color="continent", # Couleur selon le champ 'continent'
        title=str(value), # Titre : année sélectionnée dans le menu déroulant
        hover_name="country", # Survol : nom du pays affiché
        log_x=True, # axe des abscisses à l'échelle des logarithmes
        size_max=60, # Taille max des bulles
        ).update_layout(
            showlegend=True, # Légende affichée
            title_x=0.5, # Titre centré par rapport au graphique
            )
    
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
