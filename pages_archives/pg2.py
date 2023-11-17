"""
Lien : https://www.youtube.com/watch?v=Hc9_-ncr4nU&list=PLh3I780jNsiQWkxk05ek4M7rbLocVQaAb&index=9
Cours : How to Make a Python Multi Page Application with Plotly Dash

Documentation sur les multi-pages :
https://dash.plotly.com/urls#dash-pages

Cours indexG007_MultiPage.py

Date : 17-11-2023
"""

from dash import html, dcc, register_page
import plotly.express as px

# Récupération de la DF dans plotly
df = px.data.tips()

# Instanciation de la librairie
register_page(__name__)

layout = html.Div(
    [   
        # Boutons d'option
        dcc.RadioItems(
            [x for x in df.day.unique()], # Valeurs du composant
            id='day-choice', # pour le callback
            ),
        
        # Graphique : diagramme en barres
        dcc.Graph(
            id='bar-fig', # pour le callback
            figure=px.bar(df, # DF récupérée dans plotly
                          x='smoker', # Axe des abscisses
                          y='total_bill', # Axe des ordonnées
                          ))
    ]
)
