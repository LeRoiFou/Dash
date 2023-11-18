"""
Lien : https://dash.plotly.com/urls#dash-pages
Cours : https://dash.plotly.com/urls#dash-pages

Fichier principal : indexG008_MultiPage.py

Date : 18-11-2023
"""

from dash import register_page, dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px


# Récupération du fichier de la librairie plotly
df = px.data.gapminder()

# Configuration de l'onglet
register_page(__name__, path='/', name='Home') # page d'accueil

# Configuration de la page @
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Menu déroulant
                        dcc.Dropdown(
                            options=df.continent.unique(), # valeurs du composant
                            id='cont-choice', # pour le callback
                            )
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4 
                )
            ]
        ),
        
        dbc.Row(
            [
                dbc.Col(
                    [   
                        # Graphique : histogramme
                        dcc.Graph(
                            id='line-fig', # histogramme
                            figure=px.histogram(df, # DF
                                                x='continent', # Axe des abscisses
                                                y='lifeExp', # Axe des ordonnées
                                                histfunc='avg', # Données du graph
                                                ))
                    ], width=12
                )
            ]
        )
    ]
)

# MAJ de l'histogramme selon qu'une valeur est affichée au menu déroulant ou pas
@callback(
    Output('line-fig', 'figure'), # Sortie : graphique
    Input('cont-choice', 'value') # Entrée : menu déroulant (données affichées)
)
def update_graph(value):
    
    # Si aucune valeur du menu déroulant n'est affichée
    if value is None:
        
        # Configuration de l'histogramme
        fig = px.histogram(df, # Récupération de toutes les données de la DF
                           x='continent', # Axe des abscisses
                           y='lifeExp',  # Axe des ordonnées
                           histfunc='avg', # Données de l'histogramme
                           )
    else:
        
        # DF filtrée au champ 'continent' selon la valeur affichée au menu déroulant
        dff = df[df.continent==value] 
        
        # Configuration de l'histogramme
        fig = px.histogram(dff, # DF filtrée ci-avant
                           x='country', # Axe des abscisses
                           y='lifeExp', # Axe des ordonnées
                           histfunc='avg', # Données de l'histogramme
                           )
    # MAJ de l'histogramme
    return fig
