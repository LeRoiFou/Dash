"""
Lien : https://www.youtube.com/watch?v=t1bKNj021do&list=PLh3I780jNsiS3xlk-eLU2dpW3U-wCq4LW&index=6
Cours : Dash Bootstrap Spinner & Progress Bar

Démonstration du style de chargement :
https://tobiasahlin.com/spinkit/

Composant sur le chargement :
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/spinner/

Documentation sur le composant dcc.Loading :
https://dash.plotly.com/dash-core-components/loading

Documentation sur la barre de progression :
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/progress/

Cours sur le "sablier" (en attente de chargement)

Fichier .css dans le répertoire 'asset' avec le même nom

Date : 03-11-2023
"""

from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc 
import plotly.express as px
import pandas as pd 

# BACK END --------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/green_tripdata_2019-01.csv")

# Filtre sur la DF
df = df[df["total_amount"] > 0]

# Limite des lignes à récupérer
df = df[:150_000]

# FRONT END -------------------------------------------------------------------

# Instanciation de la librairie Dash et mise en page @
app = Dash(external_stylesheets=[dbc.themes.LUMEN])

# Configuration de la page @
app.layout = html.Div(
    children=[
        dbc.Row(
            
            dbc.Col(
                
                # Sablier s'affichant lors du chargement du graphique
                dbc.Spinner(
                    children=[
                        
                        # Graphique (vide)
                        dcc.Graph(id="loading-output", # pour le callback
                                  )], 
                    size="lg", # or "sm", "md"
                    color="primary", # ... or #FFFF00...
                    type="border", # or "grow"
                    fullscreen=True,
                    ),
                
            # spinner_style={"width": "10rem", "height": "10rem"}),
            # spinnerClassName="spinner"),
            # dcc.Loading(
                # children=[dcc.Graph(id="loading-output")], 
                # color="#119DFF", 
                # type="dot", # or “graph”, “cube”, “circle”, “default”
                # fullscreen=True,
                # ),

            width={'size': 12, 'offset': 0}),
        ),

        dbc.Row([
            
            dbc.Col(
                
                # Zone de saisie
                dbc.Input(
                    id="passenger_count", # pour le callback
                    type="number", # type requis
                    min=1, # valeur min
                    max=6, # valeur max
                    step=1, # échelle
                    value=1, # valeur affichée par défaut
                    ),
                
                width={'size': 2, # largeur
                       'offset': 1, # décalage
                       }),
            
            dbc.Col(
                
                # Bouton d'exécution
                dbc.Button(
                    id="loading-button", # pour le callback
                    n_clicks=0, # bouton non appuyé dès chargement page @
                    children=["Passengers"], # Texte du bouton
                    ),
                
                width={'size': 1, # largeur
                       'offset': 0, # décalage
                       })
            
        ]), 

        # Saut de ligne
        html.Br(),
        
        dbc.Row(
            
            dbc.Col(
                
                # Barre de progression (ne marche plus...)
                dbc.Progress(
                    children=["25%"], # valeur affichée sur la barre de progression
                    value=25, # Progression par défaut
                    max=100, # valeur max
                    striped=True,
                    color="success", # couleur de la barre de progression
                    style={"height": "20px"}, # hauteur de la barre de progression
                    ),
                
                width={'size': 5, # largeur
                       'offset': 1, # décalage
                       }),
        ),
    ]
)

# INTERACTION DES COMPOSANTS ----------------------------------------------

# MAJ de l'histogramme selon la valeur affichée à la zone de saisie et après avoir
# appuyé sur le bouton d'exécution
@callback(
    Output("loading-output", "figure"), # Sortie : graphique
    [Input("loading-button", "n_clicks")], # Entrée : bouton d'exécution
    [State("passenger_count", "value")] # State : zone de saisie
)
def load_output(n_clicks, psg_num):
    
    # Si le bouton d'exécution a été appuyé : MAJ de l'histogramme
    if n_clicks:
        
        # Filtre sur la DF en fonction de la valeur affichée dans la zone de saisie
        dff = df[df["passenger_count"] == psg_num]
        
        # MAJ du graphique : histogramme
        fig = px.histogram(
            dff, # DF filtrée
            x="total_amount", # Axe des abscisses
            title="NYC Green Taxi Rides", # Titre du graphique
            ).update_layout(title_x=0.5) # Titre centré
        
        return fig
    
    # Sinon affichage de l'histogramme selon les données ci-après
    return px.histogram(
        df.query(f"passenger_count=={psg_num}"), # Filtre selon la valeur affichée
        x="total_amount", # Axe des abscisses
        title="NYC Green Taxi Rides", # Titre du graphique
        ).update_layout(title_x=0.5) # Titre centré


if __name__ == "__main__":
    app.run_server(debug=True)
