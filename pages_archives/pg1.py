"""
Lien : https://www.youtube.com/watch?v=Hc9_-ncr4nU&list=PLh3I780jNsiQWkxk05ek4M7rbLocVQaAb&index=9
Cours : How to Make a Python Multi Page Application with Plotly Dash

Documentation sur les multi-pages :
https://dash.plotly.com/urls#dash-pages

Cours indexG007_MultiPage.py

Date : 17-11-2023
"""

from dash import dcc, html, register_page
import plotly.express as px

# Récupération du fichier dans la librairie plotly
df = px.data.gapminder()

# Assignation de la librairie
register_page(__name__, path='/pg1') # '/pg1' -> page d'accueil

# Configuration de la page @
layout = html.Div(
    [   
        # Menu déroulant
        dcc.Dropdown(
            [x for x in df.continent.unique()], # Valeurs du menu déroulant
            id='cont-choice', # pour le callback
            style={'width':'50%'}, # largeur du composant
            ),
        
        # Graphique : histogramme
        dcc.Graph(
            id='line-fig', # pour le callback
            figure=px.histogram(
                df, # DF récupérée de ploltly
                x='continent', # Axe des abscisses
                y='lifeExp', # Axe des ordonnées
                histfunc='avg', # valeurs des données du diagramme
                ))
    ]
)
