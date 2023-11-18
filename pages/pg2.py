"""
Lien : https://dash.plotly.com/urls#dash-pages
Cours : https://dash.plotly.com/urls#dash-pages

Fichier principal : indexG008_MultiPage.py

Date : 18-11-2023
"""

from dash import register_page, dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

# Récupération des données de la librairie plotly express
df = px.data.tips()

# Configuration de l'onglet
register_page(__name__, name='Tip Analysis')

# Configuration de la page @
layout = html.Div(
    [
        dbc.Row([
            
            dbc.Col(
                [   
                    # Image
                    html.Img(src='assets/smoking2.jpg')
                ], width=4
            ),
            
            dbc.Col(
                [
                    # Boutons d'option
                    dcc.RadioItems(
                        df.day.unique(), # DF données uniques du champ 'day'
                        id='day-choice', # pour le callback
                        value='Sat', # valeur affichée par défaut
                        )
                ], width=6
            )
        ]),
        
        dbc.Row([
            
            dbc.Col(
                [
                    # Graphique : diagramme en barres
                    dcc.Graph(
                        id='bar-fig', # pour le callback
                        figure=px.bar(df, # DF
                                      x='smoker', # Axe des abscisses
                                      y='total_bill', # Axe des ordonnées
                                      ))
                ], width=12
            )
        ])
    ]
)

# MAJ du graphique selon la valeur sélectionnée du champ 'day' dans le composant
# boutons d'option
@callback(
    Output('bar-fig', 'figure'), # Sortie : graphique
    Input('day-choice', 'value') # Entrée : boutons d'option
)
def update_graph(value):
    
    # Filtre de la DF selon la valeur sélectionnée des boutons d'option du champ 'day'
    dff = df[df.day==value]
    
    # Configuration du diagramme en barres
    fig = px.bar(dff, # DF filgrée ci-avant
                 x='smoker', # Axe des abscisses
                 y='total_bill', # Axe des ordonnées
                 )
    
    # MAJ du graphique
    return fig
