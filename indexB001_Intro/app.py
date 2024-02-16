"""
Introduction sur Dash

Date : 16-08-2023
"""

from dash import Dash
from dash import dcc
from dash import html

# Récupération d'un style pour la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie en objet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Connection au serveur
server = app.server

# Configuration de la page @
app.layout = html.Div(children=[
    
    # Titre principal de la page @
    html.H1(children='Tableau de bord Dash'),
    
    # Markdown
    html.Div('''Dash : A web application framework for Python'''),
    
    # Graphique
    dcc.Graph(
        id='example-graph',
        figure={
            'data':[
                {'x':[1, 2, 3], 'y':[4, 1, 2], 'type':'bar', 'name':'SF'}, 
                {'x':[1, 2, 3], 'y':[2, 4, 5], 'type':'bar', 'name':'Montréal'}],
            'layout':{'title':'Dash Data Visualisation'}
            }
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=False)
    