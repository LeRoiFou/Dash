"""
Lien : https://www.youtube.com/watch?v=acFOhdo_bxw&list=PLh3I780jNsiSDHCReNVtgPC1WkqduZA5R&index=10
Cours : How to build Interactive Excel Dashboard with Python - Dash

MAJ d'un diagramme en barres selon les valeurs choisies dans des menus déroulants

Date : 19-10-23
"""

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# DS ----------------------------------------------------------------------

# Récupération du fichier .csv converti en DF pandas
df = pd.read_csv("assets/vgsales.csv")


# FRONT END ----------------------------------------------------------------

# Instanciation de la sous-librairie Dash
app = Dash()

# Configuration de la page @
app.layout=html.Div([
    
    # Titre principal
    html.H1("Graph Analysis with Charming Data"),
    
    # Menu déroulant n° 1
    dcc.Dropdown(id='genre-choice', # pour le callback
                 options=[{'label':x, 'value':x} # valeurs du composant
                          for x in sorted(df.Genre.unique())],
                 value='Action', # valeur affichée par défaut
                 style={'width':'50%'}, # largeur du menu déroulant
                 ),
    
    # Menu déroulant n° 2
    dcc.Dropdown(id='platform-choice', # pour le callback
                 options=[{'label': x, 'value': x} # valeurs du composant
                          for x in sorted(df.Platform.unique())],
                 value='PS4', # valeur affichée par défaut
                 style={'width':'50%'}, # largeur du menu déroulant
                 ),
    
    # Graphique (vide)
    dcc.Graph(id='my-graph', # pour le callback
              figure={}, # Données vides
              ),
])

# INTERACTION ENTRE LES COMPOSANTS ----------------------------------

# MAJ du diagramme en barres selon les valeurs choisies dans les 2 menus déroulants
@callback(
    Output(
        component_id='my-graph', # Sortie : graphique
        component_property='figure'),
    Input(
        component_id='genre-choice', # Entrée : menu déroulant n° 1
        component_property='value'),
    Input(
        component_id='platform-choice', # Entrée : menu déroulant n° 2
        component_property='value')
)
def interactive_graphs(value_genre, value_platform):
    
    # 1er filtre de la DF selon la valeur choisie du menu déroulant n° 1
    dff = df[df.Genre==value_genre]
    
    # 2ème filtre de la DF selon la valeur choisie du menu déroulant n° 2
    dff = dff[dff.Platform==value_platform]
    
    # MAJ du diagramme en barres
    fig = px.bar(
        data_frame=dff, # DF filtrée
        x='Year', # Axe des abscisses
        y='Japan Sales', # Axe des ordonnées
        )
    
    return fig


if __name__=='__main__':
    app.run_server(debug=True)
