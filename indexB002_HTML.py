"""
Dans ce script, on modifie le style des éléments HTML du précédent script

Date : 16-08-23
"""

from dash import Dash
from dash import dcc
from dash import html

# Récupération d'un style pour la page @
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instanciation de la librairie en objet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Style
colors={
    'background':'#111111',
    'text':'#7FDBFF'}

# Configuration de la page @
app.layout = html.Div(
    style={'backgroundColor':colors['background']},
    children=[
    
    # Titre principal de la page @
    html.H1(children='Tableau de bord Dash',
            style={'textAlign':'center', 'color':colors['text']}),
    
    # Markdown
    html.Div(children='''Dash : A web application framework for Python''',
             style={'textAlign':'center', 'color':colors['text']}),
    
    # Graphique
    dcc.Graph(
        id='example-graph',
        figure={
            'data':[
                {'x':[1, 2, 3], 'y':[4, 1, 2], 'type':'bar', 'name':'SF'}, 
                {'x':[1, 2, 3], 'y':[2, 4, 5], 'type':'bar', 'name':'Montréal'}],
            'layout':{'title':'Dash Data Visualisation',
                      'plot_bgcolor':colors['background'],
                      'paper_bgcolor':colors['background'],
                      'font':{'color':colors['text']}}
            }
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
    